# -*- coding: utf-8 -*-
"""Module for scanning new unclassified images"""
import logging
import os
import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout
import constants as const

logging.getLogger().setLevel(
    getattr(logging, os.environ.get('LOG_LEVEL') or const.DEFAULT_LOG_LEVEL))


def get_image_paths(folder):
    """Get paths to each unclassified image, checks also sub-folders

    Args:
        folder (str): Path to folder

    Returns:
        list of image paths including folder
    """
    result = []
    if not os.path.isdir(folder):
        os.makedirs(folder)
    for root, _, files in os.walk(folder):
        for filename in files:
            # image format validation
            if filename.lower().endswith(const.SUPPORTED_IMAGES):
                result.append(os.path.join(root, filename))
    return result


async def run(loop):
    """Scan unclassified folder and notify subscribers of new images"""
    nats = NATS()
    await nats.connect(const.NATS_SERVER, loop=loop)

    while True:
        image_paths = get_image_paths(folder=const.IMAGES_FOLDER)
        for path in image_paths:
            try:
                logging.info('Sending image path %s', path)
                await nats.request("new-image", path.encode(), 5)
                logging.info('Processing of image on %s done', path)
            except ErrTimeout:
                logging.error('Image path %s timeout', path)

if __name__ == "__main__":
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(run(LOOP))
    LOOP.run_forever()
