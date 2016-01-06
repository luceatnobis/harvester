#!/usr/bin/env python3
# -+- coding: utf-8 -*-
import json
import hashlib
import re
from os import path, makedirs, SEEK_CUR

from harvester import libDataBs


def getOrCreatePath(path_):
    if not path.exists(path_):
        makedirs(path_)


def setUpDir(site, path_):
    """Prepare directory and json path for download."""
    archive_dir = path.join(*path_)
    archive_json = path.join(archive_dir, "archive.json")
    final_dir = path.join(archive_dir, site)
    getOrCreatePath(final_dir)
    return final_dir, archive_json


def appendToJson(data, file):
    """Append data to the end of json list without parsing it."""
    with open(file, "ab+") as fj:
        data_string = "{}]".format(json.dumps(data))
        if fj.tell() > 0:
            fj.seek(-1, SEEK_CUR)  # remove closing bracket of the json list
            fj.truncate()
            data_string = ", {}".format(data_string)
        else:
            data_string = "[{}".format(data_string)
        b = bytearray()
        b.extend(map(ord, data_string))
        fj.write(b)


def save(data, timestamp, path_):
    """Save given data into specified environment."""
    # prepare directory
    final_dir, archive_json = setUpDir(data['site'], path_)

    # prepare filename and location
    data['md5'] = hashlib.md5(data['content']).hexdigest()
    data['timestamp'] = timestamp
    filename = str(timestamp) + "_" + data['orig_filename']
    filename += ".%s" % data['ext'] if data['ext'] else ""
    file_location = path.join(final_dir, filename)
    data['location'] = file_location

    # check if we already downloaded the file
    with libDataBs.DataBs() as db:
        if not db.checkHashExistence(data['md5']):
            # save the file
            with open(file_location, 'wb') as f:
                f.write(data['content'])
            db.insertData({'hash': data['md5'], 'filename': filename, 'count': 1})
        else:
            # just update the count
            db.upCount(data['md5'])
    del data['content']

<<<<<<< HEAD
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
        #'^https?://hastebin\.com/(raw/[a-z]+)|([a-z]+\.hs)': hastebin.get_content, 
        '^https?://hastebin\.com/((raw/[a-z]+)|[a-z]+\.coffee)': hastebin.get_content, 
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
=======
    # save information about data in json file
    appendToJson(data, archive_json)
>>>>>>> 4f5b0caa29f92547c36b4ce23a1ba6af06d8484e


def urlReg(msg):
    """Try to match an url."""
    m = re.match('^.*(https?://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?)', msg)
    if m:
        return m.group(1)
    return
