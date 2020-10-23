# -*- coding: utf-8 -*-
"""Classifier module"""
import json
import os
import logging
from pathlib import Path

import asyncio
from nats.aio.client import Client as NATS
import webcolors
import constants as const

logging.getLogger().setLevel(
    getattr(logging, os.environ.get('LOG_LEVEL') or const.DEFAULT_LOG_LEVEL))


def closest_color(non_web_color):
    """Find closest Web color from given non-Web color using Euclidean distance

    Args:
        non_web_color (list[int]): Non-Web color

    Returns:
        string - name of the closest Web color
    """
    min_colours = {}
    for key, name in webcolors.HTML4_HEX_TO_NAMES.items():
        red, green, blue = webcolors.hex_to_rgb(key)
        r_dist = (red - non_web_color[0]) ** 2
        g_dist = (green - non_web_color[1]) ** 2
        b_dist = (blue - non_web_color[2]) ** 2
        min_colours[(r_dist + g_dist + b_dist)] = name
    return min_colours[min(min_colours.keys())]


def get_color_name(color):
    """Obtains colors Web name or closest color's Web name

    Args:
        color (list[int]): List containing R, G, B values

    Returns:
        (str, str) - actual color name (can be None) and closest color name
    """
    try:
        closest = actual = webcolors.rgb_to_name(color)
        if actual not in webcolors.HTML4_HEX_TO_NAMES.values():
            raise ValueError  # only 16 colors mode
    except ValueError:
        closest = closest_color(color)
        actual = None
    return actual, closest


def classify_image(file_path, color):
    """Classify an image based on its average color

    Args:
        file_path (string): Path to file
        color (string): Average color name

    Returns:
        string with final destination of image

    """
    file_name = os.path.split(file_path)[1]
    final_destination = Path(const.CLASSIFIED_IMAGES + color)
    if not os.path.isdir(final_destination):
        os.makedirs(final_destination)
    new_path = f"{final_destination}/{file_name}"
    Path(file_path).rename(new_path)
    return new_path


async def run(loop):
    """Classify the image by moving it to its respective directory"""
    nats = NATS()
    await nats.connect(const.NATS_SERVER, loop=loop)

    async def callback(msg):
        data = msg.data.decode()
        reply = msg.reply
        data = json.loads(data)
        avg_color = data["avg_color"]
        file_path = data["file_path"]
        # validate file path
        if not os.path.isfile(file_path):
            logging.error("File not found %s", file_path)
            await nats.publish(reply, b"OK")
            return
        actual_color_name, closest_color_name = get_color_name(avg_color)
        path = classify_image(color=(actual_color_name or closest_color_name), file_path=file_path)
        logging.info('Classified image %s to %s', file_path, path)
        await nats.publish(reply, b"OK")

    await nats.subscribe("output", cb=callback)


if __name__ == "__main__":
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(run(LOOP))
    LOOP.run_forever()
