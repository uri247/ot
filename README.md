# OT (version 0.51)
Original Track - makes an album from a YouTube playlist

OT (Original Track) is a small utility that creates an album suitable to
be uploaded to iPhone or Android from a YouTube playlist. Special
attention is paid to put the appropriate metadata, including Thumbnails,
album name, song title and artists to the files.

OT is written in Python. It should work in your Unix/Linux box, Windows
or Mac OS X.

## Dependencies

OT is a tiny bird that stands on the shoulder of giants:

- **youtube-dl**: the command line utility by rg3, which does the actual
download
- **libav**: The Linux Audio Video library
- **mutagen**: A metadata library for media files

## Installation

In order to have a runnable OT perform the following steps

##### Install Python
from http://python.org install the python suitable for your machine.
Note: Some version of Python comes pre-installed on Mac OS and on most
Linux distributions.

##### Python libraries
```shell
$ pip install youtube-dl
$ pip install mutagen
```

##### libav
libav is an open source (GPL) Audio Video library. It is used to
transcode the YouTube songs to m4a or mp3 format.

###### Linux
    $ sudo apt-get install libav
    
###### Windows

Go to http://builds.libav.org/windows/, and select the release-gpl (more
features, license is more restricted, if you were a developer). Select
the most recent build (currently, 11.3), for win32 or win64 that
appropriate for your machine. Extract the 7z file, and make sure the bin
folder is in the search path

## Running

Invoking OT has 3 steps:

1. Download all the songs and creating an Excel spreadsheet with `ot.py`
script
2. Manually review *album.xls* with Excel, fix song artist or title if
necessary, and set order
3. Fix the songs metadata, and set order with `otfix.py`

#### step 1: ot.py
Edit `config.py` and set the URL of the playlist
Then, simply run `ot.py`

#### step 2: Album.xls
Previous step will create a spreadsheet named Album.xls with a list of
all the songs. It will also fill what it believes to be the song's name
and artist, based on the YouTube title.
To set priority, put '**' or '***' in the priority column
To delete a song from the album, put 'del' in the priority column

#### step 3: otfix.py
Once *Album.xls* was reviewed, simply run otfix.py

## Copyright

OT is released into the public domain by the copyright holder.


## Authors:

- Uri London (uri at london.org.il)

