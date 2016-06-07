#!/usr/bin/env python
import requests
import re
def get_content(url):
    paste_info = {
        'site': 'pomf',
        'url': url
    }
    m = re.match('^.*/([0-9a-zA-Z]+)\.([a-zA-Z0-9]+)$',url)
    response = requests.get(url)
    if response.status_code != 200:
        return
    paste_info['ext'] = m.group(2)
    paste_info['orig_filename'] = m.group(1)
    paste_info['content'] = response.content
    return paste_info
