#!/usr/bin/env python3

import os
import pdb
import shutil
import unittest
import tempfile

import irc3
from irc3.testing import BotTestCase

from harvester import harvester
from harvester.tests import testutils

class PathTest(BotTestCase):

    def setUp(self):
        _, tmp_conf_name = tempfile.mkstemp()
        self.tmp_archive_dir = tempfile.mkdtemp()

        with open(tmp_conf_name, 'w') as f:
            f.write("[bot]\n"
                "py_path_bot_home = %s\n" % self.tmp_archive_dir
            )

        config = irc3.utils.parse_config('bot', 'bot.ini', tmp_conf_name)
        os.unlink(tmp_conf_name)

        self.bot = self.callFTU(**config)
        
    def test_create_path(self):
        # self.bot.include('harvester.tests.testutils')
        self.bot.include('harvester.harvester')

        pdb.set_trace()
        self.plugin = self.bot.get_plugin(
            # 'harvester.tests.testutils.HarvesterPathTest')
            'harvester.harvester.HarvesterBot')
        return
        self.plugin._create_paths()

    """
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_archive_dir, "archive")))
        self.assertTrue(os.path.exists(
            os.path.join(self.tmp_archive_dir, "logs")))

    """
    def tearDown(self):
        shutil.rmtree(self.tmp_archive_dir)

class BotTest(BotTestCase):

    """
    def setUp(self):
        self.nick = "padfoot"
        self.chan = '#chan'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"

        _, tmp_conf_name = tempfile.mkstemp()
        self.tmp_archive_dir = tempfile.mkdtemp()

        config = irc3.utils.parse_config('bot', 'bot.ini', tmp_conf_name)
        os.unlink(tmp_conf_name)

        self.bot = self.callFTU(**config)
        self.bot.include('harvester.tests.testutils')

        self.plugin = self.bot.get_plugin(
            'harvester.tests.testutils.HarvesterTest')
        
    def test_what(self):
        pass

    def tearDown(self):
        shutil.rmtree(self.tmp_archive_dir)
    """

if __name__ == '__main__':
    unittest.main()
