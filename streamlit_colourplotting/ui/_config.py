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


class DiagramMethod(enum.Enum):
    cie1931 = "CIE 1931"
    cie1960 = "CIE 1960 UCS"
    cie1976 = "CIE 1976 UCS"

    @classmethod
    def labels(cls) -> list[str]:
        return [item.value for item in cls]


class UserConfig:
    def __init__(self):
        # note: session_state doesn't work well with Enums

        if "USER_SOURCE_TYPE" not in streamlit.session_state:
            streamlit.session_state["USER_SOURCE_TYPE"] = SourceType.color.value
        if "USER_DIAGRAM_METHOD" not in streamlit.session_state:
            streamlit.session_state["USER_DIAGRAM_METHOD"] = DiagramMethod.cie1976.value
        if "USER_DIAGRAM_SHOW_BACKGROUND" not in streamlit.session_state:
            streamlit.session_state["USER_DIAGRAM_SHOW_BACKGROUND"] = False
        if "USER_RGB_LOCUS" not in streamlit.session_state:
            streamlit.session_state["USER_RGB_LOCUS"] = True
        if "USER_TRANSPARENT_BACKGROUND" not in streamlit.session_state:
            streamlit.session_state["USER_TRANSPARENT_BACKGROUND"] = False
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
    def USER_DIAGRAM_METHOD(self) -> DiagramMethod:
        return DiagramMethod(streamlit.session_state["USER_DIAGRAM_METHOD"])

    @USER_DIAGRAM_METHOD.setter
    def USER_DIAGRAM_METHOD(self, new_value: DiagramMethod):
        streamlit.session_state["USER_DIAGRAM_METHOD"] = new_value.value

    @property
    def USER_DIAGRAM_SHOW_BACKGROUND(self) -> bool:
        return streamlit.session_state["USER_DIAGRAM_SHOW_BACKGROUND"]

    @USER_DIAGRAM_SHOW_BACKGROUND.setter
    def USER_DIAGRAM_SHOW_BACKGROUND(self, new_value: bool):
        streamlit.session_state["USER_DIAGRAM_SHOW_BACKGROUND"] = new_value

    @property
    def USER_RGB_LOCUS(self) -> bool:
        return streamlit.session_state["USER_RGB_LOCUS"]

    @USER_RGB_LOCUS.setter
    def USER_RGB_LOCUS(self, new_value: bool):
        streamlit.session_state["USER_RGB_LOCUS"] = new_value

    @property
    def USER_TRANSPARENT_BACKGROUND(self) -> bool:
        return streamlit.session_state["USER_TRANSPARENT_BACKGROUND"]

    @USER_TRANSPARENT_BACKGROUND.setter
    def USER_TRANSPARENT_BACKGROUND(self, new_value: bool):
        streamlit.session_state["USER_TRANSPARENT_BACKGROUND"] = new_value

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
            # NOTE: bug with 1976 method, doesn't accept 1x1 array
            image = numpy.full([2, 2, 3], self.color.to_array(alpha=False))
            return image
        else:
            # TODO when image implemented
            raise NotImplementedError()

    @property
    def plot(self) -> tuple[matplotlib.pyplot.Figure, matplotlib.pyplot.Axes]:
        samples = 10
        image = self.image

        if image.shape[0] > samples or image.shape[1] > samples:
            image: numpy.ndarray = image[::samples, ::samples, ...]

        colorspace = self.USER_SOURCE_COLORSPACE
        if self.USER_SOURCE_FORCE_LINEAR:
            colorspace = self.USER_SOURCE_COLORSPACE.as_linear_copy()

        colour_colorspace = colorspace.as_colour_colorspace()

        if self.USER_DIAGRAM_METHOD == DiagramMethod.cie1931:
            plot_RGB_chromaticities_function = (
                colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1931
            )
        elif self.USER_DIAGRAM_METHOD == DiagramMethod.cie1960:
            plot_RGB_chromaticities_function = (
                colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1960UCS
            )
        elif self.USER_DIAGRAM_METHOD == DiagramMethod.cie1976:
            plot_RGB_chromaticities_function = (
                colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1976UCS
            )
        else:
            raise ValueError(f"Unsupported diagram method {self.USER_DIAGRAM_METHOD}")

        (
            figure,
            axes,
        ) = plot_RGB_chromaticities_function(
            image,
            colourspace=colour_colorspace,
            colourspaces=[colour_colorspace],
            # scatter_kwargs={
            #     "s": 90,  # size
            #     "c": [1, 1, 1],  # color
            #     "marker": "+",
            #     "zorder": 0,
            # },
            # styling
            spectral_locus_colours="RGB" if self.USER_RGB_LOCUS else None,
            show_diagram_colours=self.USER_DIAGRAM_SHOW_BACKGROUND,
            transparent_background=self.USER_TRANSPARENT_BACKGROUND,
            standalone=False,
        )
        return figure, axes


def config() -> UserConfig:
    """
    Return a user configuration instance.
    """
    return UserConfig()
