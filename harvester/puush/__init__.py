#!/usr/bin/env python3

import requests


def get_content(url):
    paste_info = {
        'site': 'puush',
        'url': url,
    }

    content_url = url
    response = requests.get(content_url)
    if response.status_code != 200:
        return

    folder_id, filename = url.split("/")[-2:]
    paste_id, ext = filename.split(".")
    paste_info['ext'] = ext
    paste_info['orig_filename'] = folder_id + '_' + paste_id
    paste_info['content'] = response.content
    return [paste_info]
