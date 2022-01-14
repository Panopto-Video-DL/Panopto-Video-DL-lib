import os
import PanoptoDownloader
from tqdm import tqdm


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


def __main__():
    print('PanoptoDownloader', end='\n\n')

    url = None
    while not url:
        url = input('URL: ')

    while True:
        filepath = None
        while not filepath:
            filepath = input('\nOUTPUT file: ')

        if os.path.isdir(filepath):
            print('ERROR. Cannot be a folder')
            continue
        if not os.path.isdir(os.path.split(filepath)[0] or './'):
            print('ERROR. Folder does not exist')
            continue

        extension = os.path.splitext(filepath)[1]
        if not extension or extension == '.':
            filepath += PanoptoDownloader.SUPPORTED_FORMATS[0] if filepath[-1] != '.' else \
                PanoptoDownloader.SUPPORTED_FORMATS[0][1:]

        if os.path.exists(filepath):
            print('File already exist')
            result = input_yesno('Replace it [Y, n]? ')
            if result:
                os.remove(filepath)
            else:
                continue
        if os.path.splitext(filepath)[1] not in PanoptoDownloader.SUPPORTED_FORMATS:
            print('Extension not officially supported. Choose from: ' + str(PanoptoDownloader.SUPPORTED_FORMATS))
            result = input_yesno('Continue anyway [Y, n]? ')
            if not result:
                continue
        break

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
        __main__()
    except KeyboardInterrupt:
        print('\nProgram closed')


if __name__ == '__main__':
    main()
