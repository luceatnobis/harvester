#!/usr/bin/env python3

import pdb
import unittest

from harvester.plugins.sprunge import Sprunge


class SprungeTest(unittest.TestCase):

    ctrl_dict = {
        'site': 'sprunge',
        'content_id': 'VShH',
        'content_timestamp': 0,
        'content_hash':  'ad39ad4ac1910e2efd85682c04dcd8f9',
    }

    def test_fetch_sprunge(self):
        msg = "http://sprunge.us/VShH"

        s = Sprunge(msg)
        l = list(s)
        self.assertEquals(len(l), 1)

        d = l[0]
        for k, v in self.ctrl_dict.items():
            self.assertEquals(d[k], v)

    def test_fetch_sprunge_404(self):
        msg = "http://sprunge.us/thisIDislikelytoneverexist"

        s = Sprunge(msg)
        l = list(s)
        self.assertEquals(len(l), 0)

if __name__ == '__main__':
    unittest.main()
