import logging
import os

# must be executed before cv2 first import
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
# to enable locally but to disable on streamlit cloud
# os.environ["STCP_DISABLE_SIZE_LIMITATIONS"] = "1"

import colour.utilities
import psutil
import streamlit
import streamlit_colourplotting


APP_LOG_LEVEL_KEY = "APP_LOG_LEVEL"


def _configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="{levelname: <7} | {asctime} [{name: >30}]{message}",
        style="{",
    )

    if APP_LOG_LEVEL_KEY not in streamlit.session_state:
        APP_LOG_LEVEL = os.getenv("STCP_APP_LOG_LEVEL", "INFO").upper()
        streamlit.session_state[APP_LOG_LEVEL_KEY] = APP_LOG_LEVEL

    ROOT_LOGGER = logging.getLogger(streamlit_colourplotting.__name__)
    ROOT_LOGGER.setLevel(streamlit.session_state[APP_LOG_LEVEL_KEY])


_configure_logging()

LOGGER = logging.getLogger("streamlit_colourplotting.app")

streamlit.set_page_config(
    page_title="Colour-science Plotting",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Report a bug": "https://github.com/MrLixm/streamlit-colour-plotting/issues",
    },
)

colour.utilities.filter_warnings(colour_usage_warnings=True, python_warnings=True)
# we create a first instance of the config at startup
streamlit_colourplotting.ui.config(force_instance=True)
streamlit_colourplotting.create_main_ui()

LOGGER.debug(
    f"Final app RAM={psutil.Process(os.getpid()).memory_info().rss / 1024**2}MB"
)


@streamlit_colourplotting.widgetify
def widget_log_level(key):
    log_level = streamlit.session_state[key]
    streamlit.session_state[APP_LOG_LEVEL_KEY] = log_level


with streamlit.sidebar:
    with streamlit.expander(" "):
        streamlit.caption("Please do not modify options here :)")
        _options = ["DEBUG", "INFO", "WARNING", "ERROR"]
        streamlit.selectbox(
            label="log level",
            help="Only useful for the developer of the application.",
            index=_options.index(streamlit.session_state[APP_LOG_LEVEL_KEY]),
            options=_options,
            key=str(widget_log_level),
            on_change=widget_log_level,
        )
