from cryptography.hazmat.primitives.asymmetric import ed25519
import base64
import hashlib
import multiprocessing
import re
import requests
import sys
import threading
import time

#tool
def tor_v3(file, tor_threads, tor_verify, vanity, verbose):
    tor_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"}
    tor_proxy = {"http": "socks5h://localhost:9050", "https": "socks5h://localhost:9050"}

    exit_boolean = False

    while True:
            if threading.active_count() < tor_threads + 2 and exit_boolean == True:
                print("Exiting thread.")
                sys.exit()
                
            if threading.active_count() == tor_threads + 2:
                exit_boolean = True
                
                if threading.active_count() < tor_threads + 2 and tor_verify != None:
                        print("Exiting thread.")
                        sys.exit()
                        
                duplicate = False

                public = ed25519.Ed25519PrivateKey.generate().sign(b"")[:32]
                checksum = hashlib.sha3_256(b".onion checksum" + public + b"\x03").digest()[:2]
                result = "http://" + base64.b32encode(public + checksum + b"\x03").decode().lower() + ".onion"

                if vanity == None:
                        if verbose == True:
                                print("checking: " + result)

                        try:
                                my_request = requests.get(result, headers = tor_agent, proxies = tor_proxy, verify = False).text
                                title = re.findall("<title>(.+)</title>", my_request)

                                try:
                                        print(title[0] + ": " + result)

                                        if file != None:
                                                with open(file, "r") as f:
                                                        for i in f:
                                                                if str(title[0] + ": " + result) == i:
                                                                        duplicate = True
                                                                        print("Duplicate found.")
                                                                        break

                                                if duplicate == False:
                                                        with open(file, "a") as f:
                                                                f.write(title[0] + ": " + result + "\n")

                                except IndexError:
                                        print("UNTITLED: " + result)

                                        if file != None:
                                                with open(file, "r") as f:
                                                        for i in f:
                                                                if str(title[0] + ": " + result) == i:
                                                                        duplicate = True
                                                                        print("Duplicate found.")
                                                                        break
                                                                
                                                if duplicate == False:
                                                        with open(file, "a") as f:
                                                                f.write("UNTITLED: " + result + "\n")

                        except:
                                pass

                if vanity != None:
                        if vanity in base64.b32encode(public + checksum + b"\x03").decode().lower():
                                if verbose == True:
                                        print("checking: " + result)

                                try:
                                        my_request = requests.get(result, headers = tor_agent, proxies = tor_proxy, verify = False).text
                                        title = re.findall("<title>(.+)</title>", my_request)

                                        try:
                                                print(title[0] + ": " + result)

                                                if file != None:
                                                        with open(file, "r") as f:
                                                                for i in f:
                                                                        if str(title[0] + ": " + result) == i:
                                                                                duplicate = True
                                                                                print("Duplicate found.")
                                                                                break

                                                        if duplicate == False:
                                                                with open(file, "a") as f:
                                                                        f.write(title[0] + ": " + result + "\n")

                                        except IndexError:
                                                print("UNTITLED: " + result)

                                                if file != None:
                                                        with open(file, "r") as f:
                                                                for i in f:
                                                                        if str(title[0] + ": " + result) == i:
                                                                                duplicate = True
                                                                                print("Duplicate found.")
                                                                                break

                                                        if duplicate == False:
                                                                with open(file, "a") as f:
                                                                        f.write("UNTITLED: " + result + "\n")

                                except:
                                        pass

def tor_v3_verify(tor_verify):
    tor_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"}
    tor_proxy = {"http": "socks5h://localhost:9050", "https": "socks5h://localhost:9050"}

    while True:
            time.sleep(60)

            try:
                    print("Checking connection.")
                    requests.get(tor_verify, headers = tor_agent, proxies = tor_proxy, timeout = (60, 120), verify = False)
                    print("Verified connection.")

            except:
                    print("Verify failed. Shuting down.")
                    break

    sys.exit()

def tor_v3_main(file = None, tor_threads = multiprocessing.cpu_count(), tor_verify = None, vanity = None, verbose = True):
    if tor_verify != None:
            threading.Thread(target = tor_v3_verify, args = (tor_verify,)).start()

    for i in range(tor_threads):
            threading.Thread(target = tor_v3, args = (file, tor_threads, tor_verify, vanity, verbose)).start()
