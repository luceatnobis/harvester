#!/usr/bin/env python3

import pdb
import irc3
import shutil

from os.path import join

from harvester.utils import PathHelper
# from harvester.harvester import HarvesterBot


class PathTestHelper(PathHelper):
    def __init__(self, folder_name, db_name=":memory:"):

        if db_name != ":memory:":
            db_name = join(folder_name, 'archive', db_name)

        paths_tmpl = {
            'py_path_bot_home': folder_name,
            'py_path_storage': join(folder_name, 'archive'),
            'py_path_log': join(folder_name, 'logs'),
            'py_db_path': db_name
        }

        super().__init__(paths_tmpl)

"""
@irc3.plugin
class HarvesterTest(HarvesterBot):

    def __init__(self, bot):
        self.bot = bot

    def _create_paths(self):  # in test cases, we dont want to create paths
        pass


@irc3.plugin
class HarvesterPathTest(HarvesterBot):

    def __init__(self, bot):
        self.bot = bot
        self._set_config_vars()
"""
