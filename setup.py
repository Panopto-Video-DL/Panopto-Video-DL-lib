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
    python_requires='>=3.7',
    install_requires=[
        'ffmpeg-progress-yield~=0.2.0',
        'requests~=2.27.1',
        'pycryptodomex~=3.12.0',
        'yarl~=1.7.2',
        'tqdm~=4.62.2'
    ],
    entry_points="""
        [console_scripts]
        panoptodownloader=PanoptoDownloader.__main__:main
    """,
)
