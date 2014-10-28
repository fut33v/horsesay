#!/usr/bin/env python


import urllib
import urllib2
import json
import os
import random
from functools import partial


json_pretty_dumps = partial(
    json.dumps,
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
)


def load_json_file(filename):
    json_f = open(filename, 'r')
    json_obj = json.loads(json_f.read())
    json_f.close()
    return json_obj


def save_json_file(filename, data):
    json_txt = json_pretty_dumps(data)
    json_f = open(filename, 'w')
    json_f.write(json_txt)
    json_f.close()


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def call_open_api(method, params, v='5.25'):
    params.append(("v", v))
    url = "https://api.vk.com/method/%s?%s" % (method, urllib.urlencode(params))
    response = urllib2.urlopen(url).read()
    if 'response' in response:
        return json.loads(response)['response']
    else:
        print response


def wall_get(owner_id, count='20'):
    return call_open_api('wall.get', [('owner_id', owner_id), ('count', count)])


def in_dict(dictionary, element):
    if element in dictionary:
        return dictionary[element]
    else:
        return None


if __name__ == "__main__":
    CLUB_ID = -66178227
    POSTS_NUMBER = 100
    POST_TMP_FILE = ".post_tmp"
    POSTS_FILE = ".suda_podoidi.json"

    network_error = False
    horse_wall = None
    try:
        horse_wall = wall_get(CLUB_ID, POSTS_NUMBER)
    except urllib2.URLError as e:
        print e.reason
        network_error = True

    if network_error:
        if not os.path.exists(POSTS_FILE):
            print "Network error and no posts"
            exit()
        else:
            posts = load_json_file(POSTS_FILE)
    else:
        posts = []
        items = in_dict(horse_wall, 'items')
        if items:
            for item in items:
                post = in_dict(item, 'text')
                if post:
                    posts.append(post)
            save_json_file(POSTS_FILE, posts)
        else:
            exit()


    r = random.randint(0, len(posts))
    random_post = posts[r].encode('utf8', 'replace')
    open(POST_TMP_FILE, 'w').write(random_post)
    horsesay = "cat " + POST_TMP_FILE + " | cowsay -f pony"

    if which('cowsay') is None:
        print (
            "Seems like 'cowsay' not installed on your PC, " +
            "on Debian/Ubuntu/Mint:\n" +
            "type: sudo apt-get install cowsay"
        )
    else:
        os.system(horsesay)
