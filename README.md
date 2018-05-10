## Overview

Take control of your home theater pre-show in Plex with this customizable script for snatching the latest cinema trailers.

## Download and installation

Clone this git repository and install the following Python libraries using pip or conda. 

- `youtube-dl`
- `ffmpeg-python`
- `yaml`

Update your configuration in the included `config.yaml` file, then run 

```
python trailerr.py --config /path/to/config.yaml
```

to 

## Tutorial

Options for Trailer Snatcher are very straightforward:
- specify directory to store trailers
- select trailer playlist(s) to download
- optionally trim annoying bumpers at the end
- randomly generate symlinks
- optionally delete 

### Set download directory
Update the `trailer_dir:` field of `config.yaml` to the directory where you will store your trailers.

### Playlist selection
By default, the program is configured to grab the latest 10 videos from each of the genre-specific trailer playlists from the [Fandango Movieclips channel](https://www.youtube.com/user/movieclipsTRAILERS/playlists). Playlist URLs are specified under the `pl_urls:` field.

The number of videos per playlist can be changed in the `ntrailers_dl:` field. For initial setup, you will probably want to use the default (10). Depending on how frequently the playlist is updated (and how often you are running the script), it might make sense to lower this value.

If you will be setting up a 

Filename parsing is currently configured specifically for these playlists--as of 2017, most titles uploaded by Movieclips are something like "Movie Title Trailer #1 (2018) | Movieclips Trailers". For better integration with the Plex metadata agents

#### Specifying video quality
You can specify the video and audio quality of the downloaded trailers using the standard youtube-dl quality codes, as specified in the `format:` field of the config file. The default is "137+140" which grabs videos encoded in mp4 at 1920x1080 resolution with a 128kbps mp3 audio stream. Note that if you are using a different playlist, the default quality code may not be available. "22" is a good alternative choice.


#### Trimming the crap
The trailers uploaded by the Movieclips YouTUbe channel include a 10-second bumper at the end so they can flash a bunch of ads/links. The `trim_secs: N` option will force the script to run ffmpeg on the downloaded trailer and remove the last N seconds, sending output to something like "Movie Title Trailer #1 (2018).mp4". Once complete, the temporary video file [youtubeID.mp4] will be deleted.

If you are using other playlists with their own bumpers, just change the time accordingly.

Note that trimming video with ffmpeg is a processor-intensive task and requires the video to be re-encoded, so this can take a while depending on how many trailers you are downloading and how powerful your server is. If for any reason you want to disable the truncation, simply set `trim_secs: 0` in the config. 

#### Removing old trailers
Although you can use this script to hoard as many trailers as you want, in most cases you will want to delete trailers as they age. Set the number of days you wish to keep trailers using the `timelim:` field. Set to 0 to never auto-delete downloaded trailers.

#### Random symlinking for custom trailers in Plex
Now that you have downloaded a handful of trailers, you will need to 


See [Plex setup](#Plex-setup) for further instructions on configuring your server.

#### Automating downloads
Ultimately, the goal is to develop a trailer-specific analog to Sonarr/Radarr/Lidarr

You will probably want automate this script to regularly grab new trailers and delete those that have come and gone. I have set up two recurring cron jobs: one runs every hour to refresh the symlinks, and another runs once every three days to grab new trailers added to the YouTube playlists.


#### Plex setup

To run the 3 randomly-chosen trailers before each movie, go to **Settings >> Server >> Extras** and put the paths to the random symlinks (separated by commas) in the "Cinema Trailers pre-roll video" field:

/path/to/trailer1.mp4,/path/to/trailer2.mp4,/path/to/trailer3.mp4,/path/to/preroll.mp4

If you have automated the script to reshuffle the symlinks, the next time you start a movie, you should be greeted with 3 new trailers from your trailer library.

This has the added benefit (drawback?) of forcing the trailers to . 

You can of course continue to use the built-in Cinema Trailers for movies in your library.

For example, if you want to watch 1 trailer from your library and two 

##### Trailer Libraries
Another perk of downloading trailers locally is that you can create a Plex video library and browse through them as you would any other media collection.

Simply create a new library and point it to the directory on your server where you store the trailers. Make sure to disable the "Enable Cinema Trailers" option under **Library >> Edit >> Advanced**, otherwise your server-wide pre-roll will run before every trailer.

Note that because trailers grabbed from YouTube do not have embedded metadata, the metadata agents will not be able to match every trailer, particularly for films with a release date far in the future or indie films.

This also occurs with trailers


### Upcoming Features

- webUI for managing source playlists and trailer libraries
- support for non-YouTube sources


## FAQ 

### Why would I possibly want to download trailers for upcoming movies when Plex has this function built in?

The [Plex Pass cinema trailers feature](https://support.plex.tv/articles/202934883-cinema-trailers-extras/) is awesome in principle, but has some pretty serious flaws, imho. While Plex excells at streaming local media, it's still rather buggy at streaming from the internet. Moreover, Users get no control over the content and quality of trailers, and streaming over the internet is not always reliable or desired. 

This script should be useful for anyone who [wants more control over the genre and quality of trailers shown](https://www.reddit.com/r/PleX/comments/87ez9q/better_cinema_trailers/), [doesn't have a Plex Pass subscription](https://www.reddit.com/r/PleX/comments/7ho134/trailers_without_plexpass/), has Plex clients on a local network without external internet access, or wants to create a browsable and constantly-up-to-date Plex library of movie trailers.

### Can I use this without a Plex Pass subscription?

Yep, as long as the pre-roll remains a free feature, you can watch trailers without paying a dime to the Plex developers. 

### I only want to view trailers from my favorite independent Bollywood anime studio, can I still use this?

As long as they make a YouTube playlist.

### I downloaded a trailer and Plex won't find the 