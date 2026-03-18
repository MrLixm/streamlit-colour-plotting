from __future__ import annotations

import dataclasses
import logging
from typing import Literal
from typing import overload
from typing import Optional
from typing import Union

import numpy

from . import RgbColorspace
from . import sRGB_COLORSPACE
from . import colorspace_to_colorspace
from . import ChromaticAdaptationTransform
from . import convert_int8_to_float
from . import convert_float_to_int8

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class RGBAColor:
    """
    Dataclass to represent a color expressed under the R-G-B color model.

    Internal values are stored as floats expressed in the given colorspace.

    You can convert from and to different encoding using the ``from_XXX`` and ``to_XXX`` methods.

    Args:
        red: [-0-1+] range
        green: [-0-1+] range
        blue: [-0-1+] range
        colorspace: colorspace in which the R,G,B triplet is encoded in.
        alpha: optional alpha values associated with the RGB triplet. [0-1] range.
    """

    red: float
    green: float
    blue: float
    colorspace: Optional[RgbColorspace] = None
    alpha: Optional[float] = None

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}<({self.r}, {self.g}, {self.b}, {self.a})"
            f":{self.colorspace} at {hex(id(self))}>"
        )

    @property
    def r(self) -> float:
        return self.red

    @property
    def g(self) -> float:
        return self.green

    @property
    def b(self) -> float:
        return self.blue

    @property
    def a(self) -> Optional[float]:
        return self.alpha

    @classmethod
    def from_int8(
        cls,
        red: int,
        green: int,
        blue: int,
        colorspace: Optional[RgbColorspace] = None,
        alpha: Optional[float] = None,
    ) -> RGBAColor:
        """
        Get a RGBColor instance from a 8bit RGB triplet. The triplet is assumed to
        always be encoded in sRGB(EOTF) colorspace.

        Args:
            red: 0-255 range
            green: 0-255 range
            blue: 0-255 range
            colorspace: colorspace the tuple is encoded in. Usually sRGB.
            alpha: optional alpha values associated with the RGB triplet. [0-1] range.

        Returns:
            RGBColor instance corresponding to the given parameters.
        """
        source_array = numpy.array((red, green, blue), dtype=numpy.uint8)
        converted_array = convert_int8_to_float(source_array)
        return cls.from_array(converted_array, colorspace=colorspace, alpha=alpha)

    @classmethod
    def from_hex(
        cls,
        hexadecimal: str,
        assume_srgb: bool = True,
        alpha: Optional[float] = None,
    ) -> RGBAColor:
        """
        Get a RGBColor instance from a hexadecimal color encoding.

        References:
            -[1] https://stackoverflow.com/a/29643643/13806195

        Args:
            hexadecimal: with or without the "#"
            assume_srgb:
                if True the color is assumed to be encoded as sRGB (EOTF).
                Usually always True for all hexadecimal colors.
            alpha: optional alpha values associated with the RGB triplet. [0-1] range.

        Returns:
            RGBColor instance corresponding to the given parameters.
        """
        hexadecimal = hexadecimal.lstrip("#")
        r, g, b = tuple(int(hexadecimal[i : i + 2], 16) for i in (0, 2, 4))
        colorspace = sRGB_COLORSPACE if assume_srgb else None
        return cls.from_int8(r, g, b, colorspace=colorspace, alpha=alpha)

    @classmethod
    def from_array(
        cls,
        array: numpy.ndarray,
        colorspace: RgbColorspace,
        alpha: Optional[float] = None,
    ) -> RGBAColor:
        """

        Args:
            array:
                R,G,B triplet with an optional 4th alpha component.
                [r,g,b] or [r,g,b,a].
                RGB channels are expressed in floats.
            colorspace: colorspace in which the R,G,B triplet is encoded in.
            alpha: optional alpha values associated with the RGB triplet. [0-1] range.

        Returns:
            RGBColor instance corresponding to the given parameters.
        """

        if array.shape[0] == 4 and alpha is None:
            alpha = array[3]

        return cls(array[0], array[1], array[2], colorspace=colorspace, alpha=alpha)

    def copy(self) -> RGBAColor:
        """
        Returns:
            return a new instance copy of this one
        """
        return dataclasses.replace(self)

    def to_array(self, alpha: Union[bool, float] = True) -> numpy.ndarray:
        """
        Args:
            alpha:
                - If True, return the internal alpha value if not none at the end of the array. (size 4 or 3)
                - If False, always return a ndarray of size 3
                - If a float, return an array with the value passed (size 4)

        Returns:
            array(3,) == [r,g,b] or array(4,) == [r,g,b,a]
        """
        return numpy.array(self.to_float(alpha=alpha), dtype=numpy.core.float32)

    @overload
    def to_float(self, alpha: float = ...) -> tuple[float, float, float, float]: ...

    @overload
    def to_float(self, alpha: Literal[False] = ...) -> tuple[float, float, float]: ...

    @overload
    def to_float(
        self,
        alpha: Literal[True] = ...,
    ) -> Union[tuple[float, float, float], tuple[float, float, float, float]]: ...

    def to_float(
        self,
        alpha: Union[bool, float] = True,
    ) -> Union[tuple[float, float, float], tuple[float, float, float, float]]:
        """
        Args:
            alpha:
                - If True, return the internal alpha value if not none at the end of the tuple. (len 4 or 3)
                - If False, always return a tuple of len 3
                - If a float, return a tuple with the value passed (len 4)

        Returns:
            (r,g,b) or (r,g,b,a) where component is a float
        """
        if alpha is False:
            return self.red, self.green, self.blue

        if alpha is True and self.alpha is not None:
            return self.red, self.green, self.blue, self.alpha

        return self.red, self.green, self.blue, alpha

    def to_hex(self, force_srgb: bool = True) -> str:
        """
        Get a hexadecimal representation of the current color.

        References:
            - [1] https://stackoverflow.com/a/3380754/13806195

        Args:
            force_srgb:
                if True perform a colorspace conversion to sRGB (with EOTF).
                hexadecimal colors are usually always sRGB encoded.

        Returns:
            hexadecimal color with the "#". Letters in lowercase.
        """
        intermediate = self
        if force_srgb:
            intermediate = self.as_colorspace(sRGB_COLORSPACE)

        r, g, b = intermediate.to_int8(alpha=False)
        return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)

    def to_int8(
        self,
        alpha: Union[bool, float] = True,
    ) -> Union[tuple[int, int, int], tuple[int, int, int, float]]:
        """
        Return an RGB(A) triplet encoded with 8bit values. [0-255]

        Usually it is desired to perform a sRGB colorspace conversion before calling
        this::

            color = RGBData(...)
            color_converted = color.as_colorspace(get_colorspace("sRGB"))
            color_converted = color_converted.to_int8()

        Args:
            alpha:
                - If True, return the internal alpha value if not none at the end of the tuple. (len 4 or 3)
                - If False, always return a tuple of len 3
                - If a float, return a tuple with the value passed (len 4)

        Returns:
            (r,g,b) or (r,g,b,a)
        """
        as_bits = convert_float_to_int8(self.to_array(alpha=False))
        red = as_bits[0].item()
        green = as_bits[1].item()
        blue = as_bits[2].item()

        if alpha is False:
            return red, green, blue

        if alpha is True and self.alpha is not None:
            return red, green, blue, self.alpha

        return red, green, blue, alpha

    def as_colorspace(
        self,
        target_colorspace: Optional[RgbColorspace],
        cat: Union[ChromaticAdaptationTransform, bool] = True,
    ) -> RGBAColor:
        """
        Get a copy of this instance converted in the given colorspace.

        Args:
            target_colorspace:
                new colorspace to encode the color in. If None no transformation is performed.
            cat: chromatic adaptation transform to use. True to use default.

        Returns:
            new RGBColor instance encoded in the given colorspace
        """
        if self.colorspace is None or target_colorspace is None:
            return dataclasses.replace(self, colorspace=target_colorspace)

        if self.colorspace == target_colorspace:
            return self.copy()

        if cat is True:
            cat = ChromaticAdaptationTransform.get_default()
        elif cat is False:
            cat = None

        new_array = colorspace_to_colorspace(
            array=self.to_array(alpha=False),
            source_colorspace=self.colorspace,
            target_colorspace=target_colorspace,
            chromatic_adaptation_transform=cat,
        )

        return self.__class__.from_array(new_array, target_colorspace, self.alpha)
