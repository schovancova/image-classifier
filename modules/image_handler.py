# -*- coding: utf-8 -*-
"""Module to compute average RGB color of an image"""
import json
import logging
import os
import asyncio
import cv2
import numpy as np
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout
import constants as const

logging.getLogger().setLevel(
    getattr(logging, os.environ.get('LOG_LEVEL') or const.DEFAULT_LOG_LEVEL))


def get_average_color(image):
    """Get average color of a cv2 image

    Args:
        image (2D or 3D matrix): Loaded image

    Raises:
        IndexError if the image is corrupted

    Returns:
        list containing values for R, G, B channels
    """
    avg_color_per_row = np.mean(image, axis=0)
    avg_bgr_color = np.mean(avg_color_per_row, axis=0)  # RGB channels are reversed
    return avg_bgr_color.tolist()[::-1]


def remove_corrupted_img(path):
    """Removes corrupted image

        Args:
            path (str): Path to image

        """
    logging.error('Found corrupted image on path %s, removing', path)
    try:
        os.remove(path)
    except OSError:
        logging.error('Failed to remove corrupted %s', path)


async def run(loop):
    """Await new files and compute average color"""
    nats = NATS()
    await nats.connect(const.NATS_SERVER, loop=loop)

    async def callback(msg):
        reply = msg.reply
        filename = msg.data.decode()
        logging.info(' Received image path %s', filename)
        if os.path.isfile(filename):  # validate file path
            image = cv2.imread(filename)
            try:
                avg_color = get_average_color(image)
            except IndexError:
                remove_corrupted_img(filename)
                await nats.publish(reply, b'OK')
                return
            packet = {"avg_color": avg_color, "file_path": filename}
            json_packet = json.dumps(packet)
            try:
                logging.info('Sending average color for %s as %s', filename, avg_color)
                await nats.request("output", json_packet.encode(), 5)
            except ErrTimeout:
                logging.error('Image path %s timeout', filename)
            await nats.publish(reply, b'OK')

    await nats.subscribe("new-image", cb=callback)


if __name__ == "__main__":
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(run(LOOP))
    LOOP.run_forever()
