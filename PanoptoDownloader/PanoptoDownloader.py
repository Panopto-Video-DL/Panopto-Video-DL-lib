import re
import threading
from ffmpeg_progress_yield import FfmpegProgress

from PanoptoDownloader.exceptions import *


class PanoptoDownloader:

    REGEX = re.compile('^https://([^\\s]+)/master.m3u8', re.I)

    def download(self, uri: str, output: str, callback: callable, error: callable) -> threading.Thread:
        """
        Download video from master.m3u8
        :param uri: master.m3u8 URI
        :param output: downloaded file path
        :param callback: function to be called during downloading
        :param error: function to be called after error
        :return: Thread
        """
        if not self.REGEX.match(uri):
            raise RegexNotMatch('URI not match')
        command = ['ffmpeg', '-f', 'hls', '-i', uri, '-c', 'copy', output]

        threading.excepthook = error
        t = threading.Thread(target=self._start, args=(command, callback))
        t.start()
        return t

    @staticmethod
    def _start(command: list, callback: callable) -> None:
        ff = FfmpegProgress(command)
        for progress in ff.run_command_with_progress():
            callback(progress)
