# -*- coding: utf-8 -*-
"""Tests for parser"""
import unittest
from unittest.mock import patch

import modules.parser as parser


@patch('modules.parser.os.path.isdir')
@patch('modules.parser.os.walk')
class TestImagePaths(unittest.TestCase):

    def test_folder_with_two_images(self, walk_mock, path_mock):
        path_mock.return_value = True
        walk_mock.return_value = [["folder", None, ["img1.png", "img2.png"]]]
        expected_result = ["folder/img1.png", "folder/img2.png"]
        result = parser.get_image_paths("folder")
        self.assertEqual(result, expected_result)

    def test_folder_with_two_images_bad_ext(self, walk_mock, path_mock):
        path_mock.return_value = True
        walk_mock.return_value = [["folder", None, ["file.mp3", "file.avi"]]]
        expected_result = []
        result = parser.get_image_paths("folder")
        self.assertEqual(result, expected_result)

    def test_folder_with_two_images_missing_ext(self, walk_mock, path_mock):
        path_mock.return_value = True
        walk_mock.return_value = [["folder", None, ["file", "file2"]]]
        expected_result = []
        result = parser.get_image_paths("folder")
        self.assertEqual(result, expected_result)

    def test_empty_folder(self, walk_mock, path_mock):
        path_mock.return_value = True
        walk_mock.return_value = [["folder", None, []]]
        expected_result = []
        result = parser.get_image_paths("folder")
        self.assertEqual(result, expected_result)

    def test_folder_doesnt_exist(self, _, path_mock):
        path_mock.return_value = False
        expected_result = []
        result = parser.get_image_paths("folder")
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()