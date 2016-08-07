#!/usr/bin/env python3

import pdb
import sqlite3

from itertools import count
from collections import OrderedDict

from harvester import plugins
from harvester.utils import RowObj, CustomPath as Path


class HarvesterDB:

    content_frag = '.content'
    tb_names = ["Content", "Metadata", "Collections"]

    content_fields = OrderedDict((
        ("id", "INTEGER PRIMARY KEY"),
        ("content_hash", "TEXT"),
        ("stored_name", "TEXT"),
    ))

    metadata_fields = OrderedDict((
        ("archived_at", "INTEGER"),
        ("id", "INTEGER"),
        ("site", "TEXT"),
        ("content_id", "TEXT"),
        ("content_url", "TEXT"),
        ("content_title", "TEXT"),
        ("content_filename", "TEXT"),
        ("content_timestamp", "INTEGER"),
        ("original_url", "TEXT"),
        # ("original_filename", "TEXT"),
    ))

    collection_fields = OrderedDict((
        ("site", "TEXT"),
        ("id", "INTEGER"),
        ("collection_id", "TEXT"),
        ("collection_title", "TEXT"),
        ("content_id", "TEXT"),
        ("content_index", "TEXT"),
    ))

    fields = {k: v for (k, v) in zip(tb_names, [
        content_fields, metadata_fields, collection_fields]
    )}

    def __init__(self, paths):

        self.paths = paths
        self.cur_dir = str(Path().cwd())
        self.db = sqlite3.connect(
            str(self.paths.db_path),
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
            p = self.paths.path_storage / p
            if not p.is_dir():
                p.mkdir()

        self.content_base = Path(self.paths.path_storage, self.content_frag)
        self.content_base.mkdir()

    def process_content(self, cc):
        self.sl_base = Path(self.paths.path_storage, cc.return_path())
        if not self.sl_base.is_dir():
            self.sl_base.mkdir(parents=True)

        for d in cc:
            # pdb.set_trace()
            found = self._query_content_archived(d)
            if not found:  # its entirely new to us
                content_row = self._store_content(d)
            else:
                assert len(found) == 1
                content_row = found[0]
                d['id'] = content_row.id

            self._custom_symlink(d, content_row)

            metadata = self._query_metadata_for_id(content_row.id)
            matching_metadata = [x for x in metadata if x == d]

            if not matching_metadata:
                self._insert_metadata(d)

            if not d['collection']:
                continue

            collections = self._query_collections_for_id(content_row.id) 
            if not collections:
                self._insert_into_collections(d)
            # we have an id match but the details dont match
            elif not any([x for x in collections if x == d]):
                collection_row = collections[0]
                if d['content_index'] != collection_row.content_index:
                    self._insert_into_collections(d)
                else:
                    pdb.set_trace()
            # we have an id match and its identical to d so we do nothing

        del self.sl_base

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
        items = ((x, y.split(" ")[0]) for x, y in self.fields[tbl].items())
        for row, coded in zip(res, items):
            assert (row.name, row.type) == coded

    def _query_content_archived(self, d):
        return self.cursor.execute(
            "SELECT * FROM Content WHERE content_hash = ?",
            (d['content_hash'],)
        ).fetchall()

    def _store_content(self, d):
        content_path, name = self._store_file_physically(d)
        content_row = self._insert_into_content(d, name)[0]

        return content_row

    def _store_file_physically(self, d):
        fpath, fname = self._find_valid_filename(d)
        with fpath.open('wb') as f:
            f.write(d.content)
        return (fpath, fname)

    def _insert_into_content(self, d, f_name):
        d['stored_name'] = f_name

        self.cursor.execute("INSERT INTO Content VALUES ({q})".format(
            q=",".join(['?'] * len(self.fields["Content"].keys()))),
            [None] + self._dict_helper(self.fields["Content"].keys(), d)
        )

        # TODO: perhaps figure out how to spare 2nd request for row data

        id = self.cursor.lastrowid
        d['id'] = id

        return self.cursor.execute(
            "SELECT * FROM Content WHERE id = ?", (id, )
        ).fetchall()

    def _insert_into_db(self, tbl, d):
        self.cursor.execute("INSERT INTO {tbl} VALUES ({q})".format(
            tbl=tbl, q=",".join(['?'] * len(self.fields[tbl].keys()))),
            self._dict_helper(self.fields[tbl].keys(), d)
        )

    def _get_collections_for_d(self, d):
        return self.cursor.execute(
            "SELECT * FROM Collections WHERE site = ? AND content_id = ? "
            (d['site'], d['content_id'])
        ).fetchall()

    def _find_valid_filename(self, d):
        t = str(d['archived_at'])
        # orig_ext = d['original_extension']
        orig_ext = d['content_extension']

        filename_templates = {
            False: ("{fname}.{ext}", "{f_name}_{i}.{ext}"),
            True: ("{fname}", "{f_name}_{i}"),
        }
        fname_tmp, fname2_tmp = filename_templates[orig_ext is None]
        fname = fname_tmp.format(fname=t, ext=orig_ext)

        fpath = self.content_base / fname

        for i in count():
            if not fpath.exists():
                return (fpath, fname)

            fname = fname2_tmp.format(f_name=t, ext=orig_ext, i=i)
            fpath = self.content_base / fname

    def _query_metadata_for_id(self, id):
        return self.cursor.execute(
            "SELECT * FROM Metadata WHERE id = ? ",
            (id, )
        ).fetchall()

    def _insert_metadata(self, d):
        return self.cursor.execute(
            "INSERT INTO Metadata VALUES ({q})".format(
                q=",".join(['?'] * len(self.fields['Metadata'].keys()))
            ), self._dict_helper(self.fields["Metadata"].keys(), d)
        )

    def _custom_symlink(self, d, row):
        templates = {
            True: "{i}_{fname}", False: "{fname}",
        }
        sl_tmpl = templates[bool(d['collection'])]
        sl_name = sl_tmpl.format(
            # i=d['content_index'], fname=d['original_filename'])
            i=d['content_index'], fname=d['content_filename'])

        content_path = self.content_base / row.stored_name
        symlink_target = self.sl_base / sl_name

        relative_path = self._relative_path(symlink_target, content_path)

        if not symlink_target.is_symlink():
            symlink_target.symlink_to(relative_path)

    def _query_collections_for_id(self, id):
        return self.cursor.execute(
            "SELECT * FROM Collections WHERE id = ?", (id, )
        ).fetchall()

    def _insert_into_collections(self, d):
        return self.cursor.execute(
            "INSERT INTO Collections VALUES ({q})".format(
                q=",".join(['?'] * len(self.fields['Collections'].keys()))
            ), self._dict_helper(self.fields['Collections'].keys(), d)
        )


    def _dict_helper(self, keys, d):
        s = []
        for k in keys:
            if k not in d:
                continue
            s.append(d[k])
        return s

    def _relative_path(self, target, origin):
        for t, o, i in zip(target.parent.parts, origin.parent.parts, count()):
            if t == o:
                continue
            up = len(target.parent.parts) - i
            break
        return Path(*((['..'] * up) + list(origin.parts[i:])))

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
