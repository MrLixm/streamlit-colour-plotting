import streamlit

from streamlit_colourplotting.ui import config
from streamlit_colourplotting import widgetify
from ._sidebar import create_sidebar
from ._colorpicker import create_color_picker


def create_body_source():
    streamlit.header("Source")
    if config().USER_SOURCE_TYPE == config().USER_SOURCE_TYPE.color:
        create_color_picker()


def create_main_ui():
    streamlit.title("Colour plotter".upper())

    with streamlit.sidebar:
        create_sidebar()

    create_body_source()
