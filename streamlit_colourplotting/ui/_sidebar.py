import streamlit

from streamlit_colourplotting import widgetify
from streamlit_colourplotting.ui._config import SourceType
from streamlit_colourplotting.ui._config import DiagramMethod
from streamlit_colourplotting.ui._config import MarkerShapeStyle
from streamlit_colourplotting.ui import config


@widgetify
def widget_source_type(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_SOURCE_TYPE.value
        return

    config().USER_SOURCE_TYPE = SourceType(streamlit.session_state[key])


@widgetify
def widget_diagram_method(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_DIAGRAM_METHOD.value
        return

    config().USER_DIAGRAM_METHOD = DiagramMethod(streamlit.session_state[key])


@widgetify
def widget_show_diagram_background(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_DIAGRAM_SHOW_BACKGROUND
        return

    config().USER_DIAGRAM_SHOW_BACKGROUND = streamlit.session_state[key]


@widgetify
def widget_rgb_locus(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_RGB_LOCUS
        return

    config().USER_RGB_LOCUS = streamlit.session_state[key]


@widgetify
def widget_transparent_background(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_TRANSPARENT_BACKGROUND
        return

    config().USER_TRANSPARENT_BACKGROUND = streamlit.session_state[key]


@widgetify
def widget_scatter_size(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_SCATTER_SIZE
        return

    config().USER_SCATTER_SIZE = streamlit.session_state[key]


@widgetify
def widget_scatter_color_rgb(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_SCATTER_COLOR_RGB
        return

    config().USER_SCATTER_COLOR_RGB = streamlit.session_state[key]


@widgetify
def widget_scatter_color(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_SCATTER_COLOR
        return

    config().USER_SCATTER_COLOR = streamlit.session_state[key]


@widgetify
def widget_marker_style(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_MARKER_STYLE.as_label()
        return

    config().USER_MARKER_STYLE = MarkerShapeStyle.from_label(
        streamlit.session_state[key]
    )


@widgetify
def widget_plot_pointer_gamut(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_PLOT_POINTER_GAMUT
        return

    config().USER_PLOT_POINTER_GAMUT = streamlit.session_state[key]


@widgetify
def widget_pointer_gamut_alpha(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_POINTER_GAMUT_ALPHA
        return

    config().USER_POINTER_GAMUT_ALPHA = streamlit.session_state[key]


@widgetify
def widget_show_whitepoint(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_SHOW_WHITEPOINT
        return

    config().USER_SHOW_WHITEPOINT = streamlit.session_state[key]


@widgetify
def widget_image_samples(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_IMAGE_SAMPLES
        return

    config().USER_IMAGE_SAMPLES = streamlit.session_state[key]


@widgetify
def widget_figure_size(key, force_update=False):
    # NOTE: conversion of inch (pyplot) to centimeters (gui)
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_FIGURE_SIZE * 2.54
        return

    config().USER_FIGURE_SIZE = streamlit.session_state[key] / 2.54


@widgetify
def widget_figure_font_size(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_FIGURE_FONT_SIZE
        return

    config().USER_FIGURE_FONT_SIZE = streamlit.session_state[key]


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
        streamlit.markdown(label)

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


def create_sidebar():
    streamlit.title("Options".upper())

    widget_source_type(force_update=True)
    options = SourceType.labels()
    streamlit.selectbox(
        label="Source",
        options=options,
        help="Choose which data type you want to plot.",
        key=str(widget_source_type),
        on_change=widget_source_type,
    )

    widget_diagram_method(force_update=True)
    options = DiagramMethod.labels()
    streamlit.selectbox(
        label="Diagram Method",
        options=options,
        help="Choose which model to use for the chromaticity diagram.",
        key=str(widget_diagram_method),
        on_change=widget_diagram_method,
    )

    widget_show_diagram_background(force_update=True)
    streamlit.checkbox(
        label="Show RGB Locus Background",
        key=str(widget_show_diagram_background),
        on_change=widget_show_diagram_background,
    )

    widget_rgb_locus(force_update=True)
    streamlit.checkbox(
        label="Use RGB Locus Border",
        key=str(widget_rgb_locus),
        on_change=widget_rgb_locus,
    )

    widget_transparent_background(force_update=True)
    streamlit.checkbox(
        label="Use Transparent Background",
        key=str(widget_transparent_background),
        on_change=widget_transparent_background,
    )

    widget_show_whitepoint(force_update=True)
    streamlit.checkbox(
        label="Show Whitepoints",
        key=str(widget_show_whitepoint),
        on_change=widget_show_whitepoint,
    )

    widget_plot_pointer_gamut(force_update=True)
    show_pointer_gamut = streamlit.checkbox(
        label="Show Pointer's Gamut",
        key=str(widget_plot_pointer_gamut),
        on_change=widget_plot_pointer_gamut,
    )

    widget_pointer_gamut_alpha(force_update=True)
    if show_pointer_gamut:
        streamlit.slider(
            label="Pointer's Gamut Opacity",
            min_value=0.0,
            max_value=1.0,
            key=str(widget_pointer_gamut_alpha),
            on_change=widget_pointer_gamut_alpha,
        )

    with streamlit.expander("Markers Styling"):
        widget_scatter_size(force_update=True)
        streamlit.slider(
            label="Marker Size",
            min_value=0.0,
            max_value=200.0,
            key=str(widget_scatter_size),
            on_change=widget_scatter_size,
        )

        streamlit.markdown("###### Marker Color")

        column1, column2 = streamlit.columns([0.15, 0.85])

        with column2:
            widget_scatter_color_rgb(force_update=True)
            use_rgb = streamlit.checkbox(
                label="Use RGB",
                key=str(widget_scatter_color_rgb),
                on_change=widget_scatter_color_rgb,
                help="If checked, each scatter marker take the color it represent.",
            )

        with column1:
            widget_scatter_color(force_update=True)
            streamlit.color_picker(
                label="Marker Color",
                label_visibility="collapsed",
                disabled=use_rgb,
                key=str(widget_scatter_color),
                on_change=widget_scatter_color,
            )

        widget_marker_style(force_update=True)
        options = MarkerShapeStyle.labels()
        streamlit.selectbox(
            label="Marker Style",
            options=options,
            help="Style of the shape of the markers (scatter points).",
            key=str(widget_marker_style),
            on_change=widget_marker_style,
        )

    widget_figure_size(force_update=True)
    streamlit.slider(
        label="Figure Size",
        min_value=1.0,
        max_value=50.0,
        help="Size of the diagram in cm.",
        key=str(widget_figure_size),
        on_change=widget_figure_size,
    )

    widget_figure_font_size(force_update=True)
    streamlit.slider(
        label="Font Size",
        min_value=1.0,
        max_value=50.0,
        key=str(widget_figure_font_size),
        on_change=widget_figure_font_size,
    )

    widget_image_samples(force_update=True)
    streamlit.number_input(
        label="Image Samples",
        help="Only plot each pixel every N sample submitted.\n\n"
        "Higher number increase processing speed of larger images.",
        min_value=1,
        key=str(widget_image_samples),
        on_change=widget_image_samples,
    )

    with streamlit.expander("Theming"):
        color_background = create_style_edit_row("Background", "#1B1B1B00")
        config().USER_STYLE["figure.facecolor"] = color_background
        config().USER_STYLE["axes.facecolor"] = color_background
        config().USER_STYLE["text.color"] = create_style_edit_row("Text", "#fefefeff")
        color_axes = create_style_edit_row("Axes", "#666666ff")
        config().USER_STYLE["axes.labelcolor"] = color_axes
        config().USER_STYLE["xtick.color"] = color_axes
        config().USER_STYLE["ytick.color"] = color_axes
        config().USER_STYLE["axes.edgecolor"] = color_axes
        config().USER_STYLE["legend.facecolor"] = create_style_edit_row(
            "Legend", "#363636ff"
        )
        config().USER_STYLE["legend.edgecolor"] = create_style_edit_row(
            "Legend Border",
            "#36363600",
            show_alpha=False,
        )
