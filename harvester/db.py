#!/usr/bin/env python3

import pdb
import sqlite3

from os import makedirs, symlink
from os.path import join, exists

from itertools import count
from collections import OrderedDict

from harvester import plugins
from harvester.utils import RowObj

class HarvesterDB:

    content_frag = '.content'
    tb_names = ["Harvester", "Collections"]
    harvester_fields = OrderedDict((
        ("site", "TEXT"),
        ("content_id", "TEXT"),
        ("content_url", "TEXT"),
        ("content_hash", "TEXT"),
        ("content_title", "TEXT"),
        ("content_timestamp", "TIMESTAMP"),
        ("original_url", "TEXT"),
        ("original_filename", "TEXT"),
        # ("original_extension", "TEXT"),
        ("archived_at", "TIMESTAMP"),
        ("stored_name", "TEXT"),
    ))

    collection_fields = OrderedDict((
        ("archived_at", "TIMESTAMP"),
        ("content_hash", "TIMESTAMP"),
        ("site", "TEXT"),
        ("collection_id", "TEXT"),
        ("collection_title", "TEXT"),
        ("content_id", "TEXT"),
    ))

    fields = {k: v for (k, v) in zip(
        tb_names, [harvester_fields, collection_fields])}

    def __init__(self, paths):

        self.paths = paths
        self.db = sqlite3.connect(
            self.paths.db_path,
            isolation_level=None,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        self.db.row_factory = self.__row_factory
        self.cursor = self.db.cursor()

        tb_list = [x.name for x in self._list_tables()]

        for tb in self.tb_names:
            if tb in tb_list:
                self._validate_table(tb)
            else:
                self._create_table(tb)

        for p in plugins.__all__:
            makedirs(join(self.paths.path_storage, p), exist_ok=True)

        self.content_base = join(self.paths.path_storage, self.content_frag)
        makedirs(self.content_base)

    def process_content(self, cc):
        sl_base = join(self.paths.path_storage, cc.return_path())
        makedirs(sl_base, exist_ok=True)

        for d in cc:
            res = self._content_in_db(d)
            link_path = join(sl_base, d['original_filename'])

            if not res:  # TODO: make this more elegant
                f_name = self._store_file_physically(d)
                content_path = join(self.content_base, f_name)
            elif d['content_hash'] in [x.content_hash for x in res]:
                found = self._get_collections_for_d(d)
                if found:  # we have the exact same object in the db
                    continue
                content_path = join(self.content_base, found[0].stored_name)

            symlink(content_path, link_path)
            self._insert_into_db("Harvester", d, f_name)
            self._insert_into_db("Collections", d)

    def _list_tables(self):
        return self.cursor.execute(
            "SELECT * FROM sqlite_master WHERE type='table'"
        ).fetchall()

    def _create_table(self, table_name):
        self.cursor.execute("CREATE TABLE {tbl} ({fields})".format(
            tbl=table_name, fields=", ".join(
                "%s %s" % (k, v) for k, v in self.fields[table_name].items())
            )
        )

    def _validate_table(self, tbl):
        res = self.cursor.execute(
            "PRAGMA TABLE_INFO('{tbl}')".format(tbl=tbl)).fetchall()
        for row, coded in zip(res, self.fields[tbl].items()):
            assert (row.name, row.type) == coded

    def _content_in_db(self, d):
        return self.cursor.execute(
            "SELECT * FROM Harvester WHERE content_hash = ?",
            (d['content_hash'],)
        ).fetchall()

    def _store_file_physically(self, d):
        fpath, fname = self._find_valid_filename(d)
        with open(fpath, 'wb') as f:
            f.write(d.content)
        return fname

    def _insert_into_db(self, tbl, d, f_name=None):
        if tbl == "Harvester":
            d['stored_name'] = f_name

        self.cursor.execute("INSERT INTO {tbl} VALUES ({q})".format(
                tbl=tbl, q=",".join(['?'] * len(self.fields[tbl].keys()))
            ), self._dict_helper(self.fields[tbl].keys(), d)
        )

    def _get_collections_for_d(self, d):
        return self.cursor.execute(
            "SELECT * FROM Collections WHERE site = ? AND content_id = ? "
            "AND collection_id = ?",
            (d['site'], d['content_id'], d['collection_id'])
        ).fetchall()

    def _find_valid_filename(self, d):
        t = str(int(d['archived_at'].timestamp()))

        _, ext = d['original_filename'].split('.', 1)
        ext = ext if ext else None
        fname = "{fname}.{ext}".format(fname=t, ext=ext)

        fpath = join(self.content_base, fname)

        for i in count():
            if not exists(fpath):
                return (fpath, fname )

            fname = "{f_name}_{i}.{ext}".format(
                f_name=t, ext=ext, i=i)
            fpath = join(self.content_base, fname)

    def _dict_helper(self, keys, d):
        s = []
        for k in keys:
            s.append(d[k])
        return s

    def __row_factory(self, cursor, row):
        f = None
        cursor_fields = {x[0] for x in cursor.description}
        fields = {x for x in dir(self) if x.endswith('_fields')}

        for x in fields:
            if not getattr(self, x).keys() == cursor_fields:
                continue
            f = getattr(self, x)
            break
        else:
            f = OrderedDict((f[0], None) for f in cursor.description)

        return RowObj(**{
            k: v for k, v in zip(f.keys(), row)})
