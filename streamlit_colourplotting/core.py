import os
from io import BytesIO
from typing import Optional

import colour.io
import imageio.v3 as imageio
import numpy

import cv2


def read_image_from_bytes(bytesio: BytesIO) -> numpy.ndarray:
    """
    Return an RGB image with a floating point encoding from the given bytes buffer.
    """
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

    image = colour.io.convert_bit_depth(image, "float32")
    return image
