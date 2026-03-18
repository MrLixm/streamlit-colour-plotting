"""
Generate and validate RGBColor instance from string inputs.

This allows to specify a color value in a single line which is very useful in the GUI context.
"""

import enum
import abc
import re
from typing import Type

from ._rgbacolor import RGBAColor

DEFAULT_COLOR = RGBAColor(0.0, 0.0, 0.0)


class ValidatorResult(enum.Enum):
    """
    Results of a validation operation.
    """

    invalid = 0
    acceptable = 1
    valid = 2


class _BaseRGBColorStringConverter(abc.ABC):
    """
    Abstract class defining logic to generate a color from/to string.
    """

    Validations = ValidatorResult

    @classmethod
    @abc.abstractmethod
    def fix(cls, user_input: str) -> str:
        """
        Sanitize the given string, so it can be a valid represention of a color instance as string.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def from_color(cls, color: RGBAColor) -> str:
        """
        Convert color instance to string.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def to_color(cls, user_input: str) -> RGBAColor:
        """
        Convert string to color instance.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def validate(cls, user_input: str) -> ValidatorResult:
        """
        Determine if the given string CAn be converted to a valid color.
        """
        pass


class _FloatD4RGBColorStringConverter(_BaseRGBColorStringConverter):
    """
    Validator for a floating point RGB tuple.

    Example of a valid string: ``0.1560 -0.2681 1.5041``
    """

    # do not change on the class, change by subclass
    DECIMALS = 4
    DEFAULT_VALUE = 0.0
    SEPARATOR = " "

    @classmethod
    def fix(cls, user_input: str) -> str:
        """
        Convert the given string into a usable color.
        """
        if not user_input:
            return cls.from_color(DEFAULT_COLOR)

        fixed_input = user_input.lstrip(" ")
        fixed_input = fixed_input.rstrip(" ")
        fixed_input = re.sub(r"\s{2,}", " ", fixed_input)
        channels = fixed_input.split(" ")
        channel_number = len(channels)

        if channel_number > 3:
            # strip out additional channels
            channels = channels[:3]

        elif channel_number == 1:
            channels *= 3

        elif channel_number < 3:
            # add missing channels with default value
            channels += [f"{cls.DEFAULT_VALUE:.{cls.DECIMALS}f}"] * (3 - channel_number)

        fixed_channels = []
        for channel in channels:
            minus_char_number = channel.count("-")

            if channel.startswith("-") and minus_char_number == 1:
                fixed_channel = channel

            else:
                fixed_channel = channel.replace("-", "")

                if channel.startswith("-"):
                    fixed_channel = "-" + fixed_channel

            dot_char_number = fixed_channel.count(".")
            if dot_char_number >= 2:
                before, after = fixed_channel.split(".", 1)
                fixed_channel = before + "." + after.replace(".", "")

            fixed_channels.append(fixed_channel)

        fixed_input = cls.SEPARATOR.join(fixed_channels)
        color = cls.to_color(fixed_input)
        return cls.from_color(color)

    @classmethod
    def from_color(cls, color: RGBAColor) -> str:
        return (
            f"{color.r:.{cls.DECIMALS}f}{cls.SEPARATOR}"
            f"{color.g:.{cls.DECIMALS}f}{cls.SEPARATOR}"
            f"{color.b:.{cls.DECIMALS}f}"
        )

    @classmethod
    def to_color(cls, user_input: str) -> RGBAColor:
        """
        Args:
            user_input: example: ``0.253 -0.1 0.005``
        """
        if not user_input:
            return DEFAULT_COLOR

        channels = user_input.split(cls.SEPARATOR)
        channels = [float(channel) for channel in channels]
        return RGBAColor(*channels)

    @classmethod
    def validate(cls, user_input: str) -> ValidatorResult:
        if re.search(rf"[^\d.{cls.SEPARATOR}-]", user_input):
            return cls.Validations.invalid

        decimals = "\\d" * cls.DECIMALS
        if re.match(
            rf"^-?\d\.{decimals}{cls.SEPARATOR}-?\d\.{decimals}{cls.SEPARATOR}-?\d\.{decimals}$",
            user_input,
        ):
            return cls.Validations.valid

        return cls.Validations.acceptable


class _FloatD4TupleRGBColorStringConverter(_FloatD4RGBColorStringConverter):
    """
    Validator for a floating point RGB tuple represented as python tuple.

    Example of a valid string: ``0.1560 -0.2681 1.5041``
    """

    DECIMALS = 4
    DEFAULT_VALUE = 0.0
    SEPARATOR = ", "

    @classmethod
    def fix(cls, user_input: str) -> str:
        """
        Convert the given string into a usable color.
        """
        if not user_input:
            return cls.from_color(DEFAULT_COLOR)

        fixed_str = user_input.lstrip("(").rstrip(")")
        fixed_str = fixed_str.replace(" ", "")
        channels = fixed_str.split(",")
        fixed_str = super().fix(" ".join(channels))
        color = cls.to_color(fixed_str)
        return cls.from_color(color)

    @classmethod
    def from_color(cls, color: RGBAColor) -> str:
        return (
            f"({color.r:.{cls.DECIMALS}f}{cls.SEPARATOR}"
            f"{color.g:.{cls.DECIMALS}f}{cls.SEPARATOR}"
            f"{color.b:.{cls.DECIMALS}f})"
        )

    @classmethod
    def to_color(cls, user_input: str) -> RGBAColor:
        """
        Args:
            user_input: example: ``(0.253, -0.1, 0.005)``
        """

        if not user_input:
            return DEFAULT_COLOR

        user_input = user_input.lstrip("(").rstrip(")")
        channels = user_input.split(cls.SEPARATOR)
        channels = [float(channel) for channel in channels]
        return RGBAColor(*channels)

    @classmethod
    def validate(cls, user_input: str) -> ValidatorResult:
        simplified_input = user_input.lstrip("(").rstrip(")")

        if re.search(rf"[^\d.{cls.SEPARATOR}-]", simplified_input) or re.search(
            r", *-{2,},", simplified_input
        ):
            return cls.Validations.invalid

        decimals = "\\d" * cls.DECIMALS
        if re.match(
            rf"^\(-?\d\.{decimals}{cls.SEPARATOR}-?\d\.{decimals}{cls.SEPARATOR}-?\d\.{decimals}\)$",
            user_input,
        ):
            return cls.Validations.valid

        return cls.Validations.acceptable


class _UInt8RGBColorStringConverter(_BaseRGBColorStringConverter):
    """
    Validator for a 8bit unsigned integers RGB colors.

    Example of a valid string: ``126 0 255``
    """

    DEFAULT_VALUE = 0
    SEPARATOR = " "

    @classmethod
    def fix(cls, user_input: str) -> str:
        """
        Convert the given string into a usable color.
        """
        if not user_input:
            return cls.from_color(DEFAULT_COLOR)

        fixed_input = user_input.lstrip(" ")
        fixed_input = fixed_input.rstrip(" ")
        fixed_input = re.sub(r"\s{2,}", "", fixed_input)
        channels = fixed_input.split(" ")
        channel_number = len(channels)

        if channel_number > 3:
            # strip out additional channels
            channels = channels[:3]

        elif channel_number == 1:
            channels *= 3

        elif channel_number < 3:
            # add missing channels with default value
            channels += [f"{int(cls.DEFAULT_VALUE)}"] * (3 - channel_number)

        fixed_channels = []
        for channel in channels:
            # if a channel is more than 3 number it's usually a typo so just remove it
            fixed_channel = channel[:3]
            fixed_channel_value = int(fixed_channel)
            # clamp to 255
            fixed_channel_value = min(fixed_channel_value, 255)
            fixed_channels.append(str(fixed_channel_value))

        fixed_input = cls.SEPARATOR.join(fixed_channels)
        color = cls.to_color(fixed_input)
        return cls.from_color(color)

    @classmethod
    def from_color(cls, color: RGBAColor) -> str:
        color_tuple = color.to_int8(alpha=False)
        return (
            f"{color_tuple[0]}{cls.SEPARATOR}"
            f"{color_tuple[1]}{cls.SEPARATOR}"
            f"{color_tuple[2]}"
        )

    @classmethod
    def to_color(cls, user_input: str) -> RGBAColor:
        """
        Args:
            user_input: example: ``0.253 -0.1 0.005``
        """
        if not user_input:
            return DEFAULT_COLOR

        channels = user_input.split(cls.SEPARATOR)
        channels = [int(channel) for channel in channels]
        return RGBAColor.from_int8(*channels)

    @classmethod
    def validate(cls, user_input: str) -> ValidatorResult:
        if re.search(rf"[^\d{cls.SEPARATOR}]", user_input):
            return cls.Validations.invalid

        if re.match(
            rf"^\d{{1,3}}{cls.SEPARATOR}\d{{1,3}}{cls.SEPARATOR}\d{{1,3}}$",
            user_input,
        ):
            r, g, b = user_input.split(cls.SEPARATOR)
            if int(r) > 255 or int(g) > 255 or int(b) > 255:
                # allowed cause clamped in fix() method anyway
                return cls.Validations.acceptable

            return cls.Validations.valid

        return cls.Validations.acceptable


class _HexRGBColorStringConverter(_BaseRGBColorStringConverter):
    """
    Validator for a hexadecimal RGB colors.

    Example of a valid string: ``#78BD68``
    """

    @classmethod
    def fix(cls, user_input: str) -> str:
        """
        Convert the given string into a usable color.
        """
        if not user_input:
            return cls.from_color(DEFAULT_COLOR)

        sanitized_user_input = user_input.lstrip("#").lower()
        sanitized_user_input = sanitized_user_input[:6]

        if len(sanitized_user_input) == 2:
            fixed_input = sanitized_user_input * 3
        else:
            fixed_input = sanitized_user_input.ljust(6, "0")

        return f"#{fixed_input}"

    @classmethod
    def from_color(cls, color: RGBAColor) -> str:
        return color.to_hex()

    @classmethod
    def to_color(cls, user_input: str) -> RGBAColor:
        """
        Args:
            user_input: example: ``#78BD68``
        """
        if not user_input:
            return DEFAULT_COLOR

        return RGBAColor.from_hex(user_input)

    @classmethod
    def validate(cls, user_input: str) -> ValidatorResult:
        if not user_input.startswith("#"):
            return cls.Validations.invalid

        sanitized_input = user_input.lstrip("#").lower()

        if re.search("[^a-f0-9]", sanitized_input):
            return cls.Validations.invalid

        if re.match(r"^#[A-Fa-f0-9]{6}$", user_input):
            return cls.Validations.valid

        return cls.Validations.acceptable


class ColorStringFormat(enum.Enum):
    """
    Define one item for each :class:`BaseRGBColorStringConverter` subclass.

    Might be used to populate a GUI.
    """

    float_d4 = "float.4"
    float_d4_tuple = "(float.4,)"
    uint8 = "uint8"
    hex = "hexadecimal"


def _get_class_from_format(
    str_format: ColorStringFormat,
) -> Type[_BaseRGBColorStringConverter]:
    """
    Constructor converting enum to class.
    """
    mapping = {
        str_format.float_d4: _FloatD4RGBColorStringConverter,
        str_format.float_d4_tuple: _FloatD4TupleRGBColorStringConverter,
        str_format.uint8: _UInt8RGBColorStringConverter,
        str_format.hex: _HexRGBColorStringConverter,
    }
    converter_class = mapping.get(str_format)
    if converter_class is None:
        raise ValueError(f"Unsupported string format {str_format}")

    return converter_class


def convert_str_to_color(user_str: str, str_format: ColorStringFormat) -> RGBAColor:
    """
    Convert string in the given format to a color instance.
    """
    converter_class = _get_class_from_format(str_format)
    return converter_class.to_color(user_str)


def convert_color_to_str(color: RGBAColor, str_format: ColorStringFormat) -> str:
    """
    Convert a color instance to a string in the given format.
    """
    converter_class = _get_class_from_format(str_format)
    return converter_class.from_color(color)


def validate_color_str(user_str: str, str_format: ColorStringFormat) -> ValidatorResult:
    """
    Determine if the given string CAN be converted to a valid color in the given format.
    """
    converter_class = _get_class_from_format(str_format)
    return converter_class.validate(user_str)


def fix_color_str(user_str: str, str_format: ColorStringFormat) -> str:
    """
    Sanitize the given string, so it can be a valid represention of a color instance as string.
    """
    converter_class = _get_class_from_format(str_format)
    return converter_class.fix(user_str)
