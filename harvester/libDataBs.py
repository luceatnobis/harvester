#!/usr/bin/env python3
import os
import sqlite3


# Simple sqlite wrapper
# Should be used with 'with' keyword to ensure proper initialization and closure of database

class DataBs:
    def __init__(self, archive_dir):
        harvester_db = os.path.join(archive_dir, "harvester.db")

        self.db = sqlite3.connect(harvester_db)
        self.curse = self.db.cursor()
        self.curse.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='harvs'")
        if not self.curse.fetchone():
            self.curse.execute("CREATE TABLE harvs(hash TEXT PRIMARY KEY, filename TEXT, count INTEGER)")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.db.commit()
        self.db.close()

    def checkHashExistence(self, hash):
        """Check if given hash is already in the database."""
        self.curse.execute("SELECT hash, filename, count FROM harvs WHERE hash = ?", [hash])
        if self.curse.fetchone():
            return True
        else:
            return False

    def insertData(self, dct):
        """Insert hash, filename and count into database."""
        if self.checkHashExistence(dct['hash']):
            return False
        else:
            self.curse.execute('''INSERT INTO harvs(hash, filename, count)
                VALUES(:hash,:filename, :count)''', dct)
            return True

    def upCount(self, hash):
        if not self.checkHashExistence(hash):
            return False
        else:
            self.curse.execute("UPDATE harvs SET count= count + 1 WHERE hash = ?", [hash])
            return True

    def gibData(self, hash):
        if not self.checkHashExistence(hash):
            return
        else:
            self.curse.execute("SELECT hash, filename, count FROM harvs WHERE hash=?", [hash])
            return [i for i in self.curse.fetchone()]
