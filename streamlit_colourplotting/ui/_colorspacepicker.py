import numpy
import streamlit

from cocoon import get_colorspace
from cocoon import get_available_colorspaces
from cocoon import sRGB_COLORSPACE

from streamlit_colourplotting.ui import config
from streamlit_colourplotting import widgetify


@widgetify
def widget_colorspace(key):
    user_value = streamlit.session_state[key]
    colorspace = get_colorspace(user_value)
    config().USER_SOURCE_COLORSPACE = colorspace


@widgetify
def widget_force_linear(key):
    config().USER_SOURCE_FORCE_LINEAR = streamlit.session_state[key]


def create_colorspace_picker():
    with streamlit.container():
        column1, column2 = streamlit.columns([0.75, 0.25])

        with column1:
            options = [colorspace.name for colorspace in get_available_colorspaces()]
            streamlit.selectbox(
                label="Colorspace",
                options=options,
                index=options.index(config().USER_SOURCE_COLORSPACE.name),
                help="Colorspace include primaries, whitepoint and transfer-functions.",
                key=str(widget_colorspace),
                on_change=widget_colorspace,
            )

        with column2:
            streamlit.text("")
            streamlit.text("")
            streamlit.checkbox(
                label="Force Linear",
                value=config().USER_SOURCE_FORCE_LINEAR,
                key=str(widget_force_linear),
                on_change=widget_force_linear,
                help="For the colorspace to be set with linear transfer-functions.",
            )
