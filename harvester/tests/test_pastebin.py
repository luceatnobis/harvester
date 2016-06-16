#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import hashlib
import unittest

from harvester import harvester


class PastebinTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.chan = '#brotherBot'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.h = harvester.HarvesterBot

    def test_fetch_regular(self):
        msg = "http://pastebin.com/Vcz07KuK"
        test_hash = "6f200af60b8ad355f7757b8f0e3efb00"

        try:
            c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        except:
            pdb.post_mortem()

        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_new_raw(self):
        msg = "http://pastebin.com/raw/Vcz07KuK"
        test_hash = "6f200af60b8ad355f7757b8f0e3efb00"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)

        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_old(self):
        msg = "http://pastebin.com/raw.php?i=Vcz07KuK"
        test_hash = "6f200af60b8ad355f7757b8f0e3efb00"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)

        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

if __name__ == '__main__':
    unittest.main()
