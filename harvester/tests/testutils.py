#!/usr/bin/env python3

import os
import pdb
import asyncio
from unittest import TestCase

try:
    from unittest import mock
except ImportError:
    import mock

import irc3

from harvester.harvester import HarvesterBot

MagicMock = mock.MagicMock
patch = mock.patch
call = mock.call

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def call_later(i, func, *args):
    if func.__name__ in dir(IrcBot):
        func(*args)
    return asyncio.Handle(func, args, asyncio.get_event_loo())

def call_soon(func, *args):
    func(*args)
    return asyncio.Handle(func, args,  asyncio.get_event_loop())

@irc3.plugin
class HarvesterTest(HarvesterBot):

    def __init__(self, bot):
        self.bot = bot

    def _create_paths(self):  # in test cases, we dont want to create paths
        pass

class IrcBot(irc3.IrcBot):

    def __init__(self, **config):
        self.check_required()
        if 'loop' not in config:
            loop = asyncio.new_event_loop()
            loop = mock.create_autospec(loop, spec_set=True)
            loop.call_later = call_later
            loop.call_soon = call_soon
            loop.time.return_value = 10
            config.update(testing=True, async=False, level=1000,
                          loop=loop)
        else:
            config.update(testing=True, level=1000)
        super(IrcBot, self).__init__(**config)
        self.protocol = irc3.IrcConnection()
        self.protocol.closed = False
        self.protocol.factory = self
        self.protocol.transport = MagicMock()
        self.protocol.write = MagicMock()

    def check_required(self):  # pragma: no cover
        dirname = os.path.expanduser('~/.irc3')
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        filename = os.path.expanduser('~/.irc3/passwd.ini')
        if not os.path.isfile(filename):
            with open(filename, 'w') as fd:
                fd.write(passwd_ini)

    def test(self, data, show=True):
        self.dispatch(data)
        if show:
            for line in self.sent:  # pragma: no cover
                if PY3:
                    print(line)
                else:
                    print(line.encode('utf8'))

    @property
    def sent(self):
        values = [tuple(c)[0][0] for c in self.protocol.write.call_args_list]
        self.protocol.write.reset_mock()
        if not PY3:  # pragma: no cover
            return [v.encode('utf8') for v in values]
        return values

class IrcTestCase(TestCase):

    project_path = PROJECT_PATH

    def patch_requests(self, **kwargs):
        self.patcher = patch('requests.Session.request')
        self.addCleanup(self.patcher.stop)
        request = self.patcher.start()

        filename = kwargs.pop('filename', None)
        if filename:
            filename = os.path.join(self.project_path, filename)
            with open(filename, 'rb') as feed:
                content = feed.read()
            for k, v in kwargs.items():
                content = content.replace(k.encode('ascii'), v.encode('ascii'))
            kwargs['content'] = content
            kwargs['text'] = content.decode('utf8')
        kwargs.setdefault('status_code', 200)
        resp = MagicMock(**kwargs)
        for k, v in kwargs.items():
            if k in ('json',):
                setattr(resp, k, MagicMock(return_value=v))
        request.return_value = resp
        return request

    def patch_asyncio(self):
        patcher = patch('irc3.compat.asyncio.Task')
        self.Task = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('irc3.compat.asyncio.get_event_loop')
        patcher.start()
        self.addCleanup(patcher.stop)


class BotTestCase(IrcTestCase):

    config = {'nick': 'nono'}

    def callFTU(self, **config):
        config = dict(self.config, **config)
        bot = IrcBot(**config)
        self.bot = bot
        return bot

    def assertSent(self, lines):
        if not lines:
            self.assertNothingSent()
            return
        if not self.bot.loop.called:
            self.bot.protocol.write.assert_has_calls(
                [call(l) for l in lines])
        else:  # pragma: no cover
            self.bot.loop.call_later.assert_has_calls(
                [call(l) for l in lines])
        self.reset_mock()

    def assertNothingSent(self):
        self.assertFalse(self.bot.protocol.write.called)
        self.assertFalse(self.bot.loop.called)
        self.reset_mock()

    def reset_mock(self):
        self.bot.protocol.write.reset_mock()
        self.bot.loop.reset_mock()
