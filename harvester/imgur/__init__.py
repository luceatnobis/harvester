#!/usr/bin/env python3
import re
import pdb
import requests

from urllib.parse import urlparse

# import imgurpython
from bs4 import BeautifulSoup

from harvester import auth


def get_content(url):

    paste_info = {
        'site': 'imgur',
        'url': url
    }

    # methods that process urls like imgur.com/gallery/ and imgur.com/a/
    chain_links = {
        'a': _return_a,
        'gallery': _return_gallery,
    }
    # original regex (doesnt match /a/)
    # m = re.match('^.*com(?:/gallery)?/([0-9a-zA-Z]+)(?:\.([a-zA-Z]+))?$', url)
    # modified regex that fell out of favour (brotherBox))
    # m = re.match('^.*com(?:/((gallery|a)/([0-9a-zA-Z]+)|(?:\.([a-zA-Z]+))?$))', url)

    parsed = urlparse(url)
    if parsed.netloc != "imgur.com":
        pass  # TODO: think of something smart

    """
    imgurclient = imgurpython.ImgurClient(
        auth.imgur_client_id, auth.imgur_client_secrets)
    """

    path = parsed.path.split("/")[1:]
    n_elements = len(path)

    if n_elements == 1:  # we probably have a single piece of content
        pass
    elif n_elements == 2:  # we have either /a/ or /gallery/
        fun = chain_links.get(path[0])
        if fun is None:
            raise NotImplementedError(path[0])
        # foo = fun(imgurclient, path[1])
        foo = fun(path[1])
    else:
        pass  # TODO: think of something for imgur.com/foo/bar/baz[/bam...]
    """
    response = requests.get(url)
    if response.status_code != 200:
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

'''
url = 'http://imgur.com/gallery/aChgMdG'
print get_content(url)
'''

def _return_single_content(foo):
    pass

def _return_a(foo):
    pass

def _return_gallery(client, gallery_id):
    query = client.gallery_search(gallery_id)
    gallery = [x for x in query if x.id == gallery_id]
    if not gallery:  # we have an invalid gallery i believe
        pass
    gallery = gallery[0]
    pdb.set_trace()
