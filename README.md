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
import PanoptoDownloader
from PanoptoDownloader.exceptions import RegexNotMatch


URL = "https://****/master.m3u8"
PATH = "./output.mp4"


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
```
