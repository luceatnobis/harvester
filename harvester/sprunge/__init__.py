#!/usr/bin/env python3

import requests

from urllib.parse import urlsplit


def get_content(url):
    paste_info = {
        'site': 'sprunge',
        'url': url,
    }

    content_id = urlsplit(url).path[1:]

    content_url = url

    response = requests.get(content_url)
    if response.status_code != 200:
        return

    paste_info['ext'] = ""
    paste_info['orig_filename'] = content_id
    paste_info['content'] = response.content
    return [paste_info]
