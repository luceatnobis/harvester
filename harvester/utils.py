#!/usr/bin/env python3
# -+- coding: utf-8 -*-
import re
import json
import hashlib

from os import path, makedirs, SEEK_CUR

from harvester import libDataBs


def getOrCreatePath(archive_base_path):
    if not path.exists(archive_base_path):
        makedirs(archive_base_path)


def setUpDir(site, archive_base_path):
    """Prepare directory and json path for download."""
    archive_json = path.join(archive_base_path, "archive.json")
    final_dir = path.join(archive_base_path, site)
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
        print(db.gibData(data['md5']))
        if not db.checkHashExistence(data['md5']):
            # save the file
            with open(file_location, 'wb') as f:
                f.write(data['content'])
            db.insertData(
                {'hash': data['md5'], 'filename': filename, 'count': 1})
        else:
            # just update the count
            db.upCount(data['md5'])
    del data['content']
    print(data)

    # save information about data in json file
    appendToJson(data, archive_json)


def urlReg(msg):
    """Try to match an url."""
    m = re.match('^.*(https?://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?)', msg)
    if m:
        return m.group(1)
    return
