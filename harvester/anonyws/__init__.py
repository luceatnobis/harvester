#!/usr/bin/env python3


import requests

from bs4 import BeautifulSoup
from urllib.parse import urlsplit


def get_content(url):
    paste_info = {
        'site': 'anonyws',
        'url': url,
    }
    fragments = urlsplit(url)
    nodes = [x for x in fragments.path.split("/") if x]
    if nodes[0] == 'i':
        filename = nodes[-1]
        fname_frags = filename.split(".")
        if fname_frags[-2] in ('th', 'md'):
            # remove th, md from filename.(th|md).ext
            fname = ".".join(fname_frags[:-2]) + '.'+ fname_frags[-1]
        else:
            fname = ".".join(fname_frags[-2:])
        content_url = "https://anony.ws/" + '/'.join(nodes[:-1]) + '/' + fname
    elif nodes[0] == 'image':
        share_pg = requests.get(url)
        soup = BeautifulSoup(share_pg.text, "html5lib")
        content_url = soup.find('input', {'id': 'embed-code-1'})['value']
        fname = content_url.split("/")[-1]

    response = requests.get(content_url)
    if response.status_code != 200:
        return

    paste_info['ext'] = fname.rsplit(".")[1]
    paste_info['orig_filename'] = fname
    paste_info['content'] = response.content
    return [paste_info]
