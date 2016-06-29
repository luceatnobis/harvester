#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pdb
import irc3
import sqlite3
import unittest

from harvester import harvester
from harvester.tests.testutils import HarvesterTest, BotTestCase
# from harvester.plugins import *


class DatabaseTest(BotTestCase):

    def setUp(self):

        config = irc3.utils.parse_config('bot', 'bot.ini')
        self.bot = self.callFTU(**config)

        self.bot.include('harvester.tests.testutils')

        """
        self.plugin = self.bot.get_plugin(
            'harvester.tests.testutils.HarvesterTest')
        self.plugin.db.close()

        self.plugin.db = sqlite3.connect(':memory:')
        """

    def test_what(self):
        pass
        """
        c = cubeupload.CubeUpload('http://cubeupload.com/im/YhUxlj.jpg')
        c.store_content()
        pdb.set_trace()
        for l in c:
            del l['content']
            print(l)
        """

    """
    def tearDown(self):
        self.plugin.db.close()
    """

if __name__ == '__main__':
    unittest.main()
