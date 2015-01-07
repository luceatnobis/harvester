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

    def __init__(self, bot):
        self.bot = bot

    #TODO: gyazo, 
    #NOTE: https://irc3.readthedocs.org/en/latest/rfc.html
    @irc3.event(irc3.rfc.PRIVMSG)
    def privmsg_trigger(self, mask=None, event=None, target=None, data=None):
        if not all([mask, event, target, data]):
            raise Exception("shits fucked up yo")
        if target not in self.harvested_channels:
            return

        nick, user, host = self.split_mask(mask)
        url = self.urlReg(data)
        if url:
            content = self.harvest(nick, url)
    
    def urlReg(self,msg):
        m = re.match('^.*(https?://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?)',msg)
        if m:
            return m.group(1)
        return

    def harvest(self, nick, msg):
        archive_dir = os.environ['HOME'] + os.sep + "archive"
        archive_json = archive_dir + os.sep + "archive.json"

        timestamp = str(int(time.time() * 1000))
        paste_regex_to_func = {
                '^https?://pastebin\.com/(raw\.php\?i=)?[a-zA-Z0-9]+': pastebin.get_content,
            '^https?://p\.pomf\.se/[\d.]+': ppomf.get_content,
            '^https?://(?:infotomb\.com|itmb\.co)/[0-9a-zA-Z.]+': infotomb.get_content,
            '^https?://prntscr\.com/[0-9a-zA-Z]+': prntscrn.get_content,
            # dpaste doesnt get along with https, so we're not gonna bother
            '^http://dpaste\.com/[0-9a-zA-Z]+': dpaste.get_content,
            '^https?://bpaste\.net/(raw|show)/[0-9a-zA-Z]+': bpaste.get_content,
            '^https?://hastebin\.com/.+': hastebin.get_content,

            # here come the image hosters
            '^https?://(i\.)?cubeupload\.com/(im/)?[a-zA-Z0-9.]+': cubeupload.get_content,
            '^https?://(i\.)?imgur\.com/(gallery/)?[a-zA-Z0-9.]+': imgur.get_content,
            '^https?://(cache\.|i\.)?gyazo.com/[a-z0-9]{32}(\.png)?': gyazo.get_content
        }
        for regex, func in paste_regex_to_func.items():
            m = re.match(regex, msg)
            if not m:
                continue
            print(m.group(0))
            paste_data = func(m.group(0))

        # either no regex was found to match or no content could be pulled
        if not "paste_data" in locals() or paste_data is None:
                return

        paste_data['md5'] = hashlib.md5(paste_data['content']).hexdigest()
        paste_data['timestamp'] = timestamp
        final_folder = (
            archive_dir + os.sep + paste_data['site'])

        if not os.path.exists(final_folder):
            os.makedirs(final_folder)
        filename = str(timestamp) + "_" + paste_data['orig_filename']
        filename += ".%s" % paste_data['ext'] if paste_data['ext'] else ""

        file_location = final_folder + os.sep + filename
        paste_data['location'] = file_location
        
        with libDataBs.DataBs() as db:
            if not db.check(paste_data['md5']):
                #NOTE: THIS IS COMMENTED OUT FOR DEBUGGING PURPOSES
                with open(file_location, 'wb') as f:
                    f.write(paste_data['content'])
                db.set({'hash': paste_data['md5'], 'filename': filename, 'count': 1})
            else:
                #TODO add actions to take if file already in archive
                pass
        del paste_data['content']
        open(archive_json, 'a').close() #really obscure way to ensure that we always have a file to read from/to
        with open(archive_json, "r") as fj:
            try:
                dat = json.load(fj)
                dat.append(paste_data)
            except ValueError:
                dat = [paste_data]
        with open(archive_json, 'w+') as fj:
            json.dump(dat, fj)

        return True

    def split_mask(self, mask_raw):
        nick, _ = mask_raw.split('!')
        user, host = _.split('@')
        return (nick, user, host)


def main():

    bot = irc3.IrcBot(
        nick='joyTheRipper', autojoins=['#brotherBot'],
        host='irc.freenode.net', port=6697, ssl=True,
        includes=[
            'irc3.plugins.core',
            'irc3.plugins.command',
            'irc3.plugins.human',
            __name__,
        ]
    )
    bot.run()

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
