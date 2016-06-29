#!/usr/bin/env python3

import re
from urllib.parse import urlsplit

import requests

def get_content(url):
    paste_info = {
        'url': url,
        'site': 'anonmgr',
    }
    direct_base_url = "https://anonmgur.com/up/"
    fragments = urlsplit(url)
    nodes = [x for x in fragments.path.split("/") if x]
    if re.match("[a-z0-9]{32}\..{,3}", fragments.query):
        fname = fragments.query
        content_url = direct_base_url + fragments.query
    elif nodes[0] == 'up':
        fname = nodes[-1]
        content_url = url
    else:
        return

    response = requests.get(content_url)
    if response.status_code != 200:
        return

    fname, ext = fname.rsplit(".")
    paste_info['ext'] = ext
    paste_info['orig_filename'] = fname
    paste_info['content'] = response.content
    return [paste_info]
