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
        ("path", "TEXT"),
    ))

    """
    collection_fields = OrderedDict((
        ("site", "TEXT"),
        ("collection_id", "TEXT"),
        ("collection_title", "TEXT"),
        ("nr_items", "INTEGER"),
    ))
    """

    fields = {k: v for (k, v) in zip(
        tb_names, [harvester_fields])}
        # tb_names, [harvester_fields, collection_fields])}

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

    def __row_factory(self, cursor, row):
        cursor_fields = {x[0] for x in cursor.description}
        fields = {x for x in dir(self) if x.endswith('_fields')}
        
        f = [x for x in fields if getattr(self, x).keys() == cursor_fields][0]
        f = getattr(self, f)
        return RowObj(**{
            k: v for k, v in zip(f.keys(), row)})
