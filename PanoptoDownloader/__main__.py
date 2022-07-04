import os
import argparse
import PanoptoDownloader
from tqdm import tqdm
from PanoptoDownloader import __version__, SUPPORTED_FORMATS


parser = argparse.ArgumentParser()
parser.add_argument('URL', type=str, help='URL copied from Panopto-Video-DL-browser')
parser.add_argument('-o', '--output', type=str, default='./output' + SUPPORTED_FORMATS[0], help='Output file path')
parser.add_argument('-v', '--version', action='version', version=f'v{__version__}')


def input_yesno(*args) -> bool:
    r = None
    while r not in ['Y', 'N']:
        r = input(*args).upper()
        if r == 'Y':
            return True
        elif r == 'N':
            return False
        else:
            print('Invalid input. Use Y or N', end='\n\n')


def __main__(args):
    print('PanoptoDownloader', end='\n\n')

    url = args.URL
    filepath = args.output

    if os.path.isdir(filepath):
        print('ERROR. Cannot be a folder')
        exit(1)
    if not os.path.isdir(os.path.split(filepath)[0] or './'):
        print('ERROR. Folder does not exist')
        exit(1)

    extension = os.path.splitext(filepath)[1]
    if not extension or extension == '.':
        filepath += SUPPORTED_FORMATS[0] if filepath[-1] != '.' else SUPPORTED_FORMATS[0][1:]

    if os.path.exists(filepath):
        print('File already exist')
        result = input_yesno('Replace it [Y, n]? ')
        if result:
            os.remove(filepath)
        else:
            exit(1)
    if os.path.splitext(filepath)[1] not in SUPPORTED_FORMATS:
        print('Extension not officially supported. Choose from: ' + str(SUPPORTED_FORMATS))
        result = input_yesno('Continue anyway [Y, n]? ')
        if not result:
            exit(1)

    print(f'\nDownload started: {filepath}\n')

    bar = tqdm(total=100)

    def callback(progress: int) -> None:
        bar.n = progress
        bar.refresh()

    try:
        PanoptoDownloader.download(url, filepath, callback)
    except Exception as e:
        bar.close()
        print('ERROR.', str(e))
    except KeyboardInterrupt as e:
        bar.close()
        raise e
    else:
        bar.close()
        print('\nDownload completed')


def main():
    try:
        args = parser.parse_args()
        __main__(args)
    except KeyboardInterrupt:
        print('\nProgram closed')


if __name__ == '__main__':
    main()
