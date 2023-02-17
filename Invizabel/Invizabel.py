from b64_crack import *
from tor_v3 import *

from cryptography.hazmat.primitives.asymmetric import ed25519
import argparse
import base64
import hashlib
import os
import re
import requests
import sys
import threading
import time

#initialize parser
og_parser = argparse.ArgumentParser(prog = "Invizabel")

#tools
og_parser.add_argument("--b64_crack", dest = "b64_crack", type = bool, required = False, help = "[tool]: Cracks base64")
og_parser.add_argument("--tor_v3", dest = "tor_v3", type = bool, required = False, help = "[tool]: Generates and visits tor V3 links.")

#parameters
og_parser.add_argument("--file", dest = "file", type = str, required = False, help = "[parameter]: Name of the output file.")
og_parser.add_argument("--threads", dest = "threads", type = int, required = False, help = "[parameter]: Number of threads to use.")
og_parser.add_argument("--vanity", dest = "vanity", type = str, required = False, help = "[parameter]: Search for string in url.")
og_parser.add_argument("--verbose", dest = "verbose", type = bool, required = False, help = "[parameter]: Displays urls that are being checked.")
og_parser.add_argument("--verify", dest = "verify", type = str, required = False, help = "[parameter]: Verify connection once every minute against a known onion site.")

#parse parameters
args = og_parser.parse_args()

if args.b64_crack == True:
    b64_crack()

if args.tor_v3 == True:
    tor_v3_main(args.file, args.threads, args.verify, args.vanity, args.verbose)
