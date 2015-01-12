#!/usr/bin/env python3
# -+- coding: utf-8 -*-
import time
import json
import hashlib 
import re
import os

from harvester import gyazo
from harvester import imgur
from harvester import ppomf
from harvester import bpaste
from harvester import dpaste
from harvester import infotomb
from harvester import prntscrn
from harvester import hastebin
from harvester import pastebin
from harvester import cubeupload
from harvester import libDataBs

#Function operating on harvested data. 
#Takes dictionary as input
def saver(paste_data,timestamp,mask):
    archive_dir = os.environ['HOME'] + os.sep + "archive"
    archive_json = archive_dir + os.sep + "archive.json"
    paste_data['md5'] = hashlib.md5(paste_data['content']).hexdigest()
    paste_data['timestamp'] = timestamp
    final_folder = (
        archive_dir + os.sep + paste_data['site'])
 
    if not os.path.exists(final_folder):
        os.makedirs(final_folder)
    filename = str(timestamp) + "_" + paste_data['orig_filename']
    filename += ".%s" % paste_data['ext'] if paste_data['ext'] else ""
 
    file_location = final_folder + os.sep + filename
    paste_data['location'] = file_location
 
    with libDataBs.DataBs() as db:
        print(db.gibData(paste_data['md5']))
        if not db.check(paste_data['md5']):
            with open(file_location, 'wb') as f:
                f.write(paste_data['content'])
            db.set({'hash': paste_data['md5'], 'filename': filename, 'count': 1})
        else:
            db.upCount(paste_data['md5'])
    del paste_data['content']
    paste_data['mask'] = mask
    print(paste_data)
    #obscure way to ensure that we always have a file to read from/to
    open(archive_json, 'a').close()
    with open(archive_json, "r") as fj:
        try:
            dat = json.load(fj)
            dat.append(paste_data)
        except ValueError:
            dat = [paste_data]
    with open(archive_json, 'w+') as fj:
        json.dump(dat, fj)

#Given url, checks if it matches one of regexes and tries to gather data from them
def harvest(mask, msg, bot,chan):
    timestamp = str(int(time.time() * 1000))
    #NOTE site harvesters should return a list of dictionaries, even if only one file has been gathered
    paste_regex_to_func = {
        '^https?://pastebin\.com/(raw\.php\?i=)?[a-zA-Z0-9]+': pastebin.get_content,
        '^https?://p\.pomf\.se/[\d.]+': ppomf.get_content,
        '^https?://(?:infotomb\.com|itmb\.co)/[0-9a-zA-Z.]+': infotomb.get_content,
        '^https?://prntscr\.com/[0-9a-zA-Z]+': prntscrn.get_content,
        # dpaste doesnt get along with https, so we're not gonna bother
        '^http://dpaste\.com/[0-9a-zA-Z]+': dpaste.get_content,
        '^https?://bpaste\.net/(raw|show)/[0-9a-zA-Z]+': bpaste.get_content,
        '^https?://hastebin\.com/(raw/[a-z]+)|([a-z]+\.hs)': hastebin.get_content, 
        # here come the image hosters
        '^https?://(i\.)?cubeupload\.com/(im/)?[a-zA-Z0-9.]+': cubeupload.get_content,
        '^https?://(i\.)?imgur\.com/(gallery/)?[a-zA-Z0-9.,]+': imgur.get_content,
        '^https?://(cache\.|i\.)?gyazo.com/[a-z0-9]{32}(\.png)?': gyazo.get_content
    }
    for regex, func in paste_regex_to_func.items():
        m = re.match(regex, msg)
        if not m:
            continue
        paste_data = func(m.group(0))
 
    # either no regex was found to match or no content could be pulled
    if not "paste_data" in locals() or paste_data is None:
            return
    #NOTE paste_data is a list of dictionaries
    filenames = []
    #print("Paste data:")
    #print(paste_data)
    for data in paste_data:
        saver(data,timestamp,mask)
        filenames.append(data['orig_filename'])
    bot.privmsg(chan, "^ Archived file(s): " + " ".join(filenames) + " ^")
    return True 


#Simple regex to match an url
def urlReg(msg):
    m = re.match('^.*(https?://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?)', msg)
    if m:
        return m.group(1)
    return
