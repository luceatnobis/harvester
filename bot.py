#!/usr/bin/env python3
# -+- coding: utf-8 -*-

import os
import re
import time
import json
import hashlib

import irc3

from harvester import gyazo
from harvester import imgur
from harvester import ppomf
from harvester import bpaste
from harvester import dpaste
from harvester import infotomb
from harvester import prntscrn
from harvester import hastebin
from harvester import pastebin
from harvester import cubeupload

from harvester import libDataBs


@irc3.plugin
class brotherBot:

    requires = [
        'irc3.plugins.core',
        'irc3.plugins.userlist',
        'irc3.plugins.command',
        'irc3.plugins.human',
    ]
    harvested_channels = [
        '#brotherBot',
    ]
    paste_regex_to_mod = {
        '^https?://pastebin\.com/(raw\.php\?i=)?[a-zA-Z0-9]+': pastebin,
        '^https?://p\.pomf\.se/[\d.]+': ppomf,
        '^https?://(?:infotomb\.com|itmb\.co)/[0-9a-zA-Z.]+': infotomb,
        '^https?://prntscr\.com/[0-9a-zA-Z]+': prntscrn,
        # dpaste doesnt get along with https, so we're not gonna bother
        '^http://dpaste\.com/[0-9a-zA-Z]+': dpaste,
        '^https?://bpaste\.net/(raw|show)/[0-9a-zA-Z]+': bpaste,
        '^https?://hastebin\.com/(raw/[a-z]+)|([a-z]+\.hs)': hastebin,

        # here come the image hosters
        '^https?://(i\.)?cubeupload\.com/(im/)?[a-zA-Z0-9.]+': cubeupload,
        # '^https?://(i\.)?imgur\.com/(gallery/)?[a-zA-Z0-9.]+': imgur,
        '^https?://(i\.)?imgur\.com/(a/|gallery/)?[a-zA-Z0-9.]+': imgur,
        '^https?://(cache\.|i\.)?gyazo.com/[a-z0-9]{32}(\.png)?': gyazo
    }

    def __init__(self, bot):
        self.bot = bot

    #NOTE: https://irc3.readthedocs.org/en/latest/rfc.html
    @irc3.event(irc3.rfc.PRIVMSG)
    def privmsg_trigger(self, mask=None, event=None, target=None, data=None):
        if not all([mask, event, target, data]):
            raise Exception("shits fucked up yo")
        if target not in self.harvested_channels:
            return

        nick, user, host = self.split_mask(mask)

        for url in self.urlReg(data):
            self.harvest(nick, url)

    def urlReg(self, url):
        m = re.findall('(https?://[^\s]+)', url)
        return m

    def harvest(self, nick, url):
        # for more correlation between logs and timestamps, generate it here
        timestamp = str(int(time.time() * 1000))

        paste_info = self.paste_url_to_json(url)
        paste_info['timestamp'] = timestamp

    def paste_url_to_json(self, url):
        paste_module = self.get_harvest_module(url)
        if paste_module is None:
            return

        paste_data = paste_module.get_content(url)

        # either no regex was found to match or no content could be pulled
        if not "paste_data" in locals() or paste_data is None:
                return

        paste_data = self.hash_content(paste_data)
        return paste_data

    def store_paste(self, paste_data):
        archive_dir = os.path.join(os.environ['HOME'], "archive")
        archive_json = os.path.join(archive_dir, "archive.json")

        final_folder = (
            archive_dir + os.sep + paste_data['site'])

        if not os.path.exists(final_folder):
            os.makedirs(final_folder)

        filename = "%s_%s" % (
            paste_data['timestamp'], paste_data['orig_filename'])
        filename += ".%s" % paste_data['ext'] if paste_data['ext'] else ""

        file_location = final_folder + os.sep + filename
        paste_data['location'] = file_location

        return

        with libDataBs.DataBs() as db:
            print(db.gibData(paste_data['md5']))
            if not db.check(paste_data['md5']):
                with open(file_location, 'wb') as f:
                    f.write(paste_data['content'])
                db.set({
                    'hash': paste_data['md5'],
                    'filename': filename,
                    'count': 1
                })
            else:
                db.upCount(paste_data['md5'])
        del paste_data['content']

        #obscure way to ensure that we always have a file to read from/to
        open(archive_json, 'a').close()
        with open(archive_json, "r") as fj:
            try:
                dat = json.load(fj)
                dat.append(paste_data)
            except ValueError:
                dat = [paste_data]
        with open(archive_json, 'w+') as fj:
            json.dump(dat, fj)

        return True

    def hash_content(self, paste_data):
        if 'type' not in paste_data:  # we assume the content is not a gallery
            paste_data['md5'] = hashlib.md5(paste_data['content']).hexdigest()
            return paste_data

    def split_mask(self, mask_raw):
        nick, _ = mask_raw.split('!')
        user, host = _.split('@')
        return (nick, user, host)

    def get_harvest_module(self, url):
        """
        We operate under the assumption that only one regex can match a link.
        If this ever changes we really do have a problem.
        """
        for regex, mod in self.paste_regex_to_mod.items():
            m = re.match(regex, url)
            if m:
                return mod

def main():

    bot = irc3.IrcBot(
        nick='brotherBot', autojoins=['#brotherBot'],
        host='irc.freenode.net', port=6697, ssl=True,
        includes=[
            'irc3.plugins.core',
            'irc3.plugins.command',
            'irc3.plugins.human',
            __name__,
        ]
    )
    bot.include('irc3.plugins.log')
    bot.run()

if __name__ == "__main__":
    main()

"""
urls = [
    'http://gyazo.com/fc12a9bb2a4b92d1debef49b8279371f',
    'http://i.gyazo.com/fc12a9bb2a4b92d1debef49b8279371f.png',
    'https://cache.gyazo.com/fc12a9bb2a4b92d1debef49b8279371f.png',
    'http://i.imgur.com/aChgMdG.gif',
    'http://hastebin.com/zebihupixo.hs',
    'http://hastebin.com/raw/zebihupixo',
    'https://bpaste.net/show/31f01443d2b1',
    'http://dpaste.com/03N0Y7Z',
    'http://p.pomf.se/5504',
    'http://pastebin.com/raw.php?i=gpRREVYd',
    'http://prntscr.com/5o2enp',
    'https://infotomb.com/y53jc',
]
"""
