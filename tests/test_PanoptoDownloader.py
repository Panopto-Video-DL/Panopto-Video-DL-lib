from PanoptoDownloader import PanoptoDownloader
from PanoptoDownloader.exceptions import RegexNotMach


URL = input('master.m3u8 URL: ')
PATH = input('Output file: ) or './output.mp4'


def callback(progress):
    """
    :param progress: Downloading progress. From 0 to 100
    """
    print(f"{progress}/100")
    if progress == 100:
        print("Download completed")


def error(args, /):
    """
    :param args: threading.excepthook -> https://docs.python.org/3/library/threading.html#threading.excepthook
    """
    if isinstance(args.exc_type, RegexNotMach):
        print('URL not correct')
    else:
        raise args.exc_type


if __name__ == '__main__':
    downloader = PanoptoDownloader()
    
    thread = downloader.download(
        URL,
        PATH,
        callback,
        error
    )
    thread.join()
