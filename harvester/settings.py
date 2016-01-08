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
from os import environ


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


class BotSettings(Settings):
    nick = 'boringBot'
    host = 'irc.freenode.net'
    port = 6697
    ssl = True

    includes = [
        'irc3.plugins.core',
        'irc3.plugins.command',
        'irc3.plugins.human',
        '__main__'
    ]

    autojoins = [
        '#brotherBot'
    ]

    log_formatters = {
        'privmsg': '{date:%Y-%m-%d %H:%M} <{mask.nick}> {data}',
        'join': '{date:%Y-%m-%d %H:%M} {mask.nick} joined {channel}',
        'part': '{date:%Y-%m-%d %H:%M} {mask.nick} has left {channel} ({data})',
        'quit': '{date:%Y-%m-%d %H:%M} {mask.nick} has quit ({data})',
        'topic': '{date:%Y-%m-%d %H:%M} {mask.nick} has set topic to: {data}',
    }

    log_filename = [environ['HOME'], 'archive', 'logs', '{host}',
                    '{channel}-{date:%Y-%m-%d}.log']


class HarvesterSettings(Settings):

    harvested_channels = [
        '#brotherBot'
    ]

    archive_path = [environ['HOME'], 'archive']
    service_regex_dict = {
        '^https?://pastebin\.com/(raw\.php\?i=)?[a-zA-Z0-9]+': pastebin.get_content,
        '^https?://p\.pomf\.se/[\d.]+': ppomf.get_content,
        '^https?://(?:infotomb\.com|itmb\.co)/[0-9a-zA-Z.]+': infotomb.get_content,
        '^https?://prntscr\.com/[0-9a-zA-Z]+': prntscrn.get_content,
        # dpaste doesnt get along with https, so we're not gonna bother
        '^http://dpaste\.com/[0-9a-zA-Z]+': dpaste.get_content,
        '^https?://bpaste\.net/(raw|show)/[0-9a-zA-Z]+': bpaste.get_content,
        '^https?://hastebin\.com/(raw/[a-z]+)|([a-z]+\.hs)': hastebin.get_content,
        # here come the image hosters
        '^https?://(i\.)?cubeupload\.com/(im/)?[a-zA-Z0-9.]+': cubeupload.get_content,
        '^https?://(i\.)?imgur\.com/(gallery/)?[a-zA-Z0-9.,]+': imgur.get_content,
        '^https?://(cache\.|i\.)?gyazo.com/[a-z0-9]{32}(\.png)?': gyazo.get_content
    }
