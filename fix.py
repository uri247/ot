import glob
import os
import random
from xlrd import open_workbook
from mutagen import mp4
from meta import Config


class SongDetails(object):

    def __init__(self, filename=None, artist=None, name=None,  youtube_id=None, priority=None):
        self.filename = filename
        self.artist = artist
        self.name = name
        self.youtube_id = youtube_id
        self.priority = priority


class Program(object):

    def __init__(self, folder, album, genre, tracks_per_disk):
        self.folder = folder
        self.xl_filename = os.path.join(folder, 'album.xlsx')
        self.album = album
        self.genre = genre
        self.tracks_per_disk = tracks_per_disk
        self.wb = None
        self.sh = None
        self.songs = {}
        self.files = None
        self.num_songs = None
        self.num_disks = None
        self.ordered = None
        pass

    def read_xl_file(self):
        self.wb = open_workbook(self.xl_filename)
        self.sh = self.wb.sheet_by_name(self.album)
        fields = ('number', 'youtube id', 'title', 'artist', 'song name')
        for idx, f in enumerate(fields):
            v = self.sh.cell(0, idx).value
            assert v == f
        for row_index in range(1, self.sh.nrows):
            song = SongDetails()
            song.youtube_id = self.sh.cell(row_index, 1).value
            song.artist = self.sh.cell(row_index, 3).value
            song.name = self.sh.cell(row_index, 4).value
            song.priority = self.sh.cell(row_index, 5).value
            self.songs[song.youtube_id] = song

    def read_files(self):
        self.files = glob.glob(os.path.join(self.folder, u'*.m4a'))
        for filename in self.files:
            f = mp4.MP4(filename)
            comment = f.tags['\xa9cmt']
            if comment and isinstance(comment, list) and len(comment) > 0:
                youtube_id = comment[0]
                song = self.songs.get(youtube_id)
                if song:
                    song.filename = filename
                else:
                    print 'unknown m4a file', filename
            else:
                print 'song does not have compatible comment', filename

    def fix(self):
        pri1 = []
        pri2 = []
        pri3 = []
        for song in self.songs.itervalues():
            if song.priority == 'del':
                try:
                    os.unlink(song.filename)
                except WindowsError:
                    pass
            elif song.priority == '***':
                pri1.append(song)
            elif song.priority == '**':
                pri2.append(song)
            else:
                pri3.append(song)

        random.shuffle(pri1)
        random.shuffle(pri2)
        random.shuffle(pri3)
        self.ordered = pri1 + pri2 + pri3
        self.num_songs = len(self.ordered)
        self.num_disks = (self.num_songs + self.tracks_per_disk - 1) / self.tracks_per_disk

        for idx, song in enumerate(self.ordered):
            disk_number = idx / self.tracks_per_disk + 1
            track_number = idx % self.tracks_per_disk + 1

            f = mp4.MP4(song.filename)
            f.tags['trkn'] = [(track_number, self.tracks_per_disk)]
            f.tags['disk'] = [(disk_number, self.num_disks)]
            f.tags['cpil'] = True
            f.tags['\xa9alb'] = [self.album, ]
            f.tags['\xa9nam'] = [song.name, ]
            f.tags['\xa9ART'] = [song.artist, ]
            # f.tags['\xa9gen'] = [self.genre, ]
            # f.tags['\xa9cmt'] = [song.youtube_id, ]
            f.save()

            new_filename = os.path.join(self.folder, u'{0} - {1}.m4a'.format(song.artist, song.name))
            new_filename = new_filename.replace('"', '\'')
            if song.filename != new_filename:
                try:
                    os.rename(song.filename, new_filename)
                except WindowsError:
                    print 'error renaming', idx

    def main(self):
        self.read_xl_file()
        self.read_files()
        self.fix()
        pass

if __name__ == '__main__':
    program = Program(Config.folder, Config.album, Config.genre, Config.tracks_per_disk)
    program.main()
