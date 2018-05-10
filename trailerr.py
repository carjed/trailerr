import os
import random
import time
import datetime
import sys
import argparse
import yaml
import ffmpeg
import youtube_dl
import subprocess

###############################################################################
# function to get existing trailer length (timestamp) using ffprobe
# from https://stackoverflow.com/questions/3844430
###############################################################################
def getLength(filename):
  result = subprocess.Popen(["ffprobe", filename],
    stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  return [x for x in result.stdout.readlines() if b"Duration" in x]

###############################################################################
# exclude hidden files from listdir command
# from https://stackoverflow.com/questions/7099290
###############################################################################
def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

###############################################################################
# Input options
###############################################################################
parser = argparse.ArgumentParser()

parser.add_argument("-c", "--config",
                    help="path to config.yaml. \
                        Defaults to current working directory.",
                    nargs='?',
                    type=str,
                    metavar='',
                    default="config.yaml")

parser.add_argument("-b", "--blacklist",
                    help="path to file of blacklisted releases",
                    nargs='?',
                    type=str,
                    metavar='',
                    default="")

parser.add_argument("-s", "--skipdownloads",
                    help="Skip attempt to download from playlist. Use this \
                        option if you already have trailers in your directory \
                        and just want to reshuffle the softlinks.",
                    action="store_true")

args = parser.parse_args()

with open(args.config, "r") as f:
    config = yaml.load(f)

if args.blacklist:
    with open(args.blacklist) as f:
        blacklist = f.read().splitlines()

os.chdir(config['trailer_dir'])

###############################################################################
# remove linked trailers
###############################################################################
trailers = listdir_nohidden(config['trailer_dir'])

print("-" * 40)
print("Removing symlinks...")
for trailer in trailers:
    if trailer.startswith(config['ln_prefix']):
        print(" - ", trailer)
        os.remove(os.path.join(config['trailer_dir'], trailer))

###############################################################################
# remove old trailers
###############################################################################
now = time.time()
trailers = listdir_nohidden(config['trailer_dir'])

if config['timelim'] > 0:
    print("-" * 40)
    print("Deleting trailers older than", str(config['timelim']), "days...")
    
    counter = 0
    for trailer in trailers:
        if (os.stat(trailer).st_mtime < now - config['timelim'] * 86400) and (os.path.isfile(trailer)):
            if not trailer.startswith("preroll"):
                os.remove(os.path.join(config['trailer_dir'], trailer))
                counter += 1
                
    print(" - ", counter, "trailers deleted")

###############################################################################
# randomly select trailers to download
###############################################################################
if not args.skipdownloads:
    
    dl_count = 0
    have_count = 0
    
    print("-" * 40)
    print("Scanning playlist URLs for new trailers...")
    for url in config['pl_urls'].values():
        
        # Get IDs of trailers in playlist
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s',
                            'restrictfilenames': True,
                           'playliststart': 1,
                           'playlistend': config['ntrailers_dl'],
                            'format': config['format'],
                           'quiet': True})

        with ydl:
            result = ydl.extract_info(
                url,
                download=False
            )
        
        for item in result['entries']:
        #     print(item.keys())
            # print(item['format'])
            # print(item['id'])
            print("-" * 40)
            print("Checking if we need to download " + item['title'])
            trimmed_title = item['title'].split(" |", 1)[0]
            trimmed_title = trimmed_title.replace(":", " -")
            trimmed_title = trimmed_title.replace(" Final Trailer", "")
            trimmed_title = trimmed_title.replace(" Teaser Trailer #1", "")
            trimmed_title = trimmed_title.replace(" Trailer #1", "")
            trimmed_title = trimmed_title.replace(" Trailer #2", "")
            # print(trimmed_title)
            
            trimmed_dur = item['duration']-config['trim_secs']
            runtime = time.strftime('%H:%M:%S', time.gmtime(trimmed_dur))
            
            input_trailer = item['id'] + ".mp4"
            output_trailer = trimmed_title + ".mp4"
            
            if not os.path.isfile(output_trailer):
                
                # config for downloading
                ydl_snatch = youtube_dl.YoutubeDL({'outtmpl': '%(id)s',
                                       'playliststart': 1,
                                       'playlistend': config['ntrailers_dl'],
                                        'format': config['format'],
                                       'quiet': True})
        
                print("Downloading " + trimmed_title + "...")
                dl = ydl_snatch.download([item['id']])
                
                # if trim option is set in config, trim with ffmpeg
                if config['trim_secs']>0:
                    print("Trimming " + trimmed_title + "...")
            
                    (ffmpeg
                        .input(input_trailer, ss='00:00:00', t=runtime)
                        .output(output_trailer)
                        .run(overwrite_output=True)
                    )
                    
                    print("Removing temporary file " + input_trailer)
                    os.remove(input_trailer)
                # if trim option set to 0, just rename the temp file
                else:
                    print("Renaming " + input_trailer + " to " + output_trailer)
                    os.rename(input_trailer, output_trailer)
                dl_count += 1

            else:
                print(output_trailer + " already exists")
                have_count += 1
    
    print("Playlist scan complete!")
    print("items downloaded: " + str(dl_count))
    print("items already in directory: " + str(have_count))

###############################################################################
# Randomly select 3 trailers and soft link
###############################################################################
# print("-" * 40)
# print("Generating new symlinks...")

trailers = list(listdir_nohidden(config['trailer_dir']))

# check blacklist for titles to exclude
if args.blacklist:
    print("-" * 40)
    print("Checking for blacklisted trailers...")
    for trailer in trailers:
        for bl in blacklist:
            if bl.lower() in trailer.lower():
                trailers.remove(trailer)
                print(" - Blacklisting " + trailer)
                
    print("Blacklisted trailers may still exist in", config["trailer_dir"], "but will be excluded from symlinks")

random.shuffle(trailers)

print("-" * 40)
print("Generating symlinks...")
for i in range(0,config['ntrailers_ln']):
    ln_name = config['ln_prefix'] + str(i) + ".mp4"
    os.symlink(trailers[i], ln_name)
    print(" - " + ln_name + " --> " + trailers[i])
