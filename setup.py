#!/usr/bin/env python3
from setuptools import setup, find_packages
from PanoptoDownloader import __version__


with open('./README.md', 'r') as fp:
    long_description = fp.read()
with open('requirements.txt', 'r') as fp:
    install_requires = fp.read().strip().split('\n')


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
    install_requires=install_requires,
    extras_require={
        'ffmpeg': ['ffmpeg_progress_yield']
    },
    entry_points="""
        [console_scripts]
        panoptodownloader=PanoptoDownloader.__main__:main
    """,
)
