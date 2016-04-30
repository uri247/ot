"""

o52. Takes a folder of clips downloads from YouTube, and fix its meta data

Getting the folder:
    youtube-dl --extract-audio --audio-format m4a --audio-quality 0 \
        --postprocessor-args "-strict -2" --write-all-thumbnails --autonumber-size 4 \
         --output "%(autonumber)s;%(id)s;%(title)s.%(ext)s" \
         https://www.youtube.com/playlist?list=PLJDaThmgB7hg7ZoLav_o9kInfPwW7cw5d

"""

import glob
import os
import re
import random
import string
from mutagen import mp4
import xlsxwriter


class Config(object):
    folder = ur'C:\Dropbox\Shabat.Ivrit\Shabat.Ivrit'
    # album = u'Shabat Ivrit'
    album = u'\u05e9\u05d1\u05ea \u05e2\u05d1\u05e8\u05d9\u05ea'
    genre = 'Israeli'
    tracks_per_disk = 50
    num_disks = None


class XL(object):

    def __init__(self, filename, album):
        self.filename = filename
        self.album = album

        if os.path.isfile(self.filename):
            os.remove(self.filename)

        self.wb = xlsxwriter.Workbook(self.filename)
        self.ws = self.wb.add_worksheet(self.album)
        self.ws.right_to_left()

        # set column headers and width
        bold = self.wb.add_format({'bold': True})
        columns = [(8, 'number'), (12, 'youtube id'), (60, 'title'), (50, 'artist'), (50, 'song name')]
        for idx, col in enumerate(columns):
            self.ws.write(0, idx, col[1], bold)
            self.ws.set_column(idx, idx, col[0])

    def __del__(self):
        self.wb.close()

    def write(self, row, column, content):
        self.ws.write(self.cell_name(row, column), content)

    @staticmethod
    def col_name(col):
        """Calculate the Excel column name. n is a zero based index. e.g. 0 => A, 1 => B, ... 25 => Z, 26 => AA"""
        col += 1
        col_name = ''
        while col > 0:
            modulo = (col-1) % 26 + 1
            col_name = string.ascii_uppercase[modulo-1] + col_name
            col = (col - modulo) / 26
        return col_name

    @staticmethod
    def row_name(row):
        return str(row+1)

    def cell_name(self, row, col):
        name = self.col_name(col) + self.row_name(row)
        return name

    def add_song(self, number, youtube_id, title, song_name, artist):
        self.write(number + 1, 0, number + 1)
        self.write(number + 1, 1, youtube_id)
        self.write(number + 1, 2, title)
        self.write(number + 1, 3, artist)
        self.write(number + 1, 4, song_name)


class MetaProcessor(object):

    def __init__(self, folder, album, genre, tracks_per_disk):
        self.folder = folder
        self.album = album
        self.genre = genre
        self.tracks_per_disk = tracks_per_disk
        self.num_disks = None
        self.numbers = None
        self.xl = None

    def do_one(self, number, fn):
        bn = os.path.basename(fn)
        dn = os.path.dirname(fn)
        result = re.match('(\d*);(.*?);(.*).(m4a)', bn)
        if not result:
            print u'bad file name format: {0}'.format(bn)
            return

        _, youtube_id, title, ext = result.groups()

        disk_number = number / self.tracks_per_disk + 1
        track_number = number % self.tracks_per_disk + 1

        # try to split title to artist - song name
        result = re.match('(.*) - (.*)', title)
        if result:
            artist, song_name = result.groups()
        else:
            artist, song_name = '', title

        f = mp4.MP4(fn)
        f.tags['trkn'] = [(track_number, self.tracks_per_disk)]
        f.tags['disk'] = [(disk_number, self.num_disks)]
        f.tags['cpil'] = True
        f.tags['\xa9alb'] = [self.album, ]
        f.tags['\xa9nam'] = [song_name, ]
        f.tags['\xa9ART'] = [artist, ]
        f.tags['\xa9gen'] = [self.genre, ]
        f.tags['\xa9cmt'] = [youtube_id, ]

        jpg_file = os.path.splitext(fn)[0] + '.jpg'
        with open(jpg_file, 'rb') as h:
            cover_data = h.read()
        cover = mp4.MP4Cover(cover_data, mp4.AtomDataType.JPEG)
        f.tags['covr'] = [cover, ]

        f.save()

        os.unlink(jpg_file)
        new_fn = os.path.join(dn, title + '.' + ext)
        try:
            os.rename(fn, new_fn)
        except WindowsError as e:
            print u'cannot rename {0}'.format(number)
            print u'error {0}: {1}'.format(e.args[0], e.args[1])

        self.xl.add_song(number, youtube_id, title, song_name, artist)

    def process(self):
        print 'Finding *.m4a files in {0}'.format(self.folder)

        files = glob.glob(u'{0}{1}*.m4a'.format(self.folder, os.path.sep))
        num_files = len(files)
        self.num_disks = (num_files + self.tracks_per_disk - 1) / self.tracks_per_disk
        self.numbers = range(len(files))
        random.shuffle(self.numbers)

        xl_filename = os.path.join(self.folder, 'album.xlsx')
        self.xl = XL(xl_filename, self.album)

        for track_number, fn in zip(self.numbers, files):
            self.do_one(track_number, fn)


def main():
    MetaProcessor(Config.folder, Config.album, Config.genre, Config.tracks_per_disk).process()


if __name__ == '__main__':
    main()
