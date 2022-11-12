# PanoptoDownloader

Download video from Panopto!  

## Prerequisites  

- [Panopto-Video-DL-browser](https://github.com/Panopto-Video-DL/Panopto-Video-DL-browser)
- [FFmpeg](https://ffmpeg.org/download.html) (Optional. See [below](#ffmpeg))  
    **Note**: FFmpeg **must** be added in the _system PATH_  
- Python >= 3.7

## Install

Run the command:
```shell
pip install git+https://github.com/Panopto-Video-DL/Panopto-Video-DL-lib#egg=PanoptoDownloader
```

### FFmpeg

Since version 1.4.0 FFmpeg is _no longer needed_, but it is highly recommended.  
It is possible that some videos will not download properly without FFmpeg.

## Usage

Run the command:

```shell
panoptodownloader URL [-o OUTPUT]
```

### Use as Python Module

```python
import PanoptoDownloader


URL = "https://****"
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

    except Exception as e:
        print(e)
```
