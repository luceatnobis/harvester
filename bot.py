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
            harvest(mask, url, self.bot, target)

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
    bot.include('irc3.plugins.log')
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
