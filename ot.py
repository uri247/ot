"""ot - Original Track

A utility that brings music tracks from Youtube playlist, straight to your iPhone player
"""

import youtube_dl


class Program(object):

    def main(self):
        self.download('https://www.youtube.com/playlist?list=PLJDaThmgB7hhK3ASynwajyuQAj6XUUGXZ')

    @staticmethod
    def ydl_hook(d):
        print d['status']

    def download(self, playlist):

        postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': 0
        }]

        ydl_opts = {
            'verbose': True,
            'progress_hooks': [self.ydl_hook],
            'write_all_thumbnails': True,
            'outtmpl': u'%(autonumber)s;%(id)s;%(title)s.%(ext)s',
            'postprocessor_args': ['-strict', '-2'],
            'autonumber_size': 4,
            'postprocessors': postprocessors,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist])


if __name__ == '__main__':
    Program().main()
