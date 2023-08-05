import logging
import os
import sys
from io import BytesIO
from typing import Optional

import colour.io
import imageio.v3 as imageio
import numpy

import cv2

LOGGER = logging.getLogger(__name__)


def transform_box(
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    scale: float,
    offset_x: float,
    offset_y: float,
) -> tuple[float, float, float, float]:
    """
    Transform the given "box" shape defined by its x,y coordinates using given scale and offsets.

    Args:
        xmin: "left" of the box
        xmax: "right" of the box
        ymin: "top" of the box
        ymax: "bottom"
        scale: null == 1.0,  unit relative to x, y coordinates
        offset_x: null == 0.0, unit relative to x coordinates
        offset_y: null == 0.0, unit relative to y coordinates

    Returns:
        new coordinates as tuple[xmin, xmax, ymin, max]
    """
    center_x = (xmin + xmax) / 2
    center_y = (ymin + ymax) / 2

    xmin -= center_x
    xmax -= center_x
    ymin -= center_y
    ymax -= center_y

    xmin *= scale
    xmax *= scale
    ymin *= scale
    ymax *= scale

    xmin += center_x + offset_x
    xmax += center_x + offset_x
    ymin += center_y + offset_y
    ymax += center_y + offset_y

    return xmin, xmax, ymin, ymax


def rescale_image_fast(image_array: numpy.ndarray, target_width: int):
    """
    Rescale the given image array to the given width while preserving aspect ratio.

    The rescaling is low-quality but fast.

    Args:
        image_array: array of shape looking like (height, width, 3)
        target_width: size in pixels of the desired output width

    Returns:
        initial image rescaled as specified
    """
    source_width = image_array.shape[1]
    target_width = max(target_width, source_width)
    width_ratio = int(source_width / target_width)

    source_height = image_array.shape[0]
    target_height = int(source_height / (source_width / target_width))
    height_ratio = int(source_height / target_height)

    if width_ratio >= 1 and height_ratio >= 1:
        return image_array[::width_ratio, ::height_ratio, ...]
    return image_array.copy()


def read_image_from_bytes(bytesio: BytesIO) -> numpy.ndarray:
    """
    Return an RGB image with a floating point encoding from the given bytes buffer.
    """
    LOGGER.debug(f"initial BytesIO size { sys.getsizeof(bytesio) / 1024**2}MB")
    # make sure the buffer cursor is back at start
    bytesio.seek(0)

    extension = os.path.splitext(bytesio.name)[-1]

    # imageio can't read exr that are not filepaths
    if extension in [".exr", ".hdr"]:
        byte_array = numpy.asarray(bytearray(bytesio.read()))
        image = cv2.imdecode(byte_array, cv2.IMREAD_UNCHANGED)
        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB,
        )

    else:
        image = imageio.imread(bytesio)

    if len(image.shape) == 2:
        image = image[:, :, numpy.newaxis]
        image = numpy.repeat(image, 3, axis=2)

    if image.shape[2] > 3:
        image = image[:, :, :3]

    LOGGER.debug(f"initial ndarray size {sys.getsizeof(image) / 1024**2}MB")
    image = colour.io.convert_bit_depth(image, "float32")
    LOGGER.debug(f"float32 ndarray size {sys.getsizeof(image) / 1024**2}MB")
    return image
