# -*- coding: utf-8 -*-
"""Tests for classifier"""
import unittest

import modules.classifier as classifier


class TestGetColorName(unittest.TestCase):
    """All colors tested against picked from extended Web colors"""

    def test_almost_black(self):
        result = classifier.get_color_name([0, 0, 1])  # black is 0, 0, 0
        expected_result = (None, "black")
        self.assertEqual(result, expected_result)

    def test_black(self):
        result = classifier.get_color_name([0, 0, 0])  # black is 0, 0, 0
        expected_result = ("black", "black")
        self.assertEqual(result, expected_result)

    def test_midnight_blue(self):
        result = classifier.get_color_name([25, 25, 112])  # navy is 0, 0, 128
        expected_result = (None, "navy")
        self.assertEqual(result, expected_result)

    def test_orange_red(self):
        result = classifier.get_color_name([255, 69, 0])  # red is 255, 0, 0
        expected_result = (None, "red")
        self.assertEqual(result, expected_result)

    def test_beige(self):
        result = classifier.get_color_name([245, 245, 220])  # white is 255, 255, 255
        expected_result = (None, "white")
        self.assertEqual(result, expected_result)

    def test_gold(self):
        result = classifier.get_color_name([255, 215, 0])  # yellow is 255, 255, 0
        expected_result = (None, "yellow")
        self.assertEqual(result, expected_result)

    def test_chocolate(self):
        result = classifier.get_color_name([210, 105, 30])  # olive is 128, 128, 0
        expected_result = (None, "olive")
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()