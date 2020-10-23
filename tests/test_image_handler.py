# -*- coding: utf-8 -*-
"""Tests for image handler"""
import unittest
from io import BytesIO
from PIL import Image
import numpy as np
import cv2

import modules.image_handler as handler


def create_in_memory_image(image):
    in_memory_file = BytesIO()
    image.save(in_memory_file, 'png')
    in_memory_file.seek(0)
    file_bytes = np.asarray(bytearray(in_memory_file.read()), dtype=np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)


class TestGetAverageColor(unittest.TestCase):

    def test_single_color(self):
        color = (155, 0, 0)
        img = create_in_memory_image(Image.new('RGB', size=(10, 10), color=color))
        expected_result = [155.0, 0.0, 0.0]
        result = handler.get_average_color(img)
        self.assertEqual(result, expected_result)

    def test_half_black_half_white_expect_grey(self):
        canvas = Image.new('RGB', (100, 200), "white")
        black_rectangle = Image.new('RGB', (100, 100), "black")
        canvas.paste(black_rectangle, (0, 100))
        img = create_in_memory_image(canvas)
        expected_result = [127.5, 127.5, 127.5]  # grey (#7f7f7f)
        result = handler.get_average_color(img)
        self.assertEqual(result, expected_result)

    def test_half_yellow_half_red_expect_orange(self):
        canvas = Image.new('RGB', (100, 200), "red")
        yellow_rectangle = Image.new('RGB', (100, 100), "yellow")
        canvas.paste(yellow_rectangle, (0, 100))
        img = create_in_memory_image(canvas)
        expected_result = [255, 127.5, 0]  # orange (#ff7f00)
        result = handler.get_average_color(img)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()