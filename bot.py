#!/usr/bin/env python3
# -+- coding: utf-8 -*-

import irc3

if __name__ == "__main__":
    config = irc3.utils.parse_config('bot', 'bot.ini')
    bot = irc3.IrcBot(**config)
    bot.include('irc3.plugins.logger')
    bot.include('harvester.harvester')
    bot.run()

urls = [
    'https://bpaste.net/show/426fe62985e3',
    'https://bpaste.net/raw/426fe62985e3',
    'http://cubeupload.com/im/YhUxlj.jpg',
    'http://i.cubeupload.com/YhUxlj.jpg',
    'http://dpaste.com/2E0H71M',
    'http://dpaste.com/2E0H71M.txt',
    'https://gyazo.com/fc12a9bb2a4b92d1debef49b8279371f',
    'https://i.gyazo.com/fc12a9bb2a4b92d1debef49b8279371f.png',
    'https://cache.gyazo.com/fc12a9bb2a4b92d1debef49b8279371f.png',
    'http://hastebin.com/vohayuzodu.vala',
    'http://hastebin.com/vohayuzodu',
    'http://hastebin.com/raw/vohayuzodu',
    'https://imgur.com/tNHwwYvf',
    'http://pastebin.com/Vcz07KuK',
    'http://pastebin.com/Vcz07KuK',
    'http://pastebin.com/raw/Vcz07KuK',
    'http://pastebin.com/raw.php?i=Vcz07KuK',
    'http://prntscr.com/5o2enp',
]
