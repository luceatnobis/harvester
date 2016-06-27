#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import unittest

from . import testing
from harvester import harvester


class CubeuploadTest(testing.BotTestCase):

    def setUp(self):

        self.nick = "padfoot"
        self.chan = '#chan'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.hash = "3c1a8ef650f3c3c3c2f4dd115931c0ca"
        self.filename = "YhUxlj.jpg"

        self.h = harvester.HarvesterBot

    def test_fetch_cubeupload_share(self):
        link = "http://cubeupload.com/im/YhUxlj.jpg"

        c = self.h._retrieve_content(self.h, self.mask, link, self.chan)

        c.store_content()

        self.assertEquals(c.items, 1)
        self.assertIsNone(c.collection)
        self.assertEquals(c.filename, self.filename)
        self.assertEqual(c.hashes[0], self.hash)

    def test_fetch_cubeupload_raw(self):
        link = "http://i.cubeupload.com/YhUxlj.jpg"

        c = self.h._retrieve_content(self.h, self.mask, link, self.chan)
        c.store_content()

        self.assertEquals(c.items, 1)
        self.assertIsNone(c.collection)
        self.assertEquals(c.filename, self.filename)
        self.assertEqual(c.hashes[0], self.hash)

if __name__ == '__main__':
    unittest.main()
