#!/usr/bin/env python3

from os import sep
import unittest

from pathlib import Path
from harvester.utils import CustomPath

class CustomPathTest(unittest.TestCase):

    def test_multiple(self):
        c = CustomPath('hi', 'lol')
        self.assertEquals(str(c), sep.join(['hi', 'lol']))

    def test_path(self):
        ps = [Path(x) for x in ('hi', 'lol')]
        c = CustomPath(*ps)
        self.assertEquals(str(c), sep.join(['hi', 'lol']))

    def test_single(self):
        c = CustomPath('hi')
        self.assertEquals(str(c), 'hi')

if __name__ == "__main__":
    main()
