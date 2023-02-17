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

#tool
if args.b64_crack == True:
        value = input("Enter value:\n").encode()

        for i in range(1000000):
                try:
                        value = base64.b64decode(value)

                except:
                        clean = str(value).replace("b'", "")
                        clean = clean.replace("'", "")
                        print(clean)
                        print("attempts: " + str(i))
                        break

#tool
def tor_v3():
        tor_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"}
        tor_proxy = {"http": "socks5h://localhost:9050", "https": "socks5h://localhost:9050"}
        os.system("clear")

        while True:
                if threading.active_count() <= args.threads + 1 and args.verify != None:
                        sys.exit()
                        
                duplicate = False

                public = ed25519.Ed25519PrivateKey.generate().sign(b"")[:32]
                checksum = hashlib.sha3_256(b".onion checksum" + public + b"\x03").digest()[:2]
                result = "http://" + base64.b32encode(public + checksum + b"\x03").decode().lower() + ".onion"

                if args.vanity == None:
                        if args.verbose == True:
                                print("checking: " + result)

                        try:
                                my_request = requests.get(result, headers = tor_agent, proxies = tor_proxy, timeout = (60, 120), verify = False).text
                                title = re.findall("<title>(.+)</title>", my_request)

                                try:
                                        print(title[0] + ": " + result)

                                        if args.file != None:
                                                with open(args.file, "r") as f:
                                                        for i in f:
                                                                if str(title[0] + ": " + result) == i:
                                                                        duplicate = True
                                                                        print("Duplicate found.")
                                                                        break

                                                if duplicate == False:
                                                        with open(args.file, "a") as f:
                                                                f.write(title[0] + ": " + result + "\n")

                                except IndexError:
                                        print("UNTITLED: " + result)

                                        if args.file != None:
                                                with open(args.file, "r") as f:
                                                        for i in f:
                                                                if str(title[0] + ": " + result) == i:
                                                                        duplicate = True
                                                                        print("Duplicate found.")
                                                                        break
                                                                
                                                if duplicate == False:
                                                        with open(args.file, "a") as f:
                                                                f.write("UNTITLED: " + result + "\n")

                        except:
                                pass

                if args.vanity != None:
                        if args.vanity in base64.b32encode(public + checksum + b"\x03").decode().lower():
                                if args.verbose == True:
                                        print("checking: " + result)

                                try:
                                        my_request = requests.get(result, headers = tor_agent, proxies = tor_proxy, timeout = (60, 120), verify = False).text
                                        title = re.findall("<title>(.+)</title>", my_request)

                                        try:
                                                print(title[0] + ": " + result)

                                                if args.file != None:
                                                        with open(args.file, "r") as f:
                                                                for i in f:
                                                                        if str(title[0] + ": " + result) == i:
                                                                                duplicate = True
                                                                                print("Duplicate found.")
                                                                                break

                                                        if duplicate == False:
                                                                with open(args.file, "a") as f:
                                                                        f.write(title[0] + ": " + result + "\n")

                                        except IndexError:
                                                print("UNTITLED: " + result)

                                                if args.file != None:
                                                        with open(args.file, "r") as f:
                                                                for i in f:
                                                                        if str(title[0] + ": " + result) == i:
                                                                                duplicate = True
                                                                                print("Duplicate found.")
                                                                                break

                                                        if duplicate == False:
                                                                with open(args.file, "a") as f:
                                                                        f.write("UNTITLED: " + result + "\n")

                                except:
                                        pass

def tor_v3_verify():
        tor_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"}
        tor_proxy = {"http": "socks5h://localhost:9050", "https": "socks5h://localhost:9050"}

        while True:
                time.sleep(60)

                try:
                        print("Checking connection.")
                        requests.get(args.verify, headers = tor_agent, proxies = tor_proxy, timeout = (60, 120), verify = False)
                        print("Verified connection.")

                except:
                        print("Verify failed. Shuting down.")
                        break

        sys.exit()

if args.tor_v3 == True:
        if args.threads == None:
                args.threads = 1

        if args.verify != None:
                threading.Thread(target = tor_v3_verify).start()

        for i in range(args.threads):
                threading.Thread(target = tor_v3).start()
