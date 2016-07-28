#!/usr/bin/env python3

import hashlib
import unittest

from harvester import harvester
from harvester.plugins.pastebin import Pastebin


class PastebinTest(unittest.TestCase):

    def setUp(self):
        """
        self.nick = "test"
        self.chan = '#brotherBot'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.h = harvester.HarvesterBot
        """

    def test_fetch_regular(self):
        msg = "http://pastebin.com/Vcz07KuK"
        test_hash = "6f200af60b8ad355f7757b8f0e3efb00"

        klass = Pastebin(msg)
        klass.get_content()

    def test_fetch_new_raw(self):
        msg = "http://pastebin.com/raw/Vcz07KuK"
        test_hash = "6f200af60b8ad355f7757b8f0e3efb00"

        klass = Pastebin(msg)

    def test_fetch_old_raw(self):
        msg = "http://pastebin.com/raw.php?i=Vcz07KuK"
        test_hash = "6f200af60b8ad355f7757b8f0e3efb00"

        klass = Pastebin(msg)

if __name__ == '__main__':
    unittest.main()
