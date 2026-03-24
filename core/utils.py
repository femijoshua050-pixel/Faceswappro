# Utility functions for image and file operations

import os
from PIL import Image


def resize_image(input_path, output_path, size):
    """Resize an image to a given size."""
    with Image.open(input_path) as img:
        img = img.resize(size)
        img.save(output_path)


def save_image(image, path):
    """Save an image to the specified path."""
    image.save(path)


def load_image(path):
    """Load an image from the specified path."""
    return Image.open(path)


def delete_file(path):
    """Delete a file at the specified path if it exists."""
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
