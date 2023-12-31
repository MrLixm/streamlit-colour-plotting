from typing import Optional

import streamlit
from cocoon import get_available_colorspaces

from streamlit_colourplotting.ui._config import SourceType
from streamlit_colourplotting.ui._config import DiagramMethod
from streamlit_colourplotting.ui._config import MarkerShapeStyle
from streamlit_colourplotting.ui import config


def create_colorspace_row(
    identifier: int,
    initial_color: str,
) -> tuple[Optional[str], str]:
    """
    Create widgets to select a colorspace to display in the diagram.

    Args:
        identifier: number starting from 1
        initial_color: default color used for the colorspace in the diagram

    Returns:
        colorspace instance to display , associated hexadecimal color
    """
    column1, column2, column3 = streamlit.columns([0.08, 0.80, 0.12])

    with column1:
        use_colorspace = streamlit.checkbox(
            label=f"Use Colorspace {identifier}",
            value=identifier == 1,
            label_visibility="collapsed",
            disabled=identifier == 1,
        )

    with column2:
        if identifier == 1:
            streamlit.markdown("Source Colorspace")
        else:
            options = [colorspace.name for colorspace in get_available_colorspaces()]
            colorspace_name = streamlit.selectbox(
                label=f"Colorspace {identifier}",
                options=options,
                label_visibility="collapsed",
            )

    with column3:
        color = streamlit.color_picker(
            label=f"{identifier} Color",
            label_visibility="collapsed",
            value=initial_color,
        )

    if identifier == 1:
        return config().SOURCE_COLORSPACE_TOKEN, color

    if use_colorspace:
        return colorspace_name, color
    return None, "#000000"


def create_style_edit_row(
    label: str,
    initial_value: str,
    show_alpha: bool = True,
) -> str:
    """
    Args:
        label: name of the style component edited
        initial_value: color to set firts time the ui is created, hexadecimal with alpha.
        show_alpha: make the alpha widget visible if True

    Returns:
        color picked by user as hexadecimal encoding, with alpha (as supported by matplotlib).
    """

    initial_color = initial_value[:7]
    initial_alpha = int(initial_value[7:], 16) / 255

    column1, column2, column3 = streamlit.columns([0.43, 0.12, 0.5])

    with column1:
        streamlit.markdown(f"###### {label}")

    with column2:
        color = streamlit.color_picker(
            label=f"{label} Color",
            label_visibility="collapsed",
            value=initial_color,
        )
    with column3:
        if show_alpha:
            alpha = streamlit.number_input(
                label=f"{label} Alpha",
                min_value=0.0,
                max_value=1.0,
                value=initial_alpha,
                label_visibility="collapsed",
            )
        else:
            alpha = 0.0

    alpha = f"{round(alpha * 255):02x}"
    return f"{color}{alpha}"


def create_color_alpha_row(
    label: str,
    default_color: str,
    default_alpha: float,
    disable_color: bool = False,
) -> tuple[str, float]:
    """
    Create a widget to edit a color and an alpha value.

    Args:
        label: to create unique widgets
        default_color: defautl value for color widget
        default_alpha: defautl value for alpha widget
        disable_color: True to dsiable the color picker widget

    Returns:
        tuple["hexadecimal color", "alpha 0-1 range"]
    """
    column1, column2, column3 = streamlit.columns([0.12, 0.45, 0.43])

    with column1:
        widget_color = streamlit.color_picker(
            label=f"{label} Color",
            label_visibility="collapsed",
            disabled=disable_color,
            value=default_color,
        )

    with column2:
        widget_alpha = streamlit.number_input(
            label=f"{label} Alpha",
            label_visibility="collapsed",
            min_value=0.0,
            max_value=1.0,
            value=default_alpha,
        )

    return widget_color, widget_alpha


def create_sidebar():
    streamlit.title("Options".upper())

    options = SourceType.labels()
    source_type = streamlit.selectbox(
        label="Source",
        options=options,
        help="Choose which data type you want to plot.",
        index=options.index(config().USER_SOURCE_TYPE.default.value),
    )
    config().USER_SOURCE_TYPE.set(SourceType(source_type))

    options = DiagramMethod.labels()
    diagram_method = streamlit.selectbox(
        label="Diagram Method",
        options=options,
        help="Choose which model to use for the chromaticity diagram.",
        index=options.index(config().USER_DIAGRAM_METHOD.default.value),
    )
    config().USER_DIAGRAM_METHOD.set(DiagramMethod(diagram_method))

    with streamlit.expander("Spectral Locus"):
        show_locus = streamlit.checkbox(
            label="Show Spectral Locus",
            value=config().USER_LOCUS_SHOW.default,
        )
        config().USER_LOCUS_SHOW.set(show_locus)

        show_locus_background = streamlit.checkbox(
            label="RGB Background",
            key="locusBackgroundRgb",
            value=config().USER_LOCUS_BACKGROUND_RGB.default,
        )
        config().USER_LOCUS_BACKGROUND_RGB.set(show_locus_background)

        use_rgb_locus = streamlit.checkbox(
            label="RGB Border",
            key="locusBorderRgb",
            value=config().USER_LOCUS_COLOR_RGB.default,
            disabled=not show_locus,
        )
        config().USER_LOCUS_COLOR_RGB.set(use_rgb_locus)

        locus_color, locus_alpha = create_color_alpha_row(
            label="Locus",
            default_color=config().USER_LOCUS_COLOR.default,
            default_alpha=config().USER_LOCUS_ALPHA.default,
            disable_color=use_rgb_locus,
        )
        config().USER_LOCUS_COLOR.set(locus_color)
        config().USER_LOCUS_ALPHA.set(locus_alpha)

    with streamlit.expander("Pointer's Gamut"):
        show_pointer_gamut = streamlit.checkbox(
            label="Show Pointer's Gamut",
            value=config().USER_PLOT_POINTER_GAMUT.default,
        )
        config().USER_PLOT_POINTER_GAMUT.set(show_pointer_gamut)

        pointer_color, pointer_alpha = create_color_alpha_row(
            label="Pointer's Gamut",
            default_color=config().USER_POINTER_GAMUT_COLOR.default,
            default_alpha=config().USER_POINTER_GAMUT_ALPHA.default,
        )
        config().USER_POINTER_GAMUT_COLOR.set(pointer_color)
        config().USER_POINTER_GAMUT_ALPHA.set(pointer_alpha)

    with streamlit.expander("Markers Styling"):
        marker_size = streamlit.slider(
            label="Marker Size",
            min_value=0.0,
            max_value=200.0,
            value=config().USER_SCATTER_SIZE.default,
        )
        config().USER_SCATTER_SIZE.set(marker_size)

        streamlit.markdown("###### Marker Color")

        column1, column2, column3 = streamlit.columns([0.43, 0.12, 0.45])

        with column1:
            marker_use_rgb = streamlit.checkbox(
                label="RGB",
                help="If checked, each scatter marker take the color it represent.",
                key="markerUseRgb",
                value=config().USER_SCATTER_COLOR_RGB.default,
            )
            config().USER_SCATTER_COLOR_RGB.set(marker_use_rgb)

        with column2:
            marker_color = streamlit.color_picker(
                label="Marker Color",
                label_visibility="collapsed",
                disabled=marker_use_rgb,
                value=config().USER_SCATTER_COLOR.default,
            )
            config().USER_SCATTER_COLOR.set(marker_color)

        with column3:
            marker_alpha = streamlit.number_input(
                label="Marker Alpha",
                label_visibility="collapsed",
                min_value=0.0,
                max_value=1.0,
                value=config().USER_SCATTER_ALPHA.default,
            )
            config().USER_SCATTER_ALPHA.set(marker_alpha)

        options = MarkerShapeStyle.labels()
        marker_style = streamlit.selectbox(
            label="Marker Style",
            options=options,
            help="Style of the shape of the markers (scatter points).",
            index=options.index(config().USER_MARKER_STYLE.default.as_label()),
        )
        config().USER_MARKER_STYLE.set(MarkerShapeStyle.from_label(marker_style))

    with streamlit.expander("Colorspaces"):
        show_whitepoints = streamlit.checkbox(
            label="Show Whitepoints",
            value=config().USER_SHOW_WHITEPOINT.default,
        )
        config().USER_SHOW_WHITEPOINT.set(show_whitepoints)

        colorspace1 = create_colorspace_row(1, "#F44336")
        colorspace2 = create_colorspace_row(2, "#9C27B0")
        colorspace3 = create_colorspace_row(3, "#3F51B5")
        colorspace4 = create_colorspace_row(4, "#03A9F4")
        colorspace5 = create_colorspace_row(5, "#009688")
        config().USER_FIGURE_COLORSPACES.set(
            [
                colorspace1,
                colorspace2,
                colorspace3,
                colorspace4,
                colorspace5,
            ]
        )

    with streamlit.expander("Theming"):
        show_legend = streamlit.checkbox(
            label="Show Legend",
            value=config().USER_SHOW_LEGEND.default,
        )
        config().USER_SHOW_LEGEND.set(show_legend)

        show_axes = streamlit.checkbox(
            label="Show Axes",
            value=config().USER_SHOW_AXES.default,
        )
        config().USER_SHOW_AXES.set(show_axes)

        style = config().USER_STYLE.get()

        figure_size = streamlit.slider(
            label="Figure Size",
            min_value=1.0,
            max_value=50.0,
            value=25.0,
            help="Size of the diagram in cm.",
        )
        # convert cm to inches for matplotlib
        style["figure.figsize"] = (figure_size / 2.54, figure_size / 2.54)

        font_size = streamlit.slider(
            label="Font Size",
            min_value=1.0,
            max_value=50.0,
            value=12.0,
        )
        style["font.size"] = font_size

        color_background = create_style_edit_row("Background", "#1B1B1B00")
        style["figure.facecolor"] = color_background
        color_background_axes = create_style_edit_row("Background Axes", "#1B1B1B00")
        style["axes.facecolor"] = color_background_axes
        style["text.color"] = create_style_edit_row("Text", "#fefefeff")
        color_axes = create_style_edit_row("Axes", "#666666ff")
        style["axes.labelcolor"] = color_axes
        style["xtick.color"] = color_axes
        style["ytick.color"] = color_axes
        style["axes.edgecolor"] = color_axes
        style["legend.facecolor"] = create_style_edit_row("Legend", "#363636ff")
        style["legend.edgecolor"] = create_style_edit_row(
            "Legend Border",
            "#36363600",
            show_alpha=False,
        )
        config().USER_STYLE.set(style)

    with streamlit.expander("Grid"):
        streamlit.caption(
            "Note that the grid can unfortunately only be drawn **above** everything."
        )

        show_grid = streamlit.checkbox(
            label="Show Grid",
            value=config().USER_SHOW_GRID.default,
        )
        config().USER_SHOW_GRID.set(show_grid)

        grid_color, grid_alpha = create_color_alpha_row(
            label="Grid",
            default_color=config().USER_GRID_COLOR.default,
            default_alpha=config().USER_GRID_ALPHA.default,
        )
        config().USER_GRID_COLOR.set(grid_color)
        config().USER_GRID_ALPHA.set(grid_alpha)

    with streamlit.expander("Graph Transform"):
        graph_scale = streamlit.number_input(
            label="Graph Scale",
            min_value=0.0,
            max_value=100.0,
            step=0.2,
            value=1 / config().USER_AXES_SCALE.default,
        )
        config().USER_AXES_SCALE.set(1 / graph_scale)

        column1, column2 = streamlit.columns(2)

        with column1:
            graph_offset_x = streamlit.number_input(
                label="Graph Offset X",
                min_value=-100.0,
                max_value=100.0,
                step=0.05,
                value=config().USER_AXES_OFFSET_X.default,
            )
            config().USER_AXES_OFFSET_X.set(graph_offset_x)

        with column2:
            graph_offset_y = streamlit.number_input(
                label="Graph Offset Y",
                min_value=-100.0,
                max_value=100.0,
                step=0.05,
                value=config().USER_AXES_OFFSET_Y.default,
            )
            config().USER_AXES_OFFSET_Y.set(graph_offset_y)

    image_samples = streamlit.number_input(
        label="Image Samples",
        help="Only plot each pixel every N sample submitted.\n\n"
        "Higher number increase processing speed of larger images.",
        min_value=10,
        value=config().USER_IMAGE_SAMPLES.default,
    )
    config().USER_IMAGE_SAMPLES.set(image_samples)
