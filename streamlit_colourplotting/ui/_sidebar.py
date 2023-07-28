import streamlit

from streamlit_colourplotting import widgetify
from streamlit_colourplotting.ui._config import SourceType
from streamlit_colourplotting.ui import config


@widgetify
def widget_source_type(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = config().USER_SOURCE_TYPE.value
        return

    config().USER_SOURCE_TYPE = SourceType(streamlit.session_state[key])


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
