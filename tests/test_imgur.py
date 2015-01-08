#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import unittest

import bot
from harvester import imgur


class ImgurTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.imgur_single = (
            "'https://imgur.com/tNHwwYvf")

    def test_match_single(self):
        my_bot = bot.brotherBot(None)
        my_bot.privmsg_trigger(
            mask="brotherBox!~brotherBo@unaffiliated/brotherbox",
            event="PRIVMSG", target="#chan", data=self.imgur_single)

        # my_bot.harvest(self.nick, self.imgur_single)

if __name__ == '__main__':
    unittest.main()
