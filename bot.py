#!/usr/bin/env python3
# -+- coding: utf-8 -*-

import irc3
from harvester.settings import BotSettings
#  from harvester.utils import urlReg, harvest

if __name__ == "__main__":
    settings = BotSettings.getSettings()
    logger = {
        'irc3.plugins.logger': {
            'handler': 'harvester.logger.CropKeeper'
        }
    }
    settings.update(logger)
    bot = irc3.IrcBot(**(settings))
    bot.include('irc3.plugins.logger')
    bot.include('harvester.harvester')
    bot.run()

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
