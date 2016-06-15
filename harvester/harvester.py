import os
import re
import irc3
import time

from irc3.plugins.command import command
from harvester.settings import HarvesterSettings
from harvester.utils import urlReg, save


@irc3.plugin
class HarvesterBot(HarvesterSettings):
    requires = [
        'irc3.plugins.core',
        'irc3.plugins.userlist',
        'irc3.plugins.command',
    ]

    def __init__(self, bot):
        self.bot = bot

    #NOTE: https://irc3.readthedocs.org/en/latest/rfc.html
    @irc3.event(irc3.rfc.PRIVMSG)
    def privmsg_trigger(self, mask=None, event=None, target=None, data=None):
        if not all([mask, event, target, data]):
            raise Exception("shits fucked up yo")
        if target not in self.bot.config['harvested_channels']:
            return

        nick, user, host = self.split_mask(mask)
        url = urlReg(data)
        if url:
            self.harvest(mask, url, target)

    def split_mask(self, mask_raw):
        nick, _ = mask_raw.split('!')
        user, host = _.split('@')
        return (nick, user, host)

    @irc3.event(irc3.rfc.JOIN)
    def myevent(
            self, mask=None, event=None, target=None, data=None, channel=None):
        if mask.nick == self.bot.nick:
            self.bot.privmsg(
                channel, "All your links are belong to us! "
                "(As long as you use proper sites)")

    @command
    def quit(self, mask, event, target):
        """quit command

            %%quit
        """
        self.bot.SIGINT()

    @irc3.event(
        r'(@(?P<tags>\S+) )?:(?P<ns>NickServ)!NickServ@services.'
        r' NOTICE (?P<nick>harvester) :This nickname is registered.*'
    )
    def register(self, ns=None, nick=None, **kw):
        np_path = os.path.join(
            os.environ['HOME'], '.harvester', 'nickserv_pass')
        with open(np_path) as f:
            p = f.read().rstrip()
        self.bot.privmsg(ns, 'identify %s %s' % (nick, p))

    def harvest(self, mask, msg, chan):
        timestamp = str(int(time.time() * 1000))
        paste_data = self._retrieve_content(mask, msg, chan)

        if paste_data is None:
            return

        filenames = self._archive(paste_data, timestamp, chan, mask)
        self.bot.privmsg(
            chan, "^ Archived file(s): {} ^".format(" ".join(filenames)))

    def _retrieve_content(self, mask, msg, chan):
        """Try to harvest given url and save the file."""
        # NOTE site harvesters should return a list of dictionaries, even if
        # only one file has been gathered
        # try to match url against known services
        for regex, get_content in self.service_regex_dict.items():
            m = re.match(regex, msg)
            if not m:
                continue
            paste_data = get_content(m.group(0))

        # weird phrasing due to paste_data possibly being unknown
        return None if "paste_data" not in locals() else paste_data

    def _archive(self, paste_data, timestamp, chan, mask):
        """ Simply fetches from a hoster and returns list of content data """
        filenames = []
        #NOTE paste_data is a list of dictionaries
        for data in paste_data:
            try:
                data['mask'] = str(mask)
            except Exception:
                print("Something went wrong with", data)
                exit(0)
            save(data, timestamp, self.archive_path)
            filenames.append(data['orig_filename'])
        return filenames
