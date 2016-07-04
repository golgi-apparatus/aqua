#!/usr/bin/python3
# -*-coding:utf-8 -*
import re, requests, sys, json, argparse

parser = argparse.ArgumentParser(description="Create a short link for given URL on waa.ai")
parser.add_argument('-c', '--custom', help='Create a custom link' +
                    '(must be between 5 and 30 characters long)')
parser.add_argument('-p','--private', help='Create a private link',
                    action='store_true')
parser.add_argument('-i', '--info', help='Get info for given url code')
parser.add_argument('url', nargs='?')
args = parser.parse_args()

valid_url = '^(http|https|ftp):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?$'
if args.url and not re.match(valid_url, args.url):
    sys.exit('\nNot a valid URL.\n')

if not args.url and not args.info:
    parser.print_help()
    sys.exit()

def request_short(url):
    r = requests.get('http://api.waa.ai/shorten?url=' + url + key)
    parsed = json.loads(r.text)
    success = parsed['success']

    if not success:
        if args.custom:
           sys.exit('\nRequest failed. Custom URL may already exist.\n')
        else:
            sys.exit('Request failed.')

    return parsed['data']['url']

def request_info(code):
    r = requests.get('http://api.waa.ai/info/' + code)
    parsed = json.loads(r.text)
    success = parsed['success']

    if not success:
        sys.exit('\nCould not request info. Verify if the given code really exists.\n')

    clicks = str(parsed['data']['clicks'])
    last = parsed['data']['last_visited']
    created = parsed['data']['date_created']
    long = parsed['data']['long_url']

    if last is None:
        last = 'Never'

    return ('\nShort URL: http://waa.ai/' + code + '\nFull URL: ' + long + '\nClicks: ' +
            clicks + '\nLast visited: ' + last + '\nDate created: ' + created + '\n')

if args.private:
    key = '&private=true'
elif args.custom:
    if len(args.custom) < 5 or len(args.custom) > 30:
        sys.exit('\nCustom url must be between 5 and 30 characters long\n')
    key = '&custom=' + args.custom
elif args.info:
    print(request_info(args.info))
else:
    key = ''

if not args.info:
    print(request_short(args.url))