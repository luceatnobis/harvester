
import shutil
import tempfile
import unittest

from os import unlink
from os.path import exists

import irc3

from harvester.utils import PathHelper


class PathTest(unittest.TestCase):

    def setUp(self):
        _, tmp_conf_name = tempfile.mkstemp()
        self.tmp_archive_dir = tempfile.mkdtemp()

        with open(tmp_conf_name, 'w') as f:
            f.write("""[bot]
                py_path_bot_home = {home}""".format(home=self.tmp_archive_dir))

        self.config = irc3.utils.parse_config('bot', 'bot.ini', tmp_conf_name)
        unlink(tmp_conf_name)

    def test_path_creation(self):
        self.path = PathHelper(self.config)
        path_vars = list(
            filter(lambda x: x.startswith('path'), vars(self.path)))

        self.assertEquals(len(path_vars), 3)
        self.assertTrue(self.path.path_bot_home.is_dir())
        self.assertTrue(self.path.path_storage.is_dir())
        self.assertTrue(self.path.path_log.is_dir())

    def tearDown(self):
        shutil.rmtree(self.tmp_archive_dir)
