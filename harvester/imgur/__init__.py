#!/usr/bin/env python
import requests
import re
from bs4 import BeautifulSoup
def get_content(url):
    m = re.match('^.*com(?:/gallery)?/((?:[0-9a-zA-Z]+,?)+)(?:\.([a-zA-Z]+))?$',url)
    if not m:
        return
    spl = m.group(1).split(',')
    ext = m.group(2)
    pastes =[]
    for id in spl:
        if id != '':
            pastes.append(get_file(id,url,ext))
    return pastes
                  
              

def get_file(id,url,ext=None): #NOTE we are passing url for a strict logs, we can construct it from id and extension
    paste_info = {
        'site': 'imgur',
        'url': url
    }    
    if not ext:
        ext = ''
    url = 'http://imgur.com/' + id + ext
    response = requests.get(url)
    if response.status_code != 200:
        return
    if ext == '':
        soup = BeautifulSoup(response.text)
        url =  soup.find('meta', {'property': 'og:image'})['content']
        m = re.match('^.*com/([0-9a-zA-Z]+)\.([a-zA-Z]+)$',url)
        response = requests.get(url)
        if response.status_code != 200:
            return
        ext = m.group(2)
    paste_info['ext'] = ext
    paste_info['orig_filename'] = id
    paste_info['content'] = response.content
    return paste_info
'''
url = 'http://imgur.com/hCHNzqk,FmdkfhX,4RTUR3B'
print(get_content(url))
'''
