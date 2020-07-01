from os import path
import shutil

from werkzeug.datastructures import ImmutableMultiDict


def save_images(images: ImmutableMultiDict, dest_path: path):
    if images is None \
            or dest_path is None \
            or len(images) == 0:
        return
    for image in images:
        print(f"Moving image {image} to {dest_path}")
        shutil.move(image, dest_path)
