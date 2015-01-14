#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pdb
import json
import pkgutil
import unittest

from packages import httpretty
from packages import imgurpython

from bot import brotherBot
from harvester import imgur


class ImgurMatchTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"

        imgur_conf = json.loads(
            pkgutil.get_data('config', 'imgur.json').decode()
        )

        self.imgur_client = imgurpython.ImgurClient(
            imgur_conf['client_id'], imgur_conf['client_secret']
        )
        self.imgur_base_url = "https://imgur.com/"

        self.imgur_single_id= "AXhCKvD"
        self.imgur_single_url = (
                self.imgur_base_url + self.imgur_single_id)

        # note the lowercase d
        self.imgur_single_404_id = "AXhCKvd"
        self.imgur_single_404_url = (
            self.imgur_base_url + self.imgur_single_404_id)

        self.imgur_album_base_url = self.imgur_base_url + "a/"
        self.imgur_album_id = "zkfmT"
        self.imgur_album_url = self.imgur_album_base_url + self.imgur_album_id
        self.imgur_gallery = "https://imgur.com/gallery/WvaSV"

        self.my_bot = brotherBot(None)

    @httpretty.activate
    def test_match_single(self):
        pass
        # harvest_mod = self.my_bot.get_harvest_module(self.imgur_single_url)

    @httpretty.activate
    def test_harvest_single(self):
        file_name = self.imgur_single_id + ".png"
    """
        single_content = pkgutil.get_data(
            'tests.raw_data', file_name)
        httpretty.register_uri(
            httpretty.GET, self.imgur_single_url, body=single_content)

        response = imgur.load_single_image(
            self.imgur_client, self.imgur_single_id)
    """

    """
    def test_match_album(self):
        harvest_mod = self.my_bot.get_harvest_module(self.imgur_album_url)
        self.assertIs(imgur, harvest_mod)

    def test_match_gallery(self):
        harvest_mod = self.my_bot.get_harvest_module(self.imgur_album_url)
        self.assertIs(imgur, harvest_mod)
    """

if __name__ == '__main__':
    unittest.main()
