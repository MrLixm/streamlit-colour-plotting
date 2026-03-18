"""
This whole lib is copied from https://github.com/MrLixm/cocoon
"""

from ._bitdepth import convert_float_to_int8
from ._bitdepth import convert_int8_to_float

from ._colorspace import RgbColorspace
from ._colorspace import sRGB_COLORSPACE
from ._colorspace import ChromaticAdaptationTransform
from ._colorspace import get_available_colorspaces
from ._colorspace import get_colorspace
from ._colorspace import colorspace_to_colorspace
from ._colorspace import is_colorspace_decoding_linear

from ._rgbacolor import RGBAColor

from ._colorstr import ColorStringFormat
from ._colorstr import ValidatorResult
from ._colorstr import convert_str_to_color
from ._colorstr import convert_color_to_str
from ._colorstr import fix_color_str
from ._colorstr import validate_color_str
