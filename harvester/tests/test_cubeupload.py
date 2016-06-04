#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pdb
import hashlib
import unittest

from harvester import harvester


class CupeuploadTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.chan = '#brotherBot'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.h = harvester.HarvesterBot

    def test_fetch_cubeupload_share(self):
        msg = "http://cubeupload.com/im/YhUxlj.jpg"
        test_hash = "3c1a8ef650f3c3c3c2f4dd115931c0ca"
        
        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_cubeupload_raw(self):
        msg = "http://i.cubeupload.com/YhUxlj.jpg"
        test_hash = "3c1a8ef650f3c3c3c2f4dd115931c0ca"
        
        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

if __name__ == '__main__':
    unittest.main()
