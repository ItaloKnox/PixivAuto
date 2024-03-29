help = """
Usage:
  PixivAuto.py (pull | download)
    * check for new images from artists added in pixiv.json

  PixivAuto.py (push | upload) --clean
    * uploads files to remote. "--clean" flag deletes uploaded folders (warning: upload errors will result in data loss)

  PixivAuto.py check <ID or name>
    * checks if an ID or artist (remote folder name) exists in pixiv.json. If found, the line will be printed
        * example: pixivauto check asanagi
        * example: pixivauto check 129381

  PixivAuto.py add <ID> <name>
    * adds artist to the json list
        * example: pixivauto add asanagi 129381

  PixivAuto.py --show-list
    * prints the entire pixiv.json file

  PixivAuto.py (-h | --help)
    * shows this screen
"""

import os, json, re, shlex, shutil
from subprocess import run
from timeit import default_timer as timer
from sys import argv

# Use absolute paths (C:/example/pixiv.json) if you plan to add this tool to your $PATH
PixivInput = "."                               # list of artists | e.g.: C:/PixivAuto/pixiv.json or /home/user/PixivAuto/pixiv.json
PixivUtil2 = "./PixivUtil2"                    # PixivUtil2 source code path | e.g.: C:/PixivUtil2/PixivUtil2.py or /home/user/PixivUtil2/PixivUtil2.py
RemotePath = "remote:destpath"                 # rclone remote | e.g. onedrive:MyPictures/Hentai/

with open(f'{PixivInput}/pixiv.json', 'r') as f:
    artistList = json.load(f)

def push():
    for artistID, artistName in artistList.items():
        artistExist = os.path.isdir(f'./{artistID}')
        if artistExist == True:
                print(f'Uploading new images by {artistName} (ID: {artistID})')
                
                start = timer()
                arguments = f'{artistID} {RemotePath}/{artistName}'
                run([r'rclone', 'copy'] + shlex.split(arguments))   # by default: copies the artist folders to a set remote folder (variable RemotePath above)
                end = timer()
                final_time = round(end) - round(start)

                if final_time >= 60:
                    final_time = final_time / 60
                    if final_time > 1:
                        print(f'Finished uploading {artistName} in {final_time} minutes')
                    else:
                        print(f'Finished uploading {artistName} in {final_time} minute')
                else:
                    if final_time > 1:
                        print(f'Finished uploading {artistName} in {final_time} seconds')
                    else:
                        print(f'Finished uploading {artistName} in {final_time} second')

                try:
                    if argv[2] == "--clean":
                        shutil.rmtree(f'./{artistID}')
                except:
                    pass

        else:
            pass

def chunks(iterable, count):
    iterator = iter(iterable)
    lst = []
    try:
        while True:
            for _ in range(count):
                lst.append(next(iterator))
            yield lst
            lst = []
    except StopIteration:
        if lst:
            yield lst

from threading import Thread
def pullThread(lst):
    # by default: downloads images from FIRST PAGE of the artists in pixiv.json and closes PixivUtil2 after the process is done
    run(['py', f'{PixivUtil2}/PixivUtil2.py', '-n', '1', '-x', '-s', '1', *lst])

def pull():
    num = sum(1 for line in open(f'{PixivInput}/pixiv.json'))
    # change the number below (default: 5) to create more threads. By default, the program divides your list in 5 threads to avoid flooding the machine with Python instances. More threads = more CPU usage.
    chunkSize = num / 5
    roundChunk = round(chunkSize)
    groups = chunks(artistList.keys(), roundChunk)
    threads = [Thread(target=pullThread, args=[group]) for group in groups]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def check():
    try:
        search = argv[2]
    except:
        exit(help)
    
    file = open(f'{PixivInput}/pixiv.json', "r")
    for line in file:
        if re.search(search, line):
            print(line)
        # else:
        #     print("Artist/ID not found")

def add():
    try:
        artistID = argv[2]
    except:
        artistID = input("Pixiv Artist ID (numbers from url): ")
    
    try:
        artistName = argv[3]
    except:
        artistName = input("Name of the artist (ANSI only, no spaces): ")

    add_input = {artistID : artistName}

    with open(f'{PixivInput}/pixiv.json', 'r') as pixiv_json:
        data = json.load(pixiv_json)
        data.update(add_input)

    with open(f'{PixivInput}/pixiv.json', 'w') as pixiv_json:
        json.dump(data, pixiv_json, indent=4)

def showList():
    with open(f'{PixivInput}/pixiv.json', 'r') as pixiv_json:
        data = json.load(pixiv_json)
        print(json.dumps(data, indent=4))
        pixiv_json.close()

try:
    arguments = argv[1]
except:
    exit(help)

if arguments == "push" or arguments == "upload":
    push()
elif arguments == "pull" or arguments == "download":
    pull()
elif arguments == "check":
    check()
elif arguments == "add":
    add()
elif arguments == "--show-list":
    showList()
elif arguments == "-h" or "--help":
    exit(help)
else:
    exit(help)
