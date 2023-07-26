import colour.utilities
import streamlit
import streamlit_colourplotting

streamlit.set_page_config(
    page_title="Colour-science Plotting",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded",
)

colour.utilities.filter_warnings(colour_usage_warnings=True, python_warnings=True)
streamlit_colourplotting.create_main_ui()
