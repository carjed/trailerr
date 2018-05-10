## Overview

Trailerr is a program for snatching the latest cinema trailers and integrating into your Plex media server.

## Quick Start

Clone this git repository and install the following Python libraries using pip or conda. 

- `youtube-dl`
- `ffmpeg-python`
- `yaml`

Update your configuration in the included `config.yaml` file, then run 

```
python trailerr.py --config /path/to/config.yaml
```

## Tutorial

### Set download directory
Update the `trailer_dir:` field of `config.yaml` to the directory where you will store your trailers.

### Playlist selection
By default, the program is configured to grab the latest 10 videos from each of the genre-specific trailer playlists from the [Fandango Movieclips channel](https://www.youtube.com/user/movieclipsTRAILERS/playlists). Playlist URLs are specified under the `pl_urls:` field. Comment out any genres you don't want to see.

The number of videos per playlist can be changed in the `ntrailers_dl:` field. For initial setup, you will probably want to use the default (10). Depending on how frequently the playlist is updated (and how often you are running the script), it might make sense to lower this value.

Filename parsing is currently configured specifically for the Movieclips playlists--as of 2017, most titles uploaded by Movieclips are something like "Movie Title Trailer #1 (YEAR) | Movieclips Trailers". For better integration with the Plex metadata agents, Trailerr will attempt to name the downloaded files in the following format: "Movie Title (YEAR).mp4"

### Specifying video quality
You can specify the video and audio quality of the downloaded trailers using the standard youtube-dl quality codes, as specified in the `format:` field of the config file. The default is "137+140" which grabs videos encoded in mp4 at 1920x1080 resolution with a 128kbps mp3 audio stream. Note that if you are using a different playlist, the default quality code may not be available.

### Trimming the crap
The trailers uploaded by the Movieclips YouTUbe channel include a 10-second bumper at the end so they can flash a bunch of ads/links. The `trim_secs: N` option will force the script to run ffmpeg (using the `ffmpeg-python` library) on the downloaded trailer and remove the last 10 seconds, sending output to something like "Movie Title (YEAR).mp4". Once complete, the temporary video file [youtubeID.mp4] will be deleted.

If you are using other playlists with their own bumpers, just change the time accordingly.

Note that trimming video with ffmpeg is a processor-intensive task and requires the video to be re-encoded, so this can take a while depending on how many trailers you are downloading and how powerful your server is. If for any reason you want to disable the truncation, simply set `trim_secs: 0` in the config. 

### Removing old trailers
Although you can use this script to hoard as many trailers as you want, in most cases you will want to delete trailers as they age. Set the number of days you wish to keep trailers using the `timelim:` field. Set to 0 to never auto-delete downloaded trailers.

### Automating downloads
You will probably want automate this script to regularly grab new trailers and delete those that have come and gone. The simplest solution is to set up a cron job running this script every day or so to check for new trailers and see if there are any old ones to delete.

#### Random symlinking for custom trailers in Plex
Once trailers have been downloaded to your specified directory, the script will randomly create symlinks to 3 trailers. Set up a cron job to run this script every hour or so to rotate the linked trailers (use the `--skipdownloads` option to skip the playlist checking/downloading and just refresh the symlinks).

Change the number of trailers to link in the `ntrailers_ln:` field. 

You can also change the prefix of the symlinks to something other than `trailerN` using the `ln_prefix:` field.

#### Plex setup
Once the symlinks have been created, you can simply add them to your Plex pre-roll list, effectively replicating the Plex Pass Cinema Trailers feature, but using only the trailers that you've downloaded.

To do so, go to **Settings >> Server >> Extras** and put the paths to the symlinks (separated by commas) in the "Cinema Trailers pre-roll video" field:

`/path/to/trailer1.mp4,/path/to/trailer2.mp4,/path/to/trailer3.mp4`

Note that if you wish to include other custom pre-roll videos, they should be placed after the list of trailer paths.

If you have automated the script to reshuffle the symlinks, the next time you start a movie, you should be greeted with 3 new trailers from your trailer library.

##### Trailer Libraries
Another perk of downloading trailers locally is that you can create a Plex video library and browse through them as you would any other media collection.

Simply create a new library and point it to the directory on your server where you store the trailers. The Plex Movie and Movie Database metadata agents should be able to pull in metadata for most trailers, provided the filenames are properly formatted (YMMV if you want to use unsupported playlists).

Note that because trailers grabbed from YouTube have no embedded metadata, the metadata agents may not always work. 

Also, make sure to disable the "Enable Cinema Trailers" option under **Library >> Edit >> Advanced**, otherwise your server-wide pre-roll will run before every trailer.

## FAQ 

### Why would I possibly want to download trailers for upcoming movies when Plex has this function built in?

The [Plex Pass cinema trailers feature](https://support.plex.tv/articles/202934883-cinema-trailers-extras/) is awesome in principle, but has some pretty serious flaws, IMHO. While Plex excells at streaming local media, it's still rather buggy at streaming from the internet. Moreover, users get no control over the content and quality of trailers.

This script should be useful for anyone who [wants more control over the genre and quality of trailers shown](https://www.reddit.com/r/PleX/comments/87ez9q/better_cinema_trailers/), [doesn't have a Plex Pass subscription](https://www.reddit.com/r/PleX/comments/7ho134/trailers_without_plexpass/), has Plex clients on a local network without external internet access, or wants to create a browsable and constantly-up-to-date Plex library of movie trailers.

### Can I use this without a Plex Pass subscription?

Yep, as long as the pre-roll remains a free feature, you can watch trailers without paying a dime to the Plex developers. 

### I only want to view trailers from my favorite independent Bollywood anime studio, can I still use this?

As long as they make a YouTube playlist.

## Upcoming Features
- webUI for managing source playlists, trailer libraries, and recurring jobs (a la Sonarr/Radarr/Headphones)
- support for non-YouTube sources
