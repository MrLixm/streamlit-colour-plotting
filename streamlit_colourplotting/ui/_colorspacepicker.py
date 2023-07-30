import numpy
import streamlit

from cocoon import get_colorspace
from cocoon import get_available_colorspaces
from cocoon import sRGB_COLORSPACE

from streamlit_colourplotting.ui import config
from streamlit_colourplotting import widgetify


@widgetify
def widget_colorspace(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_SOURCE_COLORSPACE.get().name
        return

    user_value = streamlit.session_state[key]
    colorspace = get_colorspace(user_value)
    color_format = config().USER_SOURCE_COLOR_FORMAT.get()

    if color_format == color_format.hex and colorspace != sRGB_COLORSPACE:
        user_issues = config().USER_SOURCE_ERROR.get()
        config().USER_SOURCE_ERROR.set(user_issues | user_issues.hex_colorspace)
        # reset to previously stored
        streamlit.session_state[key] = config().USER_SOURCE_COLORSPACE.get().name
        return

    config().USER_SOURCE_COLORSPACE.set(colorspace)


@widgetify
def widget_force_linear(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_SOURCE_FORCE_LINEAR.get()
        return

    force_linear = streamlit.session_state[key]
    color_format = config().USER_SOURCE_COLOR_FORMAT.get()

    if color_format == color_format.hex and force_linear:
        user_issues = config().USER_SOURCE_ERROR.get()
        config().USER_SOURCE_ERROR.set(user_issues | user_issues.hex_force_linear)
        # reset to previously stored
        streamlit.session_state[key] = config().USER_SOURCE_FORCE_LINEAR.get()
        return

    config().USER_SOURCE_FORCE_LINEAR.set(force_linear)


def create_colorspace_picker():
    """
    Generate widgets that allow to select a colorspace configuration.
    """
    with streamlit.container():
        column1, column2 = streamlit.columns([0.75, 0.25])

        with column1:
            widget_colorspace(force_update=True)
            options = [colorspace.name for colorspace in get_available_colorspaces()]
            streamlit.selectbox(
                label="Colorspace",
                options=options,
                help="Colorspace include primaries, whitepoint and transfer-functions.",
                key=str(widget_colorspace),
                on_change=widget_colorspace,
            )

        with column2:
            streamlit.text("")
            streamlit.text("")
            widget_force_linear(force_update=True)
            streamlit.checkbox(
                label="Force Linear",
                key=str(widget_force_linear),
                on_change=widget_force_linear,
                help="For the colorspace to be set with linear transfer-functions.",
            )
