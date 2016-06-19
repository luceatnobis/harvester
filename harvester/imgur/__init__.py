#!/usr/bin/env python

import os
import sys
import requests
import grequests
import imgurpython

from itertools import repeat as rep

try:
    from urlparse import urlsplit
except ImportError:
    from urllib.parse import urlsplit

from bs4 import BeautifulSoup

sys.path.append(os.path.join(os.environ['HOME'], '.harvester'))
import key_imgur


def get_content(url):
    split = urlsplit(url)
    path_elements = [x for x in split.path.split("/") if x]

    if len(path_elements) == 1:
        return retrieve_single(url)
    elif 1 < len(path_elements):
        client = imgurpython.ImgurClient(
            key_imgur.cred['client-id'], key_imgur.cred['client-secret']
        )
        particle, content_id = path_elements[:2]
        if particle == 'a':
            links = [x.link for x in client.get_album_images(content_id)]
        elif particle == 'gallery':
            g = client.gallery_item(content_id)
            if hasattr(g, 'images'):
                links = [x['link'] for x in g.images]
            else:
                links = [g.link]  # we can have a gallery with only one item

        if len(links) > 200:
            return None

        rs = (grequests.get(x) for x in links)
        res = grequests.map(rs)

        f = sort_func(links)  # for sorting
        res.sort(key=f)
        info = mk_pasteinfo(*[(x, u) for x, u in zip(res, rep(url))])

        for paste, r in zip(info, res):
            paste['content'] = r.content
        return info



def retrieve_single(url):
    paste_info = {
        'site': 'imgur',
    }
    split = urlsplit(url)
    path_elements = [x for x in split.path.split("/") if x]

    element = path_elements[0]
    response = requests.get(url)

    if response.status_code != 200:
        return

    if "." in element:
        content_url = url
    else:
        soup = BeautifulSoup(response.text, "html5lib")
        content_url = soup.find('link', {'rel': 'image_src'})['href']

    response = requests.get(content_url)
    paste_info = mk_pasteinfo((response, url))
    paste_info[0]['content'] = response.content
    return paste_info


def mk_pasteinfo(*args):
    info = list()
    for rs in args:
        paste_info = {
            'site': 'imgur',
        }
        response, url = rs
        content_url = response.url
        orig_filename, ext = content_url.split("/")[-1].split(".")
        paste_info['url'] = url
        paste_info['ext'] = ext
        paste_info['orig_filename'] = orig_filename
        info.append(paste_info)

    return info

def sort_func(all_links):
    return lambda x: all_links.index(x.url)
