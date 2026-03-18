import logging

import numpy

LOGGER = logging.getLogger(__name__)


def convert_int8_to_float(source: numpy.ndarray):
    """
    Convert a 8bit RGB color to floating point encoding.

    Result is clamped in the [0-1] range.

    Args:
        source: arbitrary length array of integers

    Returns:
        new array of the same length as float encoding
    """
    intermediate = numpy.clip(source, 0, 255)
    return intermediate.astype(numpy.float32) / 255


def convert_float_to_int8(source: numpy.ndarray):
    """
    Convert a floating point array of color values to 8bit integer encoding.

    Result is clamped in the [0-255] range.

    Args:
        source: arbitrary length array of floats

    Returns:
       new  array of the same length as 8bit encoding
    """
    array = numpy.around(numpy.multiply(source, 255))
    return numpy.clip(array, 0, 255).astype(numpy.uint8)
