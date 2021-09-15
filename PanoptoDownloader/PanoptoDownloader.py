import re
from ffmpeg_progress_yield import FfmpegProgress

from .exceptions import *


REGEX = re.compile('^https://([^\\s]+)/master.m3u8', re.I)


def download(uri: str, output: str, callback: callable) -> None:
    """
    Download video from master.m3u8
    :param uri: master.m3u8 URI
    :param output: downloaded file path
    :param callback: function to be called during downloading
    """
    if not REGEX.match(uri):
        raise RegexNotMatch('URI not match')
    command = ['ffmpeg', '-f', 'hls', '-i', uri, '-c', 'copy', output]

    ff = FfmpegProgress(command)
    for progress in ff.run_command_with_progress():
        callback(progress)
