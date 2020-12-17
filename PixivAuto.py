help = """
Usage:
  PixivAuto.py (pull | download)
  PixivAuto.py (push | upload) --clean
  PixivAuto.py twitter
  PixivAuto.py pics
  PixivAuto.py (-h | --help)

Options:
  -h --help     Show this screen.
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
                print(f'Uploading new images from {artistName}')
                
                start = timer()
                arguments = f'{artistID} {RemotePath}/{artistName}'
                run([r'rclone', 'copy'] + shlex.split(arguments))   # by default: copies the artist folders to a set remote folder (variable RemotePath above)
                end = timer()
                final_time = round(end) - round(start)

                if final_time >= 60:
                    final_time = final_time / 60
                    if final_time > 1:
                        print(f'Upload finished for {artistName} in {final_time} minutes')
                    else:
                        print(f'Upload finished for {artistName} in {final_time} minute')
                else:
                    if final_time > 1:
                        print(f'Upload finished for {artistName} in {final_time} seconds')
                    else:
                        print(f'Upload finished for {artistName} in {final_time} second')

                if argv[2] == "--clean":
                    shutil.rmtree(f'./{artistID}')
                else:
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
    run(['py', f'{PixivUtil2}/PixivUtil2.py', '-n', '1', '-x', '-s', '1', 'n', *lst])

def pull():
    chunkSize = 8
    groups = chunks(artistList.keys(), chunkSize)
    threads = [Thread(target=pullThread, args=[group]) for group in groups]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

try:
    arguments = argv[1]
except:
    exit(help)

if arguments == "push" or arguments == "upload":
    push()
elif arguments == "pull" or arguments == "download":
    pull()
elif arguments == "-h" or "--help":
    exit(help)
else:
    exit(help)