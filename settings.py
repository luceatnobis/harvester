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
from harvester.utils import urlReg, harvest
from os import environ
import irc3


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
        __name__,
    ]

    autojoins = [
        '#brotherBot'
    ]


class HarvesterSettings(Settings):

    harvested_channels = [
        '#brotherBot'
    ]

    path = [environ['HOME'], 'archive']
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


@irc3.plugin
class brotherBot:
    requires = [
        'irc3.plugins.core',
        'irc3.plugins.userlist',
        'irc3.plugins.command',
        'irc3.plugins.human',
    ]

    def __init__(self, bot):
        print("hello")
        self.bot = bot

    #NOTE: https://irc3.readthedocs.org/en/latest/rfc.html
    @irc3.event(irc3.rfc.PRIVMSG)
    def privmsg_trigger(self, mask=None, event=None, target=None, data=None):
        if not all([mask, event, target, data]):
            raise Exception("shits fucked up yo")
        if target not in HarvesterSettings.harvested_channels:
            return

        nick, user, host = self.split_mask(mask)
        url = urlReg(data)
        if url:
            harvest(mask, url, self.bot, target, HarvesterSettings())

    def split_mask(self, mask_raw):
        nick, _ = mask_raw.split('!')
        user, host = _.split('@')
        return (nick, user, host)

    @irc3.event(irc3.rfc.JOIN)
    def myevent(self, mask=None, event=None, target=None, data=None, channel=None):
        self.bot.privmsg(channel, "All of your links belong to me! (As long as you use proper sites)")
