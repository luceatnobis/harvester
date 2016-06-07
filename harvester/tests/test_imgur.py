#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import hashlib
import unittest

from harvester import harvester


class ImgurTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.chan = '#brotherBot'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.h = harvester.HarvesterBot

    def test_fetch_imgur_share(self):
        msg = "https://imgur.com/e1yYXUU"
        test_hash = "c2002691d4cd350aca016a982983ce0a"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_imgur_image_no_i(self):
        msg = "https://imgur.com/e1yYXUU.jpg"
        test_hash = "c2002691d4cd350aca016a982983ce0a"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_imgur_raw_image(self):
        msg = "https://i.imgur.com/e1yYXUU.jpg"
        test_hash = "c2002691d4cd350aca016a982983ce0a"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_imgur_a(self):
        msg = "https://imgur.com/a/Tkx0P"
        hashes = [
            "037c2962e627cdfd347528445e383cd7",
            "98a6b2f27d27d712ff430ac980cbfb48",
            "8a4a37f78a1a3e593a61ab231ce93ed7",
            "c63ff1c939582db2023dd7bc49fd76be",
        ]

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        self.assertEqual(4, len(c))

        for c_hash in c:
            md5 = hashlib.md5()
            md5.update(c_hash['content'])
            self.assertTrue(md5.hexdigest() in hashes)

    def test_fetch_imgur_gallery(self):
        msg = "https://imgur.com/gallery/P7u9z"
        hashes = [
            "b7caefeae792415b4570e5d0b6b633ea",
            "e52bf7e50b68ecbdb2d34ec0f2bae9b2",
            "14f7a5f391340444bfca381bcbfe0391",
            "940c32679c4b8d0f9144283dde90611e",
        ]

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        self.assertEqual(4, len(c))

        for c_hash in c:
            md5 = hashlib.md5()
            md5.update(c_hash['content'])
            self.assertTrue(md5.hexdigest() in hashes)

if __name__ == '__main__':
    unittest.main()
