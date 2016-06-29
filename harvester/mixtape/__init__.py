#!/usr/bin/env python3

import re
import requests

from urllib.parse import urlsplit

def get_content(url):
    spit_base_url = "https://spit.mixtape.moe/view/download/"

    paste_info = {
        'site': 'mixtape',
        'url': url,
    }

    fragments = urlsplit(url)
    subdomain = fragments.netloc.split(".")[0]

    if subdomain == "spit":  # we have a paste
        ext = ""
        paste_id = fragments.path.split("/")[-1]
        content_url = spit_base_url + paste_id
    elif subdomain == "my":  # we have other content
        paste_id, ext = fragments.path.split("/", 1)[-1].split(".", 1)
        content_url = url
    else:
        return

    response = requests.get(content_url)
    if response.status_code != 200:
        return

    paste_info['ext'] = ext
    paste_info['orig_filename'] = paste_id
    paste_info['content'] = response.content
    return [paste_info]
