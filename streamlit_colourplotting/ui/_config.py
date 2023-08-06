import enum
from typing import Generic
from typing import Optional
from typing import TypeVar

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

from streamlit_colourplotting._utils import UifiedEnum
from streamlit_colourplotting.core import transform_box


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


T = TypeVar("T")


class UserConfigOption(Generic[T]):
    """
    An option set by the user for its current session.
    """

    def __init__(self, default: T, identifier: str):
        self._default = default
        self._identifier = identifier

        if self._identifier not in streamlit.session_state:
            self.set(self._default)

    @property
    def default(self) -> T:
        return self._default

    def get(self) -> T:
        value = streamlit.session_state[self._identifier]
        # XXX: issues with enum and streamlit rerun, cannot store an enum instance
        if isinstance(self._default, enum.Enum):
            value = self._default.__class__(value)

        return value

    def set(self, new_value: T):
        # XXX: issues with enum and streamlit rerun, cannot store an enum instance
        if isinstance(self._default, enum.Enum):
            streamlit.session_state[self._identifier] = new_value.value
        else:
            streamlit.session_state[self._identifier] = new_value


class UserConfig:
    SOURCE_COLORSPACE_TOKEN = "$SOURCE_COLORSPACE$"

    def __init__(self):
        self.USER_SOURCE_TYPE = UserConfigOption(SourceType.color, "USER_SOURCE_TYPE")
        self.USER_DIAGRAM_METHOD = UserConfigOption(
            DiagramMethod.cie1976, "USER_DIAGRAM_METHOD"
        )
        self.USER_LOCUS_BACKGROUND_RGB = UserConfigOption(
            False, "USER_LOCUS_BACKGROUND_RGB"
        )
        self.USER_LOCUS_SHOW = UserConfigOption(True, "USER_LOCUS_SHOW")
        self.USER_LOCUS_COLOR_RGB = UserConfigOption(True, "USER_LOCUS_COLOR_RGB")
        self.USER_LOCUS_COLOR = UserConfigOption("#4e4e4e", "USER_LOCUS_COLOR")
        self.USER_LOCUS_ALPHA = UserConfigOption(1.0, "USER_LOCUS_ALPHA")
        self.USER_SOURCE_COLOR = UserConfigOption(
            RGBAColor(0.0, 0.0, 0.0), "USER_SOURCE_COLOR"
        )
        self.USER_SOURCE_COLORSPACE: UserConfigOption[RgbColorspace] = UserConfigOption(
            sRGB_COLORSPACE, "USER_SOURCE_COLORSPACE"
        )
        self.USER_SOURCE_FORCE_LINEAR = UserConfigOption(
            False, "USER_SOURCE_FORCE_LINEAR"
        )
        self.USER_SOURCE_COLOR_FORMAT = UserConfigOption(
            ColorStringFormat.float_d4, "USER_SOURCE_COLOR_FORMAT"
        )
        self.USER_SOURCE_ERROR = UserConfigOption(UserIssue.unset, "USER_SOURCE_ERROR")
        self.USER_SCATTER_SIZE = UserConfigOption(25.0, "USER_SCATTER_SIZE")
        self.USER_SCATTER_COLOR = UserConfigOption("#53DD97", "USER_SCATTER_COLOR")
        self.USER_SCATTER_COLOR_RGB = UserConfigOption(True, "USER_SCATTER_COLOR_RGB")
        self.USER_SCATTER_ALPHA = UserConfigOption(0.85, "USER_SCATTER_ALPHA")
        self.USER_MARKER_STYLE = UserConfigOption(
            MarkerShapeStyle.circle, "USER_MARKER_STYLE"
        )
        self.USER_PLOT_POINTER_GAMUT = UserConfigOption(
            False, "USER_PLOT_POINTER_GAMUT"
        )
        self.USER_POINTER_GAMUT_COLOR = UserConfigOption(
            "#555555", "USER_POINTER_GAMUT_COLOR"
        )
        self.USER_POINTER_GAMUT_ALPHA = UserConfigOption(
            1.0, "USER_POINTER_GAMUT_ALPHA"
        )
        self.USER_SHOW_WHITEPOINT = UserConfigOption(True, "USER_SHOW_WHITEPOINT")
        self.USER_IMAGE: UserConfigOption[Optional[numpy.ndarray]] = UserConfigOption(
            None, "USER_IMAGE"
        )
        self.USER_IMAGE_SAMPLES = UserConfigOption(20, "USER_IMAGE_SAMPLES")
        self.USER_STYLE = UserConfigOption({}, "USER_STYLE")
        self.USER_FIGURE_COLORSPACES: UserConfigOption[
            list[tuple[str, str]]
        ] = UserConfigOption(
            [(self.SOURCE_COLORSPACE_TOKEN, "#F44336")], "USER_FIGURE_COLORSPACES"
        )
        self.USER_SHOW_LEGEND = UserConfigOption(True, "USER_SHOW_LEGEND")
        self.USER_SHOW_AXES = UserConfigOption(True, "USER_SHOW_AXES")
        self.USER_SHOW_GRID = UserConfigOption(False, "USER_SHOW_GRID")
        self.USER_GRID_COLOR = UserConfigOption("#CACACA", "USER_GRID_COLOR")
        self.USER_GRID_ALPHA = UserConfigOption(0.5, "USER_GRID_ALPHA")
        self.USER_AXES_SCALE = UserConfigOption(1.0, "USER_AXES_SCALE")
        self.USER_AXES_OFFSET_X = UserConfigOption(0.0, "USER_AXES_OFFSET_X")
        self.USER_AXES_OFFSET_Y = UserConfigOption(0.0, "USER_AXES_OFFSET_Y")

    @property
    def source_colorspace(self) -> cocoon.RgbColorspace:
        """
        Full colorspace specification describing the source (linearized or not)
        """
        colorspace = self.USER_SOURCE_COLORSPACE.get()

        if self.USER_SOURCE_FORCE_LINEAR.get():
            colorspace = self.USER_SOURCE_COLORSPACE.get().as_linear_copy()

        return colorspace

    @property
    def color(self) -> RGBAColor:
        colorspace = self.USER_SOURCE_COLORSPACE.get()
        color = self.USER_SOURCE_COLOR.get().as_colorspace(colorspace)

        if self.USER_SOURCE_FORCE_LINEAR.get():
            colorspace = colorspace.as_linear_copy()
            color = color.as_colorspace(colorspace)

        return color

    def _get_figure_colorspaces(self) -> dict[colour.RGB_Colourspace, str]:
        """
        Generate a list of colorspace to display in the graph with their associated display color.

        Returns:
            dict["colorspace instance", "hexadecimal color"]
        """
        figure_colorspaces = {}
        _figure_colorspaces = self.USER_FIGURE_COLORSPACES.get()

        for colorspace_name, color in _figure_colorspaces:
            if colorspace_name == self.SOURCE_COLORSPACE_TOKEN:
                colorspace = self.source_colorspace.as_colour_colorspace()

            elif colorspace_name is None:
                continue

            else:
                colorspace = cocoon.get_colorspace(colorspace_name)
                colorspace = colorspace.as_colour_colorspace()

            figure_colorspaces[colorspace] = color

        return figure_colorspaces

    def generate_image(self) -> numpy.ndarray:
        """
        Return a floating point R-G-B image with an arbitrary dimension.
        """
        if self.USER_SOURCE_TYPE.get() == SourceType.color:
            # NOTE: bug with 1976 method, doesn't accept 1x1 array
            image = numpy.full([2, 2, 3], self.color.to_array(alpha=False))
            return image

        elif self.USER_SOURCE_TYPE.get() == SourceType.image:
            samples = self.USER_IMAGE_SAMPLES.get()
            image = self.USER_IMAGE.get()
            source_colorspace = self.source_colorspace

            if image is None:
                return numpy.full([2, 2, 3], [0.0, 0.0, 0.0])

            if image.shape[0] > samples or image.shape[1] > samples:
                image = image[::samples, ::samples, ...]

            # NOTE: colour plotting function expect linear encoding
            if not source_colorspace.transfer_functions.is_decoding_linear:
                image = source_colorspace.transfer_functions.decoding(image)

            return image

        else:
            raise ValueError(f"Unsupported enum value: {self.USER_SOURCE_TYPE.get()}")

    def generate_plot(self) -> tuple[matplotlib.pyplot.Figure, matplotlib.pyplot.Axes]:
        """
        Generate the matplotlib graph using all the options previously configured.
        """
        image = self.generate_image()
        colorspace = self.source_colorspace
        colour_colorspace = colorspace.as_colour_colorspace()
        figure_colorspaces = self._get_figure_colorspaces()
        diagram_method = self.USER_DIAGRAM_METHOD.get()

        if diagram_method == diagram_method.cie1931:
            plot_RGB_chromaticities_function = (
                colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1931
            )
        elif diagram_method == diagram_method.cie1960:
            plot_RGB_chromaticities_function = (
                colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1960UCS
            )
        elif diagram_method == diagram_method.cie1976:
            plot_RGB_chromaticities_function = (
                colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1976UCS
            )
        else:
            raise ValueError(f"Unsupported diagram method {diagram_method}")

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

        marker_color = (
            "RGB"
            if self.USER_SCATTER_COLOR_RGB.get()
            else self.USER_SCATTER_COLOR.get()
        )
        locus_color = (
            "RGB" if self.USER_LOCUS_COLOR_RGB.get() else self.USER_LOCUS_COLOR.get()
        )
        with matplotlib.style.context(self.USER_STYLE.get()):
            (
                figure,
                axes,
            ) = plot_RGB_chromaticities_function(
                image,
                colourspace=colour_colorspace,
                colourspaces=list(figure_colorspaces.keys()),
                scatter_kwargs={
                    "s": self.USER_SCATTER_SIZE.get(),
                    "c": marker_color,
                    "alpha": self.USER_SCATTER_ALPHA.get(),
                    "marker": self.USER_MARKER_STYLE.get().as_core(),
                    "zorder": 0,
                },
                # styling
                show_spectral_locus=self.USER_LOCUS_SHOW.get(),
                spectral_locus_colours=locus_color,
                spectral_locus_opacity=self.USER_LOCUS_ALPHA.get(),
                show_diagram_colours=self.USER_LOCUS_BACKGROUND_RGB.get(),
                show_whitepoints=self.USER_SHOW_WHITEPOINT.get(),
                show_pointer_gamut=self.USER_PLOT_POINTER_GAMUT.get(),
                pointer_gamut_colours=self.USER_POINTER_GAMUT_COLOR.get(),
                pointer_gamut_opacity=self.USER_POINTER_GAMUT_ALPHA.get(),
                transparent_background=False,
                standalone=False,
                legend=self.USER_SHOW_LEGEND.get(),
                axes_visible=self.USER_SHOW_AXES.get(),
                **plot_settings,
            )

            bounds_x_min, bounds_x_max = axes.get_xlim()
            bounds_y_min, bounds_y_max = axes.get_ylim()

            bounds_x_min, bounds_x_max, bounds_y_min, bounds_y_max = transform_box(
                bounds_x_min,
                bounds_x_max,
                bounds_y_min,
                bounds_y_max,
                scale=self.USER_AXES_SCALE.get(),
                offset_x=self.USER_AXES_OFFSET_X.get(),
                offset_y=self.USER_AXES_OFFSET_Y.get(),
            )

            axes.set_xlim(bounds_x_min, bounds_x_max)
            axes.set_ylim(bounds_y_min, bounds_y_max)

            if self.USER_SHOW_GRID.get():
                # NOTE: doesn't work anyway cause colour use negative zorder
                axes.set_axisbelow(True)
                axes.grid(
                    visible=self.USER_SHOW_GRID.get(),
                    alpha=self.USER_GRID_ALPHA.get(),
                    color=self.USER_GRID_COLOR.get(),
                )

        return figure, axes

    def post_clean(self):
        """
        Optimize the user config. To use after it has been used as intended.
        """
        # we clear the image array as we don't need it anymore,
        # this make sure it doesn't stay in memory
        self.USER_IMAGE.set(None)


def config(force_instance: bool = False) -> UserConfig:
    """
    Return a user configuration instance.

    Args:
        force_instance: True to force the recreation of a config instance.
    """
    if "USER_CONFIG" not in streamlit.session_state or force_instance:
        streamlit.session_state["USER_CONFIG"] = UserConfig()
    return streamlit.session_state["USER_CONFIG"]
