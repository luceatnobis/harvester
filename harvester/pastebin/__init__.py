#!/usr/bin/env python3

import requests


def get_content(url):
    paste_info = {
        'site': 'pastebin',
        'url': url,
    }

    # http://pastebin.com/Vcz07KuK  regular
    # http://pastebin.com/raw/Vcz07KuK  new raw
    # http://pastebin.com/raw.php?i=Vcz07KuK  old raw

    if "raw.php" in url:
        # dissolve the key=value pairs
        param_str_raw = url[url.index('?')+1:]
        params = {k: v for (k, v) in (
            kv.split('=') for kv in param_str_raw.split('&'))}

        paste_id = params.get('i')
        if paste_id is None:  # no i parameter
            return
        content_url = url

    else:
        paste_id = url.split('/')[-1]
        if '/raw/' not in url:
            content_url = "http://pastebin.com/raw/" + paste_id
        else:
            content_url = url

    response = requests.get(content_url)
    if response.status_code != 200:
        return

    paste_info['ext'] = ""
    paste_info['orig_filename'] = paste_id
    paste_info['content'] = response.content
    return [paste_info]
