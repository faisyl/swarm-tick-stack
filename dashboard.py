import requests
import json
import pprint
import argparse
import sys


def url_prefix(url):
    ret = "http://"
    try:
        requests.get(ret + url)
    except Exception as fault:
        ret = "https://"
    return ret

def list_dashboards(args):
    resp = requests.get(url_prefix(URL) + URL, verify=False)
    ret = {}
    if resp.ok:
        data = json.loads(resp.content)
        print("{}\t{}".format("ID", "Dashboard Name"))
        print("{}\t{}".format("--", "--------------"))
        for d in data['dashboards']:
            ret[d['id']] = d['name']
            print("{}\t{}".format(d['id'], d['name']))

def dump_dashboard(args):
    resp = requests.get("{}{}/{}".format(url_prefix(URL), URL, args.id), verify=False)
    if resp.ok:
        if args.f:
            ofile = open(args.f, "w")
        else:
            ofile = sys.stdout
        try:
            ofile.buffer.write(resp.content)
        finally:
            ofile.close()

def load_dashboard(args):
    if args.f:
        ifile = open(args.f, "r")
    else:
        ifile = sys.stdin
    data = ifile.read()
    headers = {"Accept": "application/json"}
    resp = requests.post(url_prefix(URL) + URL, data=data, headers=headers, verify=False)
    if resp.ok:
        print("Loaded OK")


parser = argparse.ArgumentParser(description='Manage chronograf dashboards')
parser.add_argument('--host', dest='host', action='store',
                    default="localhost",
                    help='Set hostname to connect to (default: localhost)')
parser.add_argument('--port', dest='port', action='store',
                    default="8888",
                    help='Set port to connect to (default: 8888)')

subparsers = parser.add_subparsers(help='Command to execute', dest='CMD')
subparsers.required = True
# List
parser_list = subparsers.add_parser('list', help='List available dashboards')
parser_list.set_defaults(func=list_dashboards)

# Dump
parser_dump = subparsers.add_parser('dump', help='Dump dashboard by ID to STDOUT')
parser_dump.add_argument('id', help='ID of dashboard to dump.')
parser_dump.add_argument('-f', help='Filename to dump to. Default: STDOUT')
parser_dump.set_defaults(func=dump_dashboard)

# Load
parser_load = subparsers.add_parser('load', help='Load dashboard from STDIN')
parser_load.add_argument('-f', help='Filename to read from. Default: STDIN')
parser_load.set_defaults(func=load_dashboard)
args = parser.parse_args()

HOST = args.host
PORT = args.port

URL="{}:{}/chronograf/v1/dashboards".format(HOST, PORT)

args.func(args)

