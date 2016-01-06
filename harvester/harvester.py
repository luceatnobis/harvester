import irc3
from harvester.settings import HarvesterSettings
from harvester.utils import urlReg, save
import time
import re


@irc3.plugin
class HarvesterBot(HarvesterSettings):
    requires = [
        'irc3.plugins.core',
        'irc3.plugins.userlist',
        'irc3.plugins.command',
        'irc3.plugins.human',
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
                channel, "All of your links belong to me!"
                "(As long as you use proper sites)")

    def harvest(self, mask, msg, chan):
        """Try to harvest given url and save the file."""
        timestamp = str(int(time.time() * 1000))
        #NOTE site harvesters should return a list of dictionaries, even if only one file has been gathered
        # try to match url against known services
        for regex, get_content in self.service_regex_dict.items():
            m = re.match(regex, msg)
            if not m:
                continue
            paste_data = get_content(m.group(0))

        # either no regex was found to match or no content could be pulled
        if "paste_data" not in locals() or paste_data is None:
            return
        #NOTE paste_data is a list of dictionaries
        filenames = []
        for data in paste_data:
            data['mask'] = mask
            save(data, timestamp, self.archive_path)
            filenames.append(data['orig_filename'])
        self.bot.privmsg(
            chan, "^ Archived file(s): {} ^".format(" ".join(filenames)))
        return True
