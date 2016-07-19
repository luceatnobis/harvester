#!/usr/bin/env python3

import pdb
import sqlite3
import tempfile
import unittest

from shutil import rmtree
from os.path import exists, join

from harvester.plugins import *
from harvester.db import HarvesterDB
from harvester.tests.testutils import PathTestHelper as PathHelper

class ContentArchiveBase(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.paths = PathHelper(self.tempdir, ':memory:')
        self.db = HarvesterDB(self.paths)

    def _retrieve_all_rows(self):
        return self.db.cursor.execute("SELECT * FROM Harvester").fetchall()

    def tearDown(self):
        rmtree(self.tempdir)

class ImgurArchiveTest(ContentArchiveBase):

    def setUp(self):
        super().setUp()
        self.single = 'https://imgur.com/e1yYXUU'
        self.gallery = 'https://imgur.com/gallery/P7u9z'

        self.single_hash = "c2002691d4cd350aca016a982983ce0a"

    def test_imgur_single_archive(self):
        klass = imgur.Imgur(self.single)
        self.db.process_content(klass)

        rows = self._retrieve_all_rows()
        self.assertEquals(len(rows), 1)

        row = rows[0]
        self.assertEquals(row.collection_id, None)
        self.assertEquals(row.content_id, "e1yYXUU")
        self.assertEquals(row.content_hash, self.single_hash)

        self.assertTrue(
            exists(join(self.paths.path_storage, "imgur", "e1yYXUU.jpg")))

    def test_imgur_single_duplicate(self):
        klass = imgur.Imgur(self.single)
        self.db.process_content(klass)

        # we duplicate inserting it
        self.db.process_content(klass)

        rows = self._retrieve_all_rows()
        self.assertEquals(len(rows), 1)

        row = rows[0]
        self.assertEquals(row.collection_id, None)
        self.assertEquals(row.content_id, "e1yYXUU")
        self.assertEquals(row.content_hash, self.single_hash)


    def test_imgur_gallery(self):
        klass = imgur.Imgur(self.gallery)
        self.db.process_content(klass)


    def test_imgur_gallery_duplicate(self):
        klass = imgur.Imgur(self.gallery)
        self.db.process_content(klass)

        self.db.process_content(klass)

if __name__ == '__main__':
    unittest.main()
