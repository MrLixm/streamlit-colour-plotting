import enum

import colour
import matplotlib.pyplot
import numpy
import streamlit
from cocoon import RgbColorspace
from cocoon import sRGB_COLORSPACE
from cocoon.color import RGBAColor
from cocoon.color import ColorStringFormat


class SourceType(enum.Enum):
    color = "Color"
    image = "Image"

    @classmethod
    def labels(cls) -> list[str]:
        return [item.value for item in cls]


class UserIssue(enum.IntFlag):
    """
    A specific issue that can happen during interaction with interface. They can be combined.
    """

    unset = enum.auto()
    value_error = enum.auto()
    hex_colorspace = enum.auto()
    hex_force_linear = enum.auto()


class UserConfig:
    def __init__(self):
        # note: session_state doesn't work well with Enums

        if "USER_SOURCE_TYPE" not in streamlit.session_state:
            streamlit.session_state["USER_SOURCE_TYPE"] = SourceType.color.value
        if "USER_SOURCE_COLOR" not in streamlit.session_state:
            streamlit.session_state["USER_SOURCE_COLOR"] = RGBAColor(0.0, 0.0, 0.0)
        if "USER_SOURCE_COLORSPACE" not in streamlit.session_state:
            streamlit.session_state["USER_SOURCE_COLORSPACE"] = sRGB_COLORSPACE
        if "USER_SOURCE_FORCE_LINEAR" not in streamlit.session_state:
            streamlit.session_state["USER_SOURCE_FORCE_LINEAR"] = False
        if "USER_SOURCE_COLOR_FORMAT" not in streamlit.session_state:
            k = "USER_SOURCE_COLOR_FORMAT"
            streamlit.session_state[k] = ColorStringFormat.float_d4.value
        if "USER_SOURCE_ERROR" not in streamlit.session_state:
            streamlit.session_state["USER_SOURCE_ERROR"] = UserIssue.unset.value

    @property
    def USER_SOURCE_TYPE(self) -> SourceType:
        return SourceType(streamlit.session_state["USER_SOURCE_TYPE"])

    @USER_SOURCE_TYPE.setter
    def USER_SOURCE_TYPE(self, new_value: SourceType):
        streamlit.session_state["USER_SOURCE_TYPE"] = new_value.value

    @property
    def USER_SOURCE_COLOR(self) -> RGBAColor:
        return streamlit.session_state["USER_SOURCE_COLOR"]

    @USER_SOURCE_COLOR.setter
    def USER_SOURCE_COLOR(self, new_value: RGBAColor):
        streamlit.session_state["USER_SOURCE_COLOR"] = new_value

    @property
    def USER_SOURCE_COLOR_FORMAT(self) -> ColorStringFormat:
        return ColorStringFormat(streamlit.session_state["USER_SOURCE_COLOR_FORMAT"])

    @USER_SOURCE_COLOR_FORMAT.setter
    def USER_SOURCE_COLOR_FORMAT(self, new_value: ColorStringFormat):
        streamlit.session_state["USER_SOURCE_COLOR_FORMAT"] = new_value.value

    @property
    def USER_SOURCE_COLORSPACE(self) -> RgbColorspace:
        return streamlit.session_state["USER_SOURCE_COLORSPACE"]

    @USER_SOURCE_COLORSPACE.setter
    def USER_SOURCE_COLORSPACE(self, new_value: RgbColorspace):
        streamlit.session_state["USER_SOURCE_COLORSPACE"] = new_value

    @property
    def USER_SOURCE_FORCE_LINEAR(self) -> bool:
        return streamlit.session_state["USER_SOURCE_FORCE_LINEAR"]

    @USER_SOURCE_FORCE_LINEAR.setter
    def USER_SOURCE_FORCE_LINEAR(self, new_value: bool):
        streamlit.session_state["USER_SOURCE_FORCE_LINEAR"] = new_value

    @property
    def USER_SOURCE_ERROR(self) -> UserIssue:
        return UserIssue(streamlit.session_state["USER_SOURCE_ERROR"])

    @USER_SOURCE_ERROR.setter
    def USER_SOURCE_ERROR(self, new_value: UserIssue):
        streamlit.session_state["USER_SOURCE_ERROR"] = new_value.value

    @property
    def color(self) -> RGBAColor:
        colorspace = self.USER_SOURCE_COLORSPACE
        if self.USER_SOURCE_FORCE_LINEAR:
            colorspace = colorspace.as_linear_copy()
        color = self.USER_SOURCE_COLOR.as_colorspace(colorspace)
        return color

    @property
    def image(self) -> numpy.ndarray:
        if self.USER_SOURCE_TYPE == SourceType.color:
            image = numpy.full([1, 1, 3], self.color.to_array(alpha=False))
            return image
        else:
            # TODO when image implemented
            raise NotImplementedError()

    @property
    def plot(self) -> tuple[matplotlib.pyplot.Figure, matplotlib.pyplot.Axes]:
        samples = 10
        colorspace = self.USER_SOURCE_COLORSPACE
        if self.USER_SOURCE_FORCE_LINEAR:
            colorspace = self.USER_SOURCE_COLORSPACE.as_linear_copy()

        colour_colorspace = colorspace.as_colour_colorspace()

        (
            figure,
            axes,
        ) = colour.plotting.models.plot_RGB_chromaticities_in_chromaticity_diagram(
            self.image[::samples, ::samples, ...],
            colourspace=colour_colorspace,
            colourspaces=[colour_colorspace],
            # scatter_kwargs={
            #     "s": 90,  # size
            #     "c": [1, 1, 1],  # color
            #     "marker": "+",
            #     "zorder": 0,
            # },
            # styling
            spectral_locus_colours="RGB",
            show_diagram_colours=False,
            transparent_background=False,
            standalone=False,
        )
        return figure, axes


def config() -> UserConfig:
    """
    Return a user configuration instance.
    """
    return UserConfig()
