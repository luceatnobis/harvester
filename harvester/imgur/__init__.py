#!/usr/bin/env python3

import os
import re
import json
import requests

from bs4 import BeautifulSoup

from packages import imgurpython


def get_content(url):
    paste_info = {
        'site': 'imgur',
        'url': url
    }
    content_id = url.split('/')[-1]
    imgur_conf = load_config()
    imgur_client = imgurpython.ImgurClient(
        imgur_conf['client_id'], imgur_conf['client_secret'])

    if "/a/" in url:  # dealing with an album
        print("album")
        paste_info['type'] = 'album'
        stuff = imgur_client.get_album(content_id)
    elif "/gallery/" in url:  # dealing with a gallery
        paste_info['type'] = 'gallery'
    else:  # a normal image. Hopefully.
        paste_info.update(load_single_image(imgur_client, content_id))

    return paste_info

    """
    m = re.match('^.*com(?:/gallery)?/([0-9a-zA-Z]+)(?:\.([a-zA-Z]+))?$',url)
    response = requests.get(url)
    if response.status_code != 200:
        return
    if not m.group(2):
        soup = BeautifulSoup(response.text)
        url1 =  soup.find('meta', {'property': 'og:image'})['content']
        m = re.match('^.*com/([0-9a-zA-Z]+)\.([a-zA-Z]+)$',url1)
        response = requests.get(url1)
        if response.status_code != 200:
            return

    paste_info['ext'] = m.group(2)
    paste_info['orig_filename'] = m.group(1)
    paste_info['content'] = response.content
    return paste_info
    """

def load_single_image(imgur_client, content_id):
    content_info = dict()
    try:
        content_metadata = imgur_client.get_image(content_id)
    except imgurpython.client.ImgurClientError:
        return

    response = requests.get(content_metadata.link)
    if response.status_code != 200:
        return

    content_info['ext'] = content_metadata.type.split('/')[-1]
    content_info['content'] = response.content
    content_info['orig_filename'] = content_id

    return content_info

def load_config():
    json_path = os.path.join(".", "config", "imgur.json")
    f = open(json_path)
    try:
        imgur_conf = json.load(f)
    except:  #TODO: figure out which exception to catch here
        return
    return imgur_conf
