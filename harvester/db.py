#!/usr/bin/env python3

import pdb
import sqlite3

from os import makedirs
from os.path import join, exists, isfile

from collections import OrderedDict

from harvester import plugins
from harvester.utils import RowObj

class HarvesterDB:

    tb_names = ["Harvester", "Collections"]
    harvester_fields = OrderedDict((
        ("timestamp", "TIMESTAMP"),
        ("site", "TEXT"),
        ("collection_id", "TEXT"),
        ("content_id", "TEXT"),
        ("content_url", "TEXT"),
        ("content_hash", "TEXT"),
        ("content_title", "TEXT"),
        ("original_url", "TEXT"),
        ("original_filename", "TEXT"),
        ("original_extension", "TEXT"),
    ))

    collection_fields = OrderedDict((
        ("site", "TEXT"),
        ("collection_id", "TEXT"),
        ("collection_title", "TEXT"),
        ("nr_items", "INTEGER"),
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

        tb_list = self._list_tables()

        for tb in self.tb_names:
            if tb in tb_list:
                self._validate_table(tb)
            else:
                self._create_table(tb)

        for p in plugins.__all__:
            plugin_folder = join(self.paths.path_storage, p)
            if not exists(plugin_folder):
                makedirs(plugin_folder)

            site_listing = join(self.paths.path_storage, p, p + '.txt')
            if not isfile(site_listing):
                with open(site_listing, 'w') as f:
                    f.write(p + ':\n\n')

    def _list_tables(self):
        # x.timestamp is the table name haha what
        return [x.timestamp for x in self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall()]

    def _create_table(self, table):
        f = self.fields[table]
        s = (  # constructs the query string from fields
            "CREATE TABLE {tbname} (%s)" %
            ", ".join("%s %s" % (k, v) for (k, v) in f.items())
        ).format(tbname=table)

        self.cursor.execute(s)
        self.db.commit()

    def _validate_table(self, table):
        columns = self._list_columns(table)
        assert set(columns) == set(self.fields[table].keys())

    def _list_columns(self, table):
        l = self.cursor.execute(
            "select * from {tb}".format(tb=table))
        return [x[0] for x in l.description]

    def process_content(self, content_class):
        if content_class.collection is None:
            self._process_non_collection(content_class)
        else:
            self._process_gallery(content_class)

    def _process_gallery(self, cc):
        results = self._retrieve_collection_results(cc)

        if not results:
            self._insert_collection(cc)
            self._store_gallery(cc)
        else:
            

    def _store_gallery(self, cc):
        for d in cc:
            self._insert_single_metadata(d)
            self._store_physical(d)

    def _retrieve_collection_results(self, cc):
        l = self.cursor.execute(
            "SELECT * FROM Collections WHERE site=? AND collection_id=?",
            (cc.site, cc.collection)
        ).fetchall()
        return l

    def _process_non_collection(self, cc):
        for d in cc:
            if self._check_single_in_db(d):
                continue
            self._insert_single_metadata(d)
            self._store_physical(d)

    def _check_single_in_db(self, d):
        self.db.commit()
        results = self.cursor.execute(
            "SELECT * FROM Harvester WHERE site=:site AND "
            "content_id=:content_id AND content_hash=:content_hash", (d)
        ).fetchall()
        return bool(results)

    def _check_collection_in_db(self, cc):
        results = self.cursor.execute(
            "SELECT * FROM Collections WHERE site=? AND collection=?",
            (cc.collection,)
        ).fetchall()
        return results
    
    def _insert_collection(self, cc):
        self.cursor.execute(
            "INSERT INTO Collections VALUES (?,?,?,?)",
            (cc.site, cc.collection, cc.collection_title, cc.items)
        )

    def _insert_single_metadata(self, d):
        s = "INSERT INTO Harvester VALUES (?,?,?,?,?,?,?,?,?,?)"
        self.cursor.execute(s, list(d.values()))
        self.db.commit()

    def _store_physical(self, d):
        file_path = join(self.paths.path_storage, d.path)
        listing_filename = (
            (d['collection'] if d['collection'] else d['site']) + '.txt'
        )

        full_file_path = join(file_path, d['original_filename'])

        full_listing_path = join(
            self.paths.path_storage, d.path, listing_filename)

        if not exists(file_path):
            makedirs(file_path, exist_ok=True)

        info_str = "%s %s\n" % (
            d['original_filename'], d['content_hash'])

        with open(full_listing_path, 'a') as f:
            f.write(info_str)

        with open(full_file_path, 'wb') as f:
            f.write(d.content)

        return True

    def __row_factory(self, cursor, row):
        cursor_fields = {x[0] for x in cursor.description}
        fields = {x for x in dir(self) if x.endswith('_fields')}
        
        f = [x for x in fields if getattr(self, x).keys() == cursor_fields][0]
        f = getattr(self, f)
        return RowObj(**{
            k: v for k, v in zip(f.keys(), row)})

    def __del__(self):
        self.db.close()
