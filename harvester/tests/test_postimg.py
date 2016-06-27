#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import hashlib
import unittest

from harvester import harvester


class PostimgTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.chan = '#brotherBot'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.h = harvester.HarvesterBot

    def test_fetch_image_upload_page(self):
        # msg = "https://postimg.org/image/e68igfdqo/"
        msg = "https://postimg.org/image/ymd0wph53/"
        test_hash = "3c1a8ef650f3c3c3c2f4dd115931c0ca"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_image_page(self):
        msg = "https://postimg.org/image/85atjcr4h"
        test_hash = "3c1a8ef650f3c3c3c2f4dd115931c0ca"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)


    def test_fetch_image_link_download(self):
        msg = "https://s32.postimg.org/j4w0uyhjn/carlton.png"
        test_hash = "3c1a8ef650f3c3c3c2f4dd115931c0ca"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)


    def test_fetch_image_link_download_dl(self):
        msg = "https://s32.postimg.org/j4w0uyhjn/carlton.png?dl=1"
        test_hash = "3c1a8ef650f3c3c3c2f4dd115931c0ca"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)


    def test_fetch_gallery_long(self):
        msg = "https://postimg.org/gallery/380x4rxc2/1b59c905/"
        hashes = [
            "e94c07126688fa7a20c03653b67d3c81",
            "14b8cb4478b2150a3e2519e4d9337e5e",
            "ea46cc856dd9b9de3f47261c8a3bc8d9",
            "e0c645a8204e1836e039160718187371",
        ]

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        for i, h in enumerate(c):
            md5 = hashlib.md5()
            md5.update(h['content'])
            self.assertEqual(md5.hexdigest(), hashes[i])

    def test_fetch_gallery_short(self):
        msg = "https://postimg.org/gallery/380x4rxc2"
        hashes = [
            "e94c07126688fa7a20c03653b67d3c81",
            "14b8cb4478b2150a3e2519e4d9337e5e",
            "ea46cc856dd9b9de3f47261c8a3bc8d9",
            "e0c645a8204e1836e039160718187371",
        ]

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        for i, h in enumerate(c):
            md5 = hashlib.md5()
            md5.update(h['content'])
            self.assertEqual(md5.hexdigest(), hashes[i])

if __name__ == '__main__':
    unittest.main()
