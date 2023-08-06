import io

import matplotlib.pyplot
import streamlit

from streamlit_colourplotting.ui import config
from streamlit_colourplotting import widgetify
from ._sidebar import create_sidebar
from ._colorpicker import create_color_picker
from ._imagepicker import create_image_picker


def create_issue_warning():
    """
    Create a widget to display warnings the user might have generated.
    """
    issues = config().USER_SOURCE_ERROR.get()
    message = ""

    if issues == issues.unset:
        return

    if issues & issues.value_error:
        message += "- Invalid color value submitted, reverting to previous.\n"

    if issues & issues.hex_colorspace:
        message += "- hexadecimal colors can only be sRGB, reverting.\n"

    if issues & issues.hex_force_linear:
        message += "- hexadecimal colors cannot be linear, reverting.\n"

    streamlit.warning(message)

    # clear all error so the message is not displayed on next refresh
    config().USER_SOURCE_ERROR.set(issues.unset)


def create_body_source():
    streamlit.header("Color Source")

    create_issue_warning()

    if config().USER_SOURCE_TYPE.get() == config().USER_SOURCE_TYPE.get().color:
        create_color_picker()
    elif config().USER_SOURCE_TYPE.get() == config().USER_SOURCE_TYPE.get().image:
        create_image_picker()

    streamlit.header("Plot Result")

    # make sure the graph is created at the end
    with streamlit.spinner("Generating plot ..."):
        figure, axes = config().generate_plot()

    # execute before calling matplotlib.pyplot.show()
    plot_file = io.BytesIO()
    matplotlib.pyplot.savefig(plot_file, format="svg")

    # this call matplotlib.pyplot.show()
    streamlit.pyplot(figure, clear_figure=True)

    config().post_clean()

    streamlit.download_button(
        label="Download as SVG", data=plot_file, file_name="plot.svg"
    )

    plot_file.flush()
    plot_file.close()


def create_main_ui():
    # HACK to have columns child vertically aligned on the center
    # HACK to have image caption above and not under
    streamlit.markdown(
        """<style>
        div[data-testid="stHorizontalBlock"]{align-items:center;}
        div[data-testid="stImage"]{flex-direction:column-reverse;}
        div[data-testid="stImage"] div[data-testid="caption"] {margin-top:unset;}
        </style>""",
        unsafe_allow_html=True,
    )

    with streamlit.sidebar:
        create_sidebar()

    create_body_source()

    streamlit.divider()
    streamlit.caption(
        "![GitHub last commit (branch)](https://img.shields.io/github/last-commit/MrLixm/streamlit-colour-plotting/main?label=last%20updated) "
        f"![GitHub last tag](https://img.shields.io/github/v/tag/MrLixm/streamlit-colour-plotting?filter=v*&label=version) "
        f"[![GitHub Repo stars](https://img.shields.io/github/stars/MrLixm/streamlit-colour-plotting?logo=github)](https://github.com/MrLixm/streamlit-colour-plotting)"
    )
