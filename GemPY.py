#!/usr/bin/env python3
import requests
import re
import base64
from urllib.parse import unquote
import json
import time
import threading
import sys
my_version = "v1.0"


gems_count = 0
def get_gems(uid):
    global gems_count
    url='https://securityheaders.com/?q=http%3A%2F%2Fembed.jungroup.com%2Fembedded_videos%2Fcatalog_frame%3Fuid%3D' + uid + '%26site%3DOurWorld-Special%26pid%3D2777179&followRedirects=on'

    rounds=0
    while True:
        response = requests.get(url)
    
    
        try:
            trampoline = re.search('trampoline=(.+?)&amp', str(response.text)).group(1)
            trampoline = json.loads(base64.b64decode(str(unquote(trampoline))).decode('utf-8'))
            if 'step_count' in trampoline:
                wait = trampoline['step_count'] * trampoline['visit_length'] + 2
            else:
                wait = trampoline['video_length'] + 2

            #
            rounds += 1
            
            print("Round No:" + str(rounds) + " completes in " + str(wait) + " seconds giving " + trampoline['reward_text'])
            
            time.sleep(wait)
            
            completion = requests.post("https://embed.jungroup.com/offer_completion/complete", data = {
                    'token':trampoline['token'],
                    'distributorid':'2777179',
                    'uid':uid,
                    'viewing_id':trampoline['viewing_id'],
                    'reward_token':trampoline['reward_token']
                    })
            gems_count = gems_count + trampoline['reward_quantity']
            print("Total Gems collected:" + str(gems_count))
            #print(completion.status_code)
            #print(completion.content)

        except Exception as e:
            break

def check_version(version):
    try:
        req = requests.get(
            "https://raw.githubusercontent.com/khanxbahria/GemPY/master/version", timeout=5)
    except:
        print("[Exit]", "No Internet Connection!")
        sys.exit()
    if req.status_code == 404:
        print(
            "[Exit]", "This project is no longer maintained!")
        sys.exit()

    latest = req.text.strip()
    if version != latest:
        print(
            "[Exit]", "Version outdated!\nPlease update.")
        sys.exit()

def banner():
    print("  /$$$$$$                          /$$$$$$$  /$$     /$$")
    print("/$$__  $$                        | $$__  $$|  $$   /$$/")
    print("| $$  \\__/  /$$$$$$  /$$$$$$/$$$$ | $$  \\ $$ \\  $$ /$$/ ")
    print("| $$ /$$$$ /$$__  $$| $$_  $$_  $$| $$$$$$$/  \\  $$$$/  ")
    print("| $$|_  $$| $$$$$$$$| $$ \\ $$ \\ $$| $$____/    \\  $$/   ")
    print("| $$  \\ $$| $$_____/| $$ | $$ | $$| $$          | $$    ")
    print("|  $$$$$$/|  $$$$$$$| $$ | $$ | $$| $$          | $$    ")
    print("\\______/  \\_______/|__/ |__/ |__/|__/          |__/    ")
    print("")
    print("")
    print("Gem Miner for ourWorld")
    print("OW user: lolmode42")
    print("https://github.com/khanxbahria/GemPY/")
    print("")
    print("")

    
if __name__=='__main__':
    banner()
    check_version(my_version)
    print("[!] Never run more than one instance for the same uid at the same time.")
    try:
        my_uid = input("uid: ")
    except KeyboardInterrupt:
        sys.exit()
    try:
        int(my_uid)
    except ValueError:
        print("Invalid uid!")
        input("")
        sys.exit()

    if len(my_uid) > 9 or len(my_uid) < 6:
        print("Invalid uid!")
        input("")
        sys.exit()

    p1 = threading.Thread(target=get_gems, args=(my_uid,))
    p1.start()
    time.sleep(2)
    p2 = threading.Thread(target=get_gems, args=("0"+ my_uid,))
    p2.start()
    p1.join()
    p2.join()
    print(f"{gems_count} gems collected")
    print("Done!")
    input("")

     
