#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import unittest
from unittest.mock import patch

import bot
from harvester import imgur


class ImgurTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.imgur_single = "https://imgur.com/AXhCKvD"
        self.imgur_single_404 = "https://imgur.com/AXhCKvd"
        self.imgur_album = "https://imgur.com/a/zkfmT"
        self.imgur_gallery = "https://imgur.com/gallery/WvaSV"

        self.my_bot = bot.brotherBot(None)

    def test_match_single(self):
        harvest_mod = self.my_bot.get_harvest_module(self.imgur_single)
        self.assertIs(imgur, harvest_mod)

    def test_harvest_single(self):
        paste_data = self.my_bot.paste_url_to_json(self.imgur_single)

    def test_match_album(self):
        harvest_mod = self.my_bot.get_harvest_module(self.imgur_album)
        self.assertIs(imgur, harvest_mod)

    def test_match_gallery(self):
        harvest_mod = self.my_bot.get_harvest_module(self.imgur_album)
        self.assertIs(imgur, harvest_mod)

if __name__ == '__main__':
    unittest.main()
