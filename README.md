# PixivAuto

## What is it?

PixivAuto is a personal project I started to automate a few commands I used to run almost on a daily-basis to download and upload Pixiv images from a list of artists to my Onedrive, using rclone and PixivUtil2 to 
accomplish both tasks. I took this project as a chance to improve my Python skills, and it is slowly getting polished over time. Do not expect anything great from it, it exists to serve a very specific reason.

### Does it replace PixivUtil2 and/or rclone?

Nope! PixivAuto is meant to be nothing more than a substitute of human hands, macros, crons or whatever for both tools. In fact, you cannot pull images from Pixiv without PixivUtil2 and cannot push images to a remote server without rclone. You can, however, use only one of the dependencies if the rest of the tool does not matter for you.

## Dependencies

- [rclone](https://rclone.org/)
- [PixivUtil2 (source code)](https://github.com/Nandaka/PixivUtil2/)
- Python 3.7 or higher
- docopt
  - run ``pip install docopt``

## Usage

From the command line:

```shell
Usage:
  PixivAuto.py (pull | download)    # check for new images from the artists in pixiv.json
  PixivAuto.py (push | upload)      # upload images to remote server using rclone (uses pixiv.json)
  PixivAuto.py (-h | --help)
```

> Protip: I prefer to have this script running on $PATH. This way I can invoke it anywhere in my system.

### JSON structure

The script uses a very simple JSON that is similar to a Python dictionary. Here is an example:

```json
{
    "123456789" : "folder-name",
    "987654321" : "folder-name2",
    "852741963" : "folder-name3"
}
```

Where ``123456789`` is the artist ID (from their Pixiv url) and ``name`` is the remote folder they are going to be uploaded to. I personally keep these as the artist names.

> Protip: it's preferable to keep your PixivUtil2 filename settings as ``%member_id%\%urlFilename%``, since artist IDs **will never** change (unless they delete their profile). Keeping it as profile names will render this tool mostly useless since a lot of artists change their names to match events dates and locations (such as ``わたお@2日目南3 ナ-37b``, where everything after the ``@`` is event info).

### Configuration

By default, the script is useless. You need to open it in any text editor (a good one, I hope) and edit a few variables:

```python
# Use absolute paths (C:/example/pixiv.json) if you plan to add this tool to your $PATH
PixivInput = "."                               # list of artists | e.g.: C:/PixivAuto/pixiv.json or /home/user/PixivAuto/pixiv.json
PixivUtil2 = "./PixivUtil2"                    # PixivUtil2 source code path | e.g.: C:/PixivUtil2/PixivUtil2.py or /home/user/PixivUtil2/PixivUtil2.py
RemotePath = "remote:destpath"                 # rclone remote | e.g. onedrive:MyPictures/Hentai/
```

You can also customize a some of the commands ran by rclone and PixivUtil2 in the following sections:

#### rclone

```python
# by default: copies the artist folders to a set remote folder (variable RemotePath above)
arguments = f'{artistID} {RemotePath}/{artistName}'
```

#### PixivUtil2

```python
# by default: downloads images from FIRST PAGE of the artists in pixiv.json and closes PixivUtil2 after the process is done
arguments = f'-n 1 -x --startaction=1 {cleanID}'
```

Please refer to each tool's manual before doing any changes. A basic knowledge of Python 3 and its [subprocess](https://docs.python.org/3/library/subprocess.html#older-high-level-api) module is also necessary.

## Contributions

I prefer to not take any contributions for this repo. You are free to fork it and make it better, but please don't let me know that. I'm lazy and I'll probably stop doing it if there's a better option.

This is a pet project, something I'm doing to improve my Python skills and test new stuff. You might find weird stuff in the code, and that's actually intended. The plan is to cram as much as I know in there, even if there are simpler ways of doing it. I hope to keep polishing it over time.

## Bugs, issues, improvements

Things that need to be fleshed out:

- UNIX support
  - I have no idea if it really works outside of Windows. Probably does.
- Upload timer
  - If you are uploading a large folder from any user, it will always display time in seconds. I hope you are good at math.
