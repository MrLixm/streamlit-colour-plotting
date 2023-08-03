import os

# must be executed before cv2 first import
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"

import colour.utilities
import streamlit
import streamlit_colourplotting

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
streamlit_colourplotting.create_main_ui()
