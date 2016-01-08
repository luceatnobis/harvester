# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os


class CropKeeper(object):
    def __init__(self, bot):
        self.filename = os.path.join(*bot.config.log_filename)
        self.formatters = bot.config.log_formatters

    def __call__(self, event):
        filename = self.filename.format(**event)
        if not os.path.isfile(filename):
            dirname = os.path.dirname(filename)
            if not os.path.isdir(dirname):  # pragma: no cover
                os.makedirs(dirname)
        fmt = self.formatters.get(event['event'].lower())
        if fmt:
            with open(filename, 'a+') as fd:
                fd.write(fmt.format(**event) + '\r\n')
