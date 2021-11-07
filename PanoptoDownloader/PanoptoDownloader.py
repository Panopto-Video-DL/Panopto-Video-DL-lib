import os.path
import re
import certifi
import urllib3
import urllib.request
from shutil import which
from ffmpeg_progress_yield import FfmpegProgress

from .exceptions import *


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
    if os.path.splitext(output)[1] not in SUPPORTED_FORMATS:
        raise NotSupported('Extension not supported. Must be one of ' + str(SUPPORTED_FORMATS))

    if uri.endswith('master.m3u8'):
        command = ['ffmpeg', '-f', 'hls', '-i', uri, '-c', 'copy', output]

        if which(command[0]) is None:
            raise RuntimeError(f'{command[0]} is not in the System Path')

        ff = FfmpegProgress(command)
        for progress in ff.run_command_with_progress():
            callback(progress)
    else:
        def _format(block_num, block_size, total_size):
            callback(int(block_num * block_size / total_size * 100))

        http = urllib3.PoolManager(ca_certs=certifi.where())
        response = http.request('HEAD', uri)
        if 'Content-Type' in response.headers and 'video/' in response.headers['Content-Type']:
            urllib.request.urlretrieve(uri, output, _format)
        else:
            raise NotAVideo('Doesn\'t seem to be a video')
