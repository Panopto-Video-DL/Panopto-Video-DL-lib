# PanoptoDownloader

Download video from Panopto!  

## Prerequisites  

- [Panopto-Video-DL-browser](https://github.com/Panopto-Video-DL/Panopto-Video-DL-browser)
- Python >= 3.7

## Install

Run the command:
```shell
pip install git+https://github.com/Panopto-Video-DL/Panopto-Video-DL-lib#egg=PanoptoDownloader
```

### FFmpeg extension

Since version 1.4.0 _FFmpeg is no longer needed_, but it is still possible to download video
using [ffmpeg](https://ffmpeg.org/download.html) by adding `[ffmpeg]` to the pip command used to install it.  
```shell
pip install git+https://github.com/Panopto-Video-DL/Panopto-Video-DL-lib#egg=PanoptoDownloader[ffmpeg]
```

**Note**: FFmpeg **must** be added in the _system PATH_  

## Usage

- In a new terminal run the command:
```shell
panoptodownloader
```
- Paste the link automatically copied from [Panopto-Video-DL-browser](https://github.com/Panopto-Video-DL/Panopto-Video-DL-browser)
- Set the destination folder
- Wait for the download to finish

## Use as Python Module

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
