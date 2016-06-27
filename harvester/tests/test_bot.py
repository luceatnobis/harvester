#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import pdb
import irc3
import shutil
import unittest
import tempfile

from . import testing
from harvester import harvester


class BotTest(testing.BotTestCase):

    def setUp(self):
        self.nick = "padfoot"
        self.chan = '#chan'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"

        _, tmp_conf_name = tempfile.mkstemp()
        self.tmp_archive_dir = tempfile.mkdtemp()

        with open(tmp_conf_name, 'w') as f:
            f.write("[bot]\n"
                "py_path_bot_home = %s\n" % self.tmp_archive_dir
            )

        config = irc3.utils.parse_config('bot', 'bot.ini', tmp_conf_name)
        os.unlink(tmp_conf_name)

        self.bot = self.callFTU(**config)
        self.bot.include('harvester.harvester')

        self.plugin = self.bot.get_plugin('harvester.harvester.HarvesterBot')
        pdb.set_trace()

    def test_what(self):
        pass

    def tearDown(self):
        shutil.rmtree(self.tmp_archive_dir)

if __name__ == '__main__':
    unittest.main()
