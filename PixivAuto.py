"""
Usage:
  PixivAuto.py (pull | download)
  PixivAuto.py (push | upload)
  PixivAuto.py (-h | --help)

Options:
  -h --help     Show this screen.
"""

import os, json, re, shlex
from subprocess import run
from timeit import default_timer as timer
from docopt import docopt

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
                    print(f'Upload finished for {artistName} in {final_time} minute(s)')
                else:
                    print(f'Upload finished for {artistName} in {final_time} second(s)')
        else:
            pass

def pull():
    artistID = re.findall(r'[0-9]\d+', str(artistList.keys()))
    cleanID = ' '.join(artistID)
    arguments = f'-n 1 -x --startaction=1 {cleanID}'    # by default: downloads images from FIRST PAGE of the artists in pixiv.json and closes PixivUtil2 after the process is done

    run([r'py', f'{PixivUtil2}/PixivUtil2.py'] + shlex.split(arguments))

if __name__ == '__main__':
    arguments = docopt(__doc__)

    if arguments['push'] or arguments['upload']:
        push()
    elif arguments['pull'] or arguments['download']:
        pull()