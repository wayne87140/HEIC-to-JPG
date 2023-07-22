from PIL import Image
from pathlib import Path
import logging
from pillow_heif import register_heif_opener

register_heif_opener()

FORMAT = '%(asctime)s: %(message)s'
# CPU(%(process)d) Thread(%(thread)d)
logging.basicConfig(format=FORMAT, level=logging.INFO)

# TODO asyncio, pyinstaller, select multiple files in one time


def main():
    path = input('Type or drag your abs path or only one file here: ')

    path = Path(path).resolve()

    logging.info('Input path is %s' % path)
    if path.exists():
        logging.info('Input path exists.')
    else:
        raise FileNotFoundError('The current path/file is not found.')

    if path.is_dir():
        path.parent.joinpath(f'{path.name}_jpg').mkdir(exist_ok=True)
        jpg_folder = path.parent / f'{path.name}_jpg'
        logging.info('Create a folder %s__jpg at %s', path.name, path.parent)

        for HEIC_photo in path.glob('*.HEIC'):
            transform_HEICtoJPEG(HEIC_photo, jpg_folder)

    if path.is_file():
        if path.name.split('.')[1] == "HEIC":
            transform_HEICtoJPEG(path)

    logging.info('Input path is not a directory or not a HEIC image.')


def transform_HEICtoJPEG(image_path: Path, directory=None):
    image_name = image_path.name
    image = Image.open(image_path)
    logging.info('%s is proccessing...', image_name)
    if directory:
        # save file in a new directory
        image_save_path = directory / image_name.replace('HEIC', 'JPG')
    else:
        # save file in the same directory
        image_save_path = image_path.parent / image_name.replace('HEIC', 'JPG')
    image.save(image_save_path, quality=95, optimize=True)
    logging.info('Image %s has been transformed to JPG successfully.',
                 image_name.split('.')[0])


if __name__ == "__main__":
    main()
