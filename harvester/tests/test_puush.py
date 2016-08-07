#!/usr/bin/env python3

import hashlib
import unittest

'''
from harvester import harvester


class PuushTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.chan = '#brotherBot'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.h = harvester.HarvesterBot

    def test_fetch_puush(self):
        msg = "https://puu.sh/pu4Wu/2f117848e3.png"
        test_hash = "3b74a82e6d0456756a2ed1623e6f6e34"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)
'''

if __name__ == '__main__':
    unittest.main()
