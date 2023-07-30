import enum
import io
from typing import Optional
from typing import Union

import cocoon
import colour
import matplotlib.style
import matplotlib.pyplot
import numpy
import streamlit
from cocoon import RgbColorspace
from cocoon import sRGB_COLORSPACE
from cocoon.color import RGBAColor
from cocoon.color import ColorStringFormat

import streamlit_colourplotting.core
from streamlit_colourplotting._utils import UifiedEnum


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


class MarkerShapeStyle(UifiedEnum):
    """
    Based on :class:`matplotlib.markers.MarkerStyle.markers`
    """

    point = (".", ".")
    pixel = (",", ",")
    circle = ("o", "o")
    plus = ("+", "+")
    x = ("x", "x")
    star = ("*", "*")
    triangle_down = ("v", "v")
    triangle_up = ("^", "^")
    triangle_left = ("<", "<")
    triangle_right = (">", ">")
    tri_down = ("tri1", "1")
    tri_up = ("tri2", "2")
    tri_left = ("tri3", "3")
    tri_right = ("tri4", "4")
    octagon = ("octagon", "8")
    square = ("■", "s")
    pentagon = ("penta", "p")
    hexagon1 = ("hexa", "h")
    hexagon2 = ("Hexa", "H")
    diamond = ("◆", "D")
    thin_diamond = ("◇", "d")
    vline = ("|", "|")
    hline = ("_", "_")
    plus_filled = ("P", "P")
    x_filled = ("X", "X")
    tickleft = ("0", 0)
    tickright = ("1", 1)
    tickup = ("2", 2)
    tickdown = ("3", 3)
    caretleft = ("4", 4)
    caretright = ("5", 5)
    caretup = ("6", 6)
    caretdown = ("7", 7)
    caretleftbase = ("8", 8)
    caretrightbase = ("9", 9)
    caretupbase = ("10", 10)
    caretdownbase = ("11", 11)


class UserConfig:
    SOURCE_COLORSPACE_TOKEN = "$SOURCE_COLORSPACE$"

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
        if "USER_SCATTER_SIZE" not in streamlit.session_state:
            streamlit.session_state["USER_SCATTER_SIZE"] = 25.0
        if "USER_SCATTER_COLOR" not in streamlit.session_state:
            streamlit.session_state["USER_SCATTER_COLOR"] = "#53DD97"
        if "USER_SCATTER_COLOR_RGB" not in streamlit.session_state:
            streamlit.session_state["USER_SCATTER_COLOR_RGB"] = True
        if "USER_MARKER_STYLE" not in streamlit.session_state:
            streamlit.session_state["USER_MARKER_STYLE"] = MarkerShapeStyle.circle.value
        if "USER_PLOT_POINTER_GAMUT" not in streamlit.session_state:
            streamlit.session_state["USER_PLOT_POINTER_GAMUT"] = False
        if "USER_POINTER_GAMUT_ALPHA" not in streamlit.session_state:
            streamlit.session_state["USER_POINTER_GAMUT_ALPHA"] = 1.0
        if "USER_SHOW_WHITEPOINT" not in streamlit.session_state:
            streamlit.session_state["USER_SHOW_WHITEPOINT"] = True
        if "USER_IMAGE" not in streamlit.session_state:
            streamlit.session_state["USER_IMAGE"] = None
        if "USER_IMAGE_SAMPLES" not in streamlit.session_state:
            streamlit.session_state["USER_IMAGE_SAMPLES"] = 10
        if "USER_STYLE" not in streamlit.session_state:
            streamlit.session_state["USER_STYLE"] = {}
        if "USER_FIGURE_COLORSPACES" not in streamlit.session_state:
            streamlit.session_state["USER_FIGURE_COLORSPACES"] = [
                (self.SOURCE_COLORSPACE_TOKEN, "#F44336")
            ]

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
    def USER_SCATTER_SIZE(self) -> float:
        return streamlit.session_state["USER_SCATTER_SIZE"]

    @USER_SCATTER_SIZE.setter
    def USER_SCATTER_SIZE(self, new_value: float):
        streamlit.session_state["USER_SCATTER_SIZE"] = new_value

    @property
    def USER_SCATTER_COLOR(self) -> str:
        return streamlit.session_state["USER_SCATTER_COLOR"]

    @USER_SCATTER_COLOR.setter
    def USER_SCATTER_COLOR(self, new_value: str):
        streamlit.session_state["USER_SCATTER_COLOR"] = new_value

    @property
    def USER_SCATTER_COLOR_RGB(self) -> bool:
        return streamlit.session_state["USER_SCATTER_COLOR_RGB"]

    @USER_SCATTER_COLOR_RGB.setter
    def USER_SCATTER_COLOR_RGB(self, new_value: bool):
        streamlit.session_state["USER_SCATTER_COLOR_RGB"] = new_value

    @property
    def USER_MARKER_STYLE(self) -> MarkerShapeStyle:
        return MarkerShapeStyle(streamlit.session_state["USER_MARKER_STYLE"])

    @USER_MARKER_STYLE.setter
    def USER_MARKER_STYLE(self, new_value: MarkerShapeStyle):
        streamlit.session_state["USER_MARKER_STYLE"] = new_value.value

    @property
    def USER_PLOT_POINTER_GAMUT(self) -> bool:
        return streamlit.session_state["USER_PLOT_POINTER_GAMUT"]

    @USER_PLOT_POINTER_GAMUT.setter
    def USER_PLOT_POINTER_GAMUT(self, new_value: bool):
        streamlit.session_state["USER_PLOT_POINTER_GAMUT"] = new_value

    @property
    def USER_POINTER_GAMUT_ALPHA(self) -> float:
        return streamlit.session_state["USER_POINTER_GAMUT_ALPHA"]

    @USER_POINTER_GAMUT_ALPHA.setter
    def USER_POINTER_GAMUT_ALPHA(self, new_value: float):
        streamlit.session_state["USER_POINTER_GAMUT_ALPHA"] = new_value

    @property
    def USER_SHOW_WHITEPOINT(self) -> bool:
        return streamlit.session_state["USER_SHOW_WHITEPOINT"]

    @USER_SHOW_WHITEPOINT.setter
    def USER_SHOW_WHITEPOINT(self, new_value: bool):
        streamlit.session_state["USER_SHOW_WHITEPOINT"] = new_value

    @property
    def USER_IMAGE(self) -> Optional[numpy.ndarray]:
        return streamlit.session_state["USER_IMAGE"]

    @USER_IMAGE.setter
    def USER_IMAGE(self, new_value: Optional[numpy.ndarray]):
        streamlit.session_state["USER_IMAGE"] = new_value

    @property
    def USER_IMAGE_SAMPLES(self) -> int:
        return streamlit.session_state["USER_IMAGE_SAMPLES"]

    @USER_IMAGE_SAMPLES.setter
    def USER_IMAGE_SAMPLES(self, new_value: int):
        streamlit.session_state["USER_IMAGE_SAMPLES"] = new_value

    @property
    def USER_STYLE(self) -> dict:
        return streamlit.session_state["USER_STYLE"]

    @USER_STYLE.setter
    def USER_STYLE(self, new_value: dict):
        streamlit.session_state["USER_STYLE"] = new_value

    @property
    def USER_FIGURE_COLORSPACES(self) -> list[Optional[str], str]:
        return streamlit.session_state["USER_FIGURE_COLORSPACES"]

    @USER_FIGURE_COLORSPACES.setter
    def USER_FIGURE_COLORSPACES(self, new_value: list[Optional[str], str]):
        streamlit.session_state["USER_FIGURE_COLORSPACES"] = new_value

    @property
    def _source_colorspace(self) -> cocoon.RgbColorspace:
        colorspace = self.USER_SOURCE_COLORSPACE

        if self.USER_SOURCE_FORCE_LINEAR:
            colorspace = self.USER_SOURCE_COLORSPACE.as_linear_copy()

        return colorspace

    @property
    def _figure_colorspaces(self) -> dict[colour.RGB_Colourspace, str]:
        figure_colorspaces = {}
        _figure_colorspaces = self.USER_FIGURE_COLORSPACES

        for colorspace_name, color in _figure_colorspaces:
            if colorspace_name == self.SOURCE_COLORSPACE_TOKEN:
                colorspace = self._source_colorspace.as_colour_colorspace()

            elif colorspace_name is None:
                continue

            else:
                colorspace = cocoon.get_colorspace(colorspace_name)
                colorspace = colorspace.as_colour_colorspace()

            figure_colorspaces[colorspace] = color

        return figure_colorspaces

    @property
    def color(self) -> RGBAColor:
        colorspace = self.USER_SOURCE_COLORSPACE
        color = self.USER_SOURCE_COLOR.as_colorspace(colorspace)

        if self.USER_SOURCE_FORCE_LINEAR:
            colorspace = colorspace.as_linear_copy()
            color = color.as_colorspace(colorspace)

        return color

    @property
    def image(self) -> numpy.ndarray:
        """
        Return a floating point R-G-B image with an arbitrary dimension.
        """
        if self.USER_SOURCE_TYPE == SourceType.color:
            # NOTE: bug with 1976 method, doesn't accept 1x1 array
            image = numpy.full([2, 2, 3], self.color.to_array(alpha=False))
            return image

        elif self.USER_SOURCE_TYPE == SourceType.image:
            samples = self.USER_IMAGE_SAMPLES
            image = self.USER_IMAGE
            source_colorspace = self._source_colorspace

            if image is None:
                return numpy.full([2, 2, 3], [0.0, 0.0, 0.0])

            if image.shape[0] > samples or image.shape[1] > samples:
                image = image[::samples, ::samples, ...]

            # NOTE: colour plotting function expect linear encoding
            if not source_colorspace.transfer_functions.is_decoding_linear:
                image = source_colorspace.transfer_functions.decoding(image)

            return image

    @property
    def plot(self) -> tuple[matplotlib.pyplot.Figure, matplotlib.pyplot.Axes]:
        image = self.image
        colorspace = self._source_colorspace
        colour_colorspace = colorspace.as_colour_colorspace()
        figure_colorspaces = self._figure_colorspaces

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

        plot_settings = {}
        if figure_colorspaces:
            colors = list(figure_colorspaces.values())
            if len(colors) == 1:
                # ensure the list is always of len 2 at minimum
                colors.append("#000000")
            color_map = matplotlib.colors.LinearSegmentedColormap.from_list(
                "user", colors
            )
            plot_settings["colour_cycle_map"] = color_map

        marker_color = "RGB" if self.USER_SCATTER_COLOR_RGB else self.USER_SCATTER_COLOR
        with matplotlib.style.context(self.USER_STYLE):
            (
                figure,
                axes,
            ) = plot_RGB_chromaticities_function(
                image,
                colourspace=colour_colorspace,
                colourspaces=list(figure_colorspaces.keys()),
                scatter_kwargs={
                    "s": self.USER_SCATTER_SIZE,
                    "c": marker_color,
                    "marker": self.USER_MARKER_STYLE.as_core(),
                    "zorder": 0,
                },
                # styling
                spectral_locus_colours="RGB" if self.USER_RGB_LOCUS else None,
                show_diagram_colours=self.USER_DIAGRAM_SHOW_BACKGROUND,
                show_whitepoints=self.USER_SHOW_WHITEPOINT,
                show_pointer_gamut=self.USER_PLOT_POINTER_GAMUT,
                pointer_gamut_opacity=self.USER_POINTER_GAMUT_ALPHA,
                standalone=False,
                **plot_settings,
            )
        return figure, axes


def config() -> UserConfig:
    """
    Return a user configuration instance.
    """
    return UserConfig()
