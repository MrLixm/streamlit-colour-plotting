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
        streamlit.session_state[key] = config().USER_MARKER_STYLE.value
        return

    config().USER_MARKER_STYLE = MarkerShapeStyle(streamlit.session_state[key])


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
        label="Show Diagram Background",
        key=str(widget_show_diagram_background),
        on_change=widget_show_diagram_background,
    )

    widget_rgb_locus(force_update=True)
    streamlit.checkbox(
        label="Use RGB Spectral Locus",
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

    widget_scatter_size(force_update=True)
    streamlit.slider(
        label="Marker Size",
        min_value=0.0,
        max_value=100.0,
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
