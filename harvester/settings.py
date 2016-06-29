#!/usr/bin/env python3
import os

from harvester import gyazo
from harvester import imgur
from harvester import puush
from harvester import bpaste
from harvester import dpaste
from harvester import anonyws
from harvester import sprunge
from harvester import anonmgr
from harvester import mixtape
from harvester import postimg
from harvester import prntscrn
from harvester import hastebin
from harvester import pastebin
from harvester import cubeupload


class Settings(object):
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def getSettings(cls):
        dct = {}
        for key, value in cls.__dict__.items():
            if not key.startswith('__') and not callable(key):
                dct[key] = value
        return dct

class HarvesterSettings(Settings):

    base_path = os.path.join(os.environ['HOME'], '.harvester')
    archive_path = os.path.join(base_path, 'archive')

    service_regex_dict = {
        "^https?://pastebin\.com/((raw\.php\?i=)|(raw/))?[A-Za-z0-9]+": pastebin.get_content,
        # those are unfortunately dead :( RIP
        # '^https?://p\.pomf\.se/[\d.]+': ppomf.get_content,
        # '^https?://(?:infotomb\.com|itmb\.co)/[0-9a-zA-Z.]+': infotomb.get_content,
        '^https?://prntscr\.com/[0-9a-zA-Z]+': prntscrn.get_content,
        # dpaste doesnt get along with https, so we're not gonna bother
        '^http://dpaste\.com/[0-9a-zA-Z]+(.txt)?': dpaste.get_content,
        '^https?://bpaste\.net/(raw|show)/[0-9a-zA-Z]+': bpaste.get_content,
        '^https?://hastebin.com/([a-z]+(\.[a-z]+)|(raw/[a-z]+)|([a-z]+))': hastebin.get_content,
        # '^https?://github.com/(.+)': github.get_content,
        '^http?://sprunge\.us/[a-zA-Z0-9.]{4,7}': sprunge.get_content,
        # here come the image hosters
        '^https?://anony\.ws/(.+)': anonyws.get_content,
        '^https?://puu\.sh/[A-Za-z0-9]{5}/(.+)': puush.get_content,
        # https://spit.mixtape.moe/view/58a37e21
        '^https?://(s\d+\.)?postimg\.org/(.+)': postimg.get_content,
        '^https?://anonmgur\.com/(.+)': anonmgr.get_content,
        '^https?://((my\.|spit\.)?)mixtape\.moe/(.+)': mixtape.get_content,
        '^https?://(i\.)?cubeupload\.com/(im/)?[a-zA-Z0-9.]+': cubeupload.get_content,
        '^https?://(cache\.|i\.)?gyazo.com/[a-z0-9]{32}(\.png)?': gyazo.get_content,
        '^https?://(i\.)?imgur\.com/(a/|gallery/)?[a-zA-Z0-9.,]+': imgur.get_content,
    }
