# -*- coding: utf-8 -*-
import requests
import re
from pymongo import MongoClient
from multiprocessing import Process, Queue, Pool


def get_hash(limit):
    client = MongoClient('localhost', 27017)
    db = client['bt1024']
    collection = db['torrents']
    bt_hash = []
    for item in collection.find().limit(limit=limit):
        bt_hash.append(item['hash'])
    return bt_hash


def download_torrent(torrent_hash):
    download_url = 'http://www.rmdown.com/download.php'
    bt_url = 'http://www.rmdown.com/link.php?hash=' + torrent_hash
    rref_re = re.compile('(?<=NAME="reff" value=").+?(?="><BR>)')
    r = requests.get(bt_url)
    rref = re.findall(rref_re, r.text)[0]
    cookie_jar = r.cookies

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
        'Referer': bt_url,
        'Host': 'www.rmdown.com',
    }

    payload = {
        'ref': (None, torrent_hash),
        'reff': (None, rref),
        'submit': (None, 'download')
    }

    print('Downloading torrent %s ...' % torrent_hash)

    download = requests.post(download_url, data=payload, cookies=cookie_jar, headers=headers)

    filename = torrent_hash + '.torrent'
    with open(filename, 'wb') as f:
        f.write(download.content)

    print('Downloading torrent %s OK!' % filename)


if __name__ == '__main__':
    hashes = get_hash(0)
    p = Pool(8)
    for bt_hash in hashes:
        p.apply_async(download_torrent, args=(bt_hash,))
    print('Begin to download torrents...')
    p.close()
    p.join()
    print('All files get done.')