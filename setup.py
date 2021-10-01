#!/usr/bin/env python3
from setuptools import setup, find_packages
from PanoptoDownloader import __version__


with open('./README.md', 'r') as fp:
    long_description = fp.read()


setup(
    name='PanoptoDownloader',
    version=__version__,
    description='Download video from Panopto',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Panopto-Video-DL',
    url='https://github.com/Panopto-Video-DL/Panopto-Video-DL-lib',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'ffmpeg_progress_yield',
        'urllib3',
        'certifi'
    ]
)
