"""ot - Original Track

A utility that brings music tracks from Youtube playlist, straight to your iPhone player
"""

from pprint import PrettyPrinter
import youtube_dl
from config import Config


class Program(object):

    def __init__(self):
        self.pp = PrettyPrinter(indent=4, width=130, depth=3)

    def main(self):
        self.download(Config.playlist_url)

    def ydl_hook(self, d):
        status = d['status']
        if status in ('downloading', 'error', 'finished'):
            print d['status']
        elif status == 'extract_info':
            ie_result = d['ie_result']
            self.ie_hook(ie_result)

    def ie_hook(self, ie_result):
        result_type = ie_result.get('_type', u'video')
        print result_type
        if result_type == 'playlist':
            entries = list(ie_result['entries'])
            ie_result['entries'] = entries
            for entry in entries:
                print entry
        elif result_type == 'video':
            self.pp.pprint(ie_result)

    def download(self, playlist_url):

        postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '0'
        }]

        ydl_opts = {
            'verbose': True,
            'progress_hooks': [self.ydl_hook],
            'write_all_thumbnails': True,
            'outtmpl': u'%(autonumber)s;%(id)s;%(title)s.%(ext)s',
            'postprocessor_args': ['-strict', '-2'],
            'autonumber_size': 4,
            'postprocessors': postprocessors,
            'format': u'bestaudio/best',
            'keepvideo': False,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            res = ydl.extract_info(playlist_url, download=False, process=True)
            pass

            # ydl.download([playlist_url, ])


if __name__ == '__main__':
    Program().main()
