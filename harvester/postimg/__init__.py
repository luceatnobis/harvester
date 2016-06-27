#!/usr/bin/env python
# NOTE: please don't ever ask questions about this code.

import pdb
import requests
import grequests

from itertools import repeat as rep

try:
    from urlparse import urlsplit
except ImportError:
    from urllib.parse import urlsplit

from bs4 import BeautifulSoup


def get_content(url):
    split = urlsplit(url)
    path_elements = [x for x in split.path.split("/") if x]

    response = requests.get(url)
    if not response.ok:
        return
    if path_elements[0] == "image":
        # https://postimg.org/image/e68igfdqo/
        # https://postimg.org/image/85atjcr4h/ (upload and image page)
        soup = BeautifulSoup(response.text, "html5lib")
        try:
            links = soup.find('input', {'id': 'code_hotlink'}).get('value')
        except:
            pdb.set_trace()
        info = process_dl_link(url, *[links])
    elif path_elements[0] == "gallery":
        # https://postimg.org/gallery/380x4rxc2/
        # https://postimg.org/gallery/380x4rxc2/1b59c905/
        soup = BeautifulSoup(response.text, "html5lib")
        all_links = (
            soup.find('option', {'id': 'bbcode_direct'}).get('value')
        ).split("\n")
        info = process_dl_link(url, *all_links)

    elif len(split.netloc.split(".")) == 3:
        # https://s32.postimg.org/gnk9noxn9/carlton.png
        # https://s32.postimg.org/gnk9noxn9/carlton.png?dl=1
        info = process_dl_link(url, *[url.replace("?dl=1", "")])
    else:
        return
    return info


def process_dl_link(orig_url, *dl_link):
    f = sort_func(dl_link)

    reqs = (grequests.get(x) for x in dl_link)
    responses = grequests.map(reqs)
    responses.sort(key=f)

    info = mk_pasteinfo(*[(x, u) for x, u in zip(responses, rep(orig_url))])
    return info


def mk_pasteinfo(*args):
    info = list()
    for rs, url in args:
        content_url = rs.url
        paste_info = {
            'url': url,
            'site': 'postimg',
            'content': rs.content
        }
        orig_filename, ext = content_url.split("/")[-1].split(".")
        paste_info['ext'] = ext
        paste_info['orig_filename'] = orig_filename
        info.append(paste_info)

    return info


def sort_func(all_links):
    return lambda x: all_links.index(x.url)


def upload_page_to_img_particle(*url):
    links = []
    f = sort_func(url)

    reqs = (grequests.get(x) for x in url)
    responses = grequests.map(reqs)
    responses.sort(key=f)

    for r in responses:
        soup = BeautifulSoup(r.text, "html5lib")
        links.append(soup.find_all('img')[1].get('src').split("/")[-2])
    return links


def image_page_to_dl_link(*url):
    links = []
    f = sort_func(url)

    reqs = (grequests.get(x) for x in url)
    responses = grequests.map(reqs)
    responses.sort(key=f)

    for r in responses:
        soup = BeautifulSoup(r.text, "html5lib")
        links.append(soup.find_all('a')[2].get('href')[:-5])
    return links
