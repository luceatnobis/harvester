#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pdb
import shutil
import unittest
import tempfile

from os.path import exists, join, dirname

from harvester import db


class HarvesterDBTest(unittest.TestCase):

    tempdir = tempfile.mkdtemp()

    def setUp(self):
        self.testfile_name = 'ayy.lmao'

    def tearDown(self):
        try:
            shutil.rmtree(self.tempdir)
        except:
            pass

    def test_db_create_on_raw_ne_folder(self):
        # we create on non-existent raw path, e.g. /foo/bar/
        shutil.rmtree(self.tempdir)
        h = db.HarvesterDB(self.tempdir)

        self.assertTrue(exists(dirname(h.db_path)))
        self.assertEquals(h.db_path, join(self.tempdir, "harvester.db"))

    def test_db_create_on_ne_path(self):
        # we create on non-existent path + filename, e.g. /for/bar/baz.db
        shutil.rmtree(self.tempdir)
        tempfolder = join(self.tempdir, self.testfile_name)
        h = db.HarvesterDB(tempfolder)

        self.assertEquals(h.db_name, self.testfile_name)
        self.assertTrue(exists(dirname(h.db_path)))

    def test_db_create_on_raw_path(self):
        # we create existent raw path, e.g. /for/bar/
        h = db.HarvesterDB(self.tempdir)

        self.assertEquals(dirname(h.db_path), self.tempdir)
        # self.assertEquals

if __name__ == '__main__':
    unittest.main()
