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
$ pip install youtube-dl
$ pip install mutagen

##### libav
Go to http://libav.org/downloads, and install the package suitable for
your machine

## Running

Once OT is installed, from the command line run `ot.py` to execute
Original Track. A new album will be created, at the current directory

## Copyright

OT is released into the public domain by the copyright holder.


## Authors:

- Uri London (uri at london.org.il)

