import streamlit

from streamlit_colourplotting import widgetify
from streamlit_colourplotting.ui._config import SourceType
from streamlit_colourplotting.ui._config import DiagramMethod
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
