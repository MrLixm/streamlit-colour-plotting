import streamlit

from ._sidebar import create_sidebar


def create_main_ui():
    streamlit.title("Colour plotter".upper())

    with streamlit.sidebar:
        create_sidebar()
