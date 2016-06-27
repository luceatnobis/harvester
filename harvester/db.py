#!/usr/bin/env python3
import os
import pdb
import sqlite3


class HarvesterDB:

    db_name = "harvester.db"

    def __init__(self, db_path):
        self._correct_path(db_path)
        return
        
    def _correct_path(self, db_path):
        if os.path.exists(db_path):
            pdb.set_trace()
            if os.path.isdir(db_path):
                db_path = os.path.join(db_path, self.db_name)
            self.db_path = db_path
        else:
            if "." in os.path.basename(db_path):
                self.db_name = os.path.basename(db_path)
                self.db_path = db_path
            else:
                self.db_path = os.path.join(db_path, self.db_name)
            os.makedirs(os.path.dirname(self.db_path))


    def process_content(self):
        pass
