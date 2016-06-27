#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pdb
import irc3
import sqlite3
import unittest

from . import testing
from harvester.plugins import *
from harvester import harvester


class DatabaseTest(testing.BotTestCase):

    def setUp(self):
        self.nick = "padfoot"
        self.chan = '#chan'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"

        config = irc3.utils.parse_config('bot', 'bot.ini')
        self.bot = self.callFTU(**config)
        self.bot.include('harvester.harvester')

        self.plugin = self.bot.get_plugin('harvester.harvester.HarvesterBot')
        self.plugin.db.close()

        self.plugin.db = sqlite3.connect(':memory:')

    def test_what(self):
        c = cubeupload.CubeUpload('http://cubeupload.com/im/YhUxlj.jpg')
        c.store_content()
        pdb.set_trace()
        for l in c:
            del l['content']
            print(l)

    def tearDown(self):
        self.plugin.db.close()

    def test_db(self):
        pass

if __name__ == '__main__':
    unittest.main()
