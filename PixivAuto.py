"""
Usage:
  PixivAuto.py (pull | download)
  PixivAuto.py (push | upload)
  PixivAuto.py (-h | --help)

Options:
  -h --help     Show this screen.
"""

import os, json, re, shlex
from subprocess import call
from timeit import default_timer as timer
from docopt import docopt

# Use absolute paths (C:/example/pixiv.json) if you plan to add this tool to your $PATH
PixivInput = "./pixiv.json"         # list of artists | e.g.: C:/PixivAuto/pixiv.json or /home/user/PixivAuto/pixiv.json
PixivUtil2 = "./PixivUtil2.py"      # PixivUtil2 source code path | e.g.: C:/PixivUtil2/PixivUtil2.py or /home/user/PixivUtil2/PixivUtil2.py
RemotePath = "remote:destpath/"         # rclone remote | e.g. onedrive:MyPictures/Hentai/

with open(PixivInput, 'r') as f:
    artistList = json.load(f)

def push():
    for artistID, artistName in artistList.items():
        artistExist = os.path.isdir(f'./{artistID}')
        if artistExist == True:
                print(f'Uploading new images from {artistName}')

                start = timer()
                call([r'rclone', 'copy', f'{artistID}', f'{RemotePath}{artistName}'])   # by default: copies the artist folders to a set remote folder (variable RemotePath above)
                end = timer()
                final_time = round(end) - round(start)

                print(f'Upload finished for {artistName} in {final_time} seconds')
        else:
            pass

def pull():
    artistID = re.findall(r'[0-9]\d+', str(artistList.keys()))
    cleanID = ' '.join(artistID)
    arguments = f'-n 1 -x --startaction=1 {cleanID}'    # by default: downloads images from FIRST PAGE of the artists in pixiv.json and closes PixivUtil2 after the process is done

    call([r'py', f'{PixivUtil2}'] + shlex.split(arguments))

if __name__ == '__main__':
    arguments = docopt(__doc__)

    if arguments['push'] or arguments['upload']:
        push()
    elif arguments['pull'] or arguments['download']:
        pull()