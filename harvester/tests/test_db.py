#!/usr/bin/env python3

import pdb
import shutil
import sqlite3
import unittest
import tempfile

from harvester.db import HarvesterDB
from harvester.tests.testutils import PathTestHelper as PathHelper


class BaseDBTest(unittest.TestCase):

    def setUp(self):
        self.test_tb = 'testtb'
        self.testfile_name = 'ayy.lmao'
        self.tempdir = tempfile.mkdtemp()

        HarvesterDB.tb_name = self.test_tb

    def _list_tables(self, db=None):
        if db is None:
            db = self.db.db

        cursor = db.cursor()
        return [x.timestamp for x in cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall()]

    def _list_columns(self, table, db=None):
        if db is None:
            db = self.db.db

        cursor = db.cursor()
        l = cursor.execute(
            "select * from {tb}".format(tb=table))
        return [x[0] for x in l.description]

    def _create_table(self, table, fields, db=None):
        s = (  # constructs the query string from fields
            "CREATE TABLE {tbname} (%s)" %
            ", ".join("%s %s" % (k, v) for (k, v) in fields.items())
        ).format(tbname=table)

        if db is None:
            db = self.db.db

        db.cursor().execute(s)
        db.commit()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

class PhysicalDBTest(BaseDBTest):

    def setUp(self):
        super().setUp()
        self.paths = PathHelper(self.tempdir, self.testfile_name)

    def test_db_create_physical(self):
        self.db = HarvesterDB(self.paths)

        for table in HarvesterDB.tb_names:
            tables = self.db._list_tables()
            self.assertTrue(table in tables)

            columns = self.db._list_columns(table)
            self.assertEquals(set(columns), set(HarvesterDB.fields[table]))

    def test_db_validate_valid_db(self):
        for table in HarvesterDB.tb_names:
            s = (  # constructs the valid query string from fields
                "CREATE TABLE {tbname} (%s)" % ", "\
                .join("%s TEXT" % k for k in HarvesterDB.fields[table].keys())
            ).format(tbname=self.test_tb)

        local_db = sqlite3.connect(self.paths.db_path)
        local_db.cursor().execute(s)
        local_db.commit()
        local_db.close()

        HarvesterDB(self.paths)

    def test_db_validate_invalid_db(self):
        for t in HarvesterDB.tb_names:
            local_db = sqlite3.connect(self.paths.db_path)

            self._create_table(t, {"lolwhat": "TEXT"}, local_db)
            local_db.close()

            with self.assertRaises(AssertionError):
                HarvesterDB(self.paths)


class MemoryDBTest(BaseDBTest):

    def setUp(self):
        super().setUp()

        self.paths = PathHelper(self.tempdir, ':memory:')

    def test_memory_creation(self):
        self.db = HarvesterDB(self.paths)

        for table in HarvesterDB.tb_names:
            tables = self._list_tables()
            self.assertTrue(table in tables)

            columns = self._list_columns(table)
            self.assertEquals(set(columns), set(HarvesterDB.fields[table]))

if __name__ == '__main__':
    unittest.main()
