import PanoptoDownloader
from PanoptoDownloader.exceptions import *


URL = input('master.m3u8 URL: ')
PATH = input('Output file: ') or './output.mp4'


def callback(progress: int):
    """
    :param progress: Downloading progress. From 0 to 100
    """
    print(f"{progress} / 100")


if __name__ == '__main__':
    try:
        PanoptoDownloader.download(
            URL,
            PATH,
            callback
        )
        print("Download completed")

    except RegexNotMatch as e:
        print(e)
