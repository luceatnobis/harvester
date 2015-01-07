import json
import os
archive_dir = os.environ['HOME'] + os.sep + "archive"
archive_json = archive_dir + os.sep + "archive.json"

paste_data = {'ext': 'png', 'orig_filename': 'WO57MsX', 'site': 'prntscr', 'url': 'http://prntscr.com/5o2enp', 'timestamp': '1420658389107', 'location': '/home/Killjoy/archive/prntscr/1420658389107_WO57MsX.png', 'md5': 'f6585b7b71fd56e759f6b95ff0e8f20f'}
print(archive_json)


with open(archive_json, "x") as fj:
    try:
        print(fj.read())
        dat = json.load(fj)
        print(dat)
        dat.append(paste_data)
    except ValueError:
        dat = [paste_data]
#with open(archive_json, 'w+') as fj:
#    json.dump(dat, fj)
