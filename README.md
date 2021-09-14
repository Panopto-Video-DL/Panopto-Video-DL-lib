# PanoptoDownloader

Simple library to download video from Panopto

## Prerequisites  

- Python >= 3.8

## Install

- Download [lasted release](https://github.com/Panopto-Video-DL/Panopto-Video-DL-lib/releases)
- In the folder run the command: 
```bach
> pip install .
```

## Usage

```python
from PanoptoDownloader import PanoptoDownloader
from PanoptoDownloader.exceptions import RegexNotMatch


URL = "https://****/master.m3u8"
PATH = "./output.mp4"


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
  if isinstance(args.exc_type, RegexNotMatch):
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
```
