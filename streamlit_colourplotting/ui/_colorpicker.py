import numpy
import streamlit

from cocoon import sRGB_COLORSPACE
from cocoon.color import convert_float_to_int8
from cocoon.color import ColorStringFormat
from cocoon.color import convert_color_to_str
from cocoon.color import convert_str_to_color
from cocoon.color import validate_color_str
from cocoon.color import fix_color_str

from streamlit_colourplotting.ui import config
from streamlit_colourplotting import widgetify


@widgetify
def widget_color_format(key):
    user_value = streamlit.session_state[key]
    value = ColorStringFormat(user_value)
    config().USER_SOURCE_COLOR_FORMAT = value
    widget_color_source(force_update=True)


@widgetify
def widget_color_source(key, force_update=False):
    config().USER_SOURCE_ERROR = ""

    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = convert_color_to_str(
            config().USER_SOURCE_COLOR,
            config().USER_SOURCE_COLOR_FORMAT,
        )
        return

    user_value = streamlit.session_state[key]

    validated = validate_color_str(user_value, config().USER_SOURCE_COLOR_FORMAT)
    if validated == validated.invalid:
        config().USER_SOURCE_ERROR = (
            "Invalid color value submitted, reseting to previous."
        )
        del streamlit.session_state[key]
        return

    safe_user_value = fix_color_str(user_value, config().USER_SOURCE_COLOR_FORMAT)
    streamlit.session_state[key] = safe_user_value
    color = convert_str_to_color(safe_user_value, config().USER_SOURCE_COLOR_FORMAT)
    config().USER_SOURCE_COLOR = color


def create_color_preview():
    """
    Generate a small thumbnail displaying the picked color
    """
    color = config().USER_SOURCE_COLOR
    color = color.as_colorspace(sRGB_COLORSPACE)
    image_array = color.to_array(alpha=False)
    image_array = convert_float_to_int8(image_array)
    image_array = numpy.full((32, 32, 3), image_array, dtype=numpy.uint8)
    streamlit.image(image_array, caption="sRGB preview")


def create_color_picker():
    """
    Generate widgets allowing to submit a RGB color value.
    """

    if config().USER_SOURCE_ERROR:
        streamlit.warning(config().USER_SOURCE_ERROR)

    column1, column2, column3 = streamlit.columns([0.15, 0.3, 0.55])

    with column1:
        create_color_preview()

    with column2:
        options = [item.value for item in ColorStringFormat]
        streamlit.selectbox(
            label="Color Format",
            options=options,
            index=options.index(config().USER_SOURCE_COLOR_FORMAT.value),
            help="Choose how is formatted your RGB color.\nA `.4` means 4 digit precision.",
            key=str(widget_color_format),
            on_change=widget_color_format,
        )
    with column3:
        # update the session state key, so we don't need to provide `value` param
        widget_color_source()
        color_text = streamlit.text_input(
            label="Color Value",
            # label_visibility="collapsed",
            help="Color expressed under the RGB model.",
            key=str(widget_color_source),
            on_change=widget_color_source,
        )
