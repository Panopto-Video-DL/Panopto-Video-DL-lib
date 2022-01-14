import os.path
import re
import requests
import urllib.request
from shutil import which

try:
    from ffmpeg_progress_yield import FfmpegProgress
    use_ffmpeg = which('ffmpeg') is not None
except ImportError:
    use_ffmpeg = False

from .exceptions import *
from .hls_downloader import hls_downloader


SUPPORTED_FORMATS = ['.mp4', '.mkv', '.flv', '.avi']
REGEX = re.compile(
    r'^(http)s?://'
    r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def download(uri: str, output: str, callback: callable) -> None:
    """
    Download video from Panopto
    :param uri: video URI
    :param output: downloaded file path
    :param callback: function to be called during downloading
    """
    if not REGEX.match(uri):
        raise RegexNotMatch('Doesn\'t seem to be a URL')
    if os.path.isdir(output):
        raise NotAFile('Cannot be a folder')
    if not os.path.isdir(os.path.split(output)[0] or './'):
        raise NotExist('Folder does not exist')
    if os.path.exists(output):
        raise AlreadyExists('File already exists')
    # if os.path.splitext(output)[1] not in SUPPORTED_FORMATS:
    #     raise NotSupported('Extension not supported. Must be one of ' + str(SUPPORTED_FORMATS))

    if uri.endswith('master.m3u8'):
        if use_ffmpeg:
            command = ['ffmpeg', '-f', 'hls', '-i', uri, '-c', 'copy', output]
            ff = FfmpegProgress(command)
            for progress in ff.run_command_with_progress():
                callback(progress)
        else:
            hls_downloader(uri, output, callback=callback)

    else:
        def _format(block_num, block_size, total_size):
            callback(int(block_num * block_size / total_size * 100))

        response = requests.head(uri)
        if 'video/' in response.headers.get('Content-Type', ''):
            urllib.request.urlretrieve(uri, output, _format)
        else:
            raise NotAVideo('Doesn\'t seem to be a video')
