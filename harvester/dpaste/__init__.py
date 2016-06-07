#!/usr/bin/env python

import requests


def get_content(url):
    paste_info = {
        'site': 'dpaste',
        'url': url,
    }
    paste_id = url.split('/')[-1]
    if not url.endswith(".txt"):
        content_url = ("%s.txt" % url)
    else:
        content_url = url

    response = requests.get(content_url)
    if response.status_code != 200:
        return

    paste_info['ext'] = ""
    paste_info['orig_filename'] = paste_id
    paste_info['content'] = response.content
    return [paste_info]
