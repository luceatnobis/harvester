#!/usr/bin/env python3
# -+- coding: utf-8 -*-
import time
import json
import hashlib
import re
from os import path, makedirs

from harvester import libDataBs


def getOrCreatePath(path_):
    if not path.exists(path_):
        print(path_)
        makedirs(path_)


def setUpDir(site, path_):
    """Prepare directory and json path for download."""
    archive_dir = path.join(*path_)
    archive_json = path.join(archive_dir, "archive.json")
    final_dir = path.join(archive_dir, site)
    getOrCreatePath(final_dir)
    return final_dir, archive_json


def saver(data, timestamp, path_):
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
        print(db.gibData(data['md5']))
        if not db.check(data['md5']):
            # save the file
            with open(file_location, 'wb') as f:
                f.write(data['content'])
            db.set({'hash': data['md5'], 'filename': filename, 'count': 1})
        else:
            # just update the count
            db.upCount(data['md5'])
    del data['content']
    print(data)

    # save information about data in json file
    # obscure way to ensure that we always have a file to read from/to
    open(archive_json, 'a').close()
    with open(archive_json, "r") as fj:
        try:
            dat = json.load(fj)
            dat.append(data)
        except ValueError:
            dat = [data]
    with open(archive_json, 'w+') as fj:
        json.dump(dat, fj)


def harvest(mask, msg, bot, chan, settings):
    """Try to harvest given url and save the file."""
    timestamp = str(int(time.time() * 1000))
    #NOTE site harvesters should return a list of dictionaries, even if only one file has been gathered
    # try to match url against known services
    for regex, get_content in settings.service_regex_dict.items():
        m = re.match(regex, msg)
        if not m:
            continue
        paste_data = get_content(m.group(0))

    # either no regex was found to match or no content could be pulled
    if "paste_data" not in locals() or paste_data is None:
        return
    #NOTE paste_data is a list of dictionaries
    filenames = []
    for data in paste_data:
        data['mask'] = mask
        saver(data, timestamp, settings.path)
        filenames.append(data['orig_filename'])
    bot.privmsg(chan, "^ Archived file(s): {} ^".format(" ".join(filenames)))
    return True


def urlReg(msg):
    """Try to match an url."""
    m = re.match('^.*(https?://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?)', msg)
    if m:
        return m.group(1)
    return
