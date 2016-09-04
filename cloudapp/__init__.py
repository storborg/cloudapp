import sys
import os.path
import configparser
import subprocess
from collections import OrderedDict

import requests
from requests.auth import HTTPDigestAuth

from datetime import datetime

__version__ = '0.0.0.dev'


def load_credentials():
    path = os.path.join(os.path.expanduser('~'), '.cloudapp')
    if not os.path.exists(path):
        print("First configure cloudapp by creating a .cloudapp file with ")
        print("login credentials. For example:")
        print("")
        print("[cloudapp]")
        print("email: alyssa.p.hacker@gmail.com")
        print("password: l!spforl!fe")
        print("")
        raise SystemExit
    config = configparser.ConfigParser()
    config.read(path)
    fields = config['cloudapp']
    return fields['email'], fields['password']


def make_timestamped_filename(spec):
    datestring = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    return 'screenshot-%s-%s.png' % (datestring, spec)


def gnome_screenshot(filename):
    args = ['gnome-screenshot', '-f', filename]
    print("Running: %s" % (' '.join(args)))
    subprocess.call(args)


def screenshot_all():
    filename = make_timestamped_filename('all')
    gnome_screenshot(filename)
    return filename


def upload_drop(path, email, password):
    auth = HTTPDigestAuth(email, password)
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'cloudapp-python/%s' % __version__,
    }

    # request to upload
    r = requests.get('http://my.cl.ly/items/new', auth=auth, headers=headers)
    initial_resp = r.json()

    post_url = initial_resp['url']
    param_list = []
    for k, v in initial_resp['params'].items():
        param_list.append((k, v))
    data = OrderedDict(sorted(param_list))

    filename = os.path.basename(path)
    data['key'] = data['key'].replace('${filename}', filename)
    files = {'file': (filename, open(path, 'rb').read())}

    # upload to S3
    r = requests.post(post_url, data=data, files=files, allow_redirects=False)
    confirm_url = r.headers['Location']

    r = requests.get(confirm_url, auth=auth, headers=headers)
    confirm_resp = r.json()
    return confirm_resp['url']


def write_clipboard(contents):
    args = ['xclip', '-selection', 'clipboard']
    p = subprocess.Popen(args, stdin=subprocess.PIPE)
    p.communicate(input=contents.encode('utf8'))


def main(args=sys.argv):
    email, password = load_credentials()

    # check what we got called with
    arg = sys.argv[1]

    # if it's a file, upload it
    if os.path.exists(arg):
        filename = arg

    # if it's a screenshot command, take the screenshot
    elif arg == 'all':
        filename = screenshot_all()

    elif arg.startswith('window:'):
        raise NotImplementedError

    else:
        print("%r does not exist." % arg)
        raise SystemExit

    # do upload
    print("Uploading %s as %s..." % (filename, email))
    url = upload_drop(filename, email, password)
    print("View at %s" % url)

    # copy cl.ly url to clipboard
    write_clipboard(url)
    print("URL copied to clipboard.")


if __name__ == '__main__':
    main()
