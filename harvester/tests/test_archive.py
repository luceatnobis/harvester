#!/usr/bin/env python3

import pdb
import tempfile
import unittest

from shutil import rmtree
from pathlib import Path
from harvester.utils import CustomPath
from datetime import datetime

from harvester.db import HarvesterDB
from harvester.tests.testutils import PathTestHelper as PathHelper

from harvester.plugins.imgur import Imgur
from harvester.plugins.hastebin import Hastebin
from harvester.plugins.pastebin import Pastebin 

class ContentArchiveBase(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.paths = PathHelper(self.tempdir, ':memory:')
        # self.paths = PathHelper(self.tempdir, 'endgame')
        self.db = HarvesterDB(self.paths)

        self.content_base = Path(self.paths.path_storage, '.content')

    def _retrieve_all_rows(self, tbl):
        return self.db.cursor.execute(
            "SELECT * FROM {tbl}".format(tbl=tbl)).fetchall()

    def tearDown(self):
        rmtree(self.tempdir)


class ImgurArchiveTest(ContentArchiveBase):

    def setUp(self):
        super().setUp()
        self.single = 'https://imgur.com/e1yYXUU'
        self.gallery = 'https://imgur.com/gallery/P7u9z'

        self.single_hash = "c2002691d4cd350aca016a982983ce0a"

    def test_imgur_single_archive(self):
        klass = Imgur(self.single)

        now = datetime.now()
        klass.archival_timestamp = now
        ts = int(now.timestamp())
        stored_name = str(ts) + ".jpg"

        self.db.process_content(klass)

        fname = Path(self.content_base, stored_name)

        self.assertTrue(fname.exists())
        self.assertFalse(fname.is_symlink())

        content_rows = self._retrieve_all_rows('Content')
        self.assertEquals(len(content_rows), 1)

        content_row = content_rows[0]
        self.assertEquals(content_row.content_hash, self.single_hash)
        self.assertEquals(content_row.stored_name, stored_name)

        metadata_rows = self._retrieve_all_rows('Metadata')
        self.assertEquals(len(metadata_rows), 1)

        metadata_row = metadata_rows[0]
        self.assertEquals(metadata_row.site, 'imgur')
        self.assertEquals(metadata_row.content_id, 'e1yYXUU')
        self.assertEquals(metadata_row.content_filename, 'e1yYXUU.jpg')
        self.assertEquals(metadata_row.archived_at, ts)

        collection_rows = self._retrieve_all_rows('Collections')
        self.assertEquals(len(collection_rows), 0)

    def test_imgur_single_duplicate(self):
        klass = Imgur(self.single)
        self.db.process_content(klass)

        # we duplicate inserting it
        self.db.process_content(klass)

        content_rows = self._retrieve_all_rows("Content")
        self.assertEquals(len(content_rows), 1)

    def test_imgur_gallery(self):
        data = (
            ('aFDjukM', 'b7caefeae792415b4570e5d0b6b633ea'),
            ('GDnuadf', 'e52bf7e50b68ecbdb2d34ec0f2bae9b2'),
            ('EUEJqpi', '14f7a5f391340444bfca381bcbfe0391'),
            ('tksJuZE', '940c32679c4b8d0f9144283dde90611e'),
        )
        klass = Imgur(self.gallery)
        self.db.process_content(klass)
        sl_base = Path(self.paths.path_storage, klass.return_path())

        content_rows = self._retrieve_all_rows("Content")
        metadata_rows = self._retrieve_all_rows("Metadata")
        collection_rows = self._retrieve_all_rows("Collections")
        self.assertEquals(klass.items, 4)

        for i in range(4):
            id, hash = data[i]
            sl_name = "{i}_{fname}.png".format(i=i+1, fname=id)
            self.assertEquals(content_rows[i].content_hash, hash)

            f_path = Path(sl_base, sl_name)
            self.assertTrue(f_path.exists())
            self.assertTrue(f_path.is_symlink())

            self.assertEquals(metadata_rows[i].content_id, id)
            self.assertEquals(collection_rows[i].content_id, id)

    def test_imgur_gallery_duplicate(self):
        klass = Imgur(self.gallery)
        self.db.process_content(klass)

        self.db.process_content(klass)
        row = self._retrieve_all_rows("Content")
        self.assertEquals(klass.items, 4)


class PastebinArchiveTest(ContentArchiveBase):

    def test_pastebin_archive(self):
        msg = "http://pastebin.com/Vcz07KuK"

        klass = Pastebin(msg)
        self.db.process_content(klass)
        # pdb.set_trace()

    def test_archive_differing_sources(self):
        pastebin_link = "http://pastebin.com/Vcz07KuK"
        hastebin_link = "http://hastebin.com/ihoyuxeret.hs"

        pb = Pastebin(pastebin_link)
        self.db.process_content(pb)

        hb = Hastebin(hastebin_link)
        self.db.process_content(hb)

if __name__ == '__main__':
    unittest.main()
