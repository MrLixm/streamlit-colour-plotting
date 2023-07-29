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
from ._colorspacepicker import create_colorspace_picker


@widgetify
def widget_color_format(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        # warning the default value should not be hexadecimal !
        streamlit.session_state[key] = config().USER_SOURCE_COLOR_FORMAT.value
        return

    user_value = streamlit.session_state[key]
    value = ColorStringFormat(user_value)

    config().USER_SOURCE_COLOR_FORMAT = value
    widget_color_source(force_update=True)

    # we assume hexadecimal color are always encoded as "display sRGB"
    if value == value.hex:
        config().USER_SOURCE_COLORSPACE = sRGB_COLORSPACE
        config().USER_SOURCE_FORCE_LINEAR = False


@widgetify
def widget_color_source(key, force_update=False):
    if key not in streamlit.session_state or force_update:
        streamlit.session_state[key] = convert_color_to_str(
            config().USER_SOURCE_COLOR,
            config().USER_SOURCE_COLOR_FORMAT,
        )
        return

    user_value = streamlit.session_state[key]
    validated = validate_color_str(user_value, config().USER_SOURCE_COLOR_FORMAT)

    if validated == validated.invalid:
        user_issues = config().USER_SOURCE_ERROR
        config().USER_SOURCE_ERROR = user_issues | user_issues.value_error
        del streamlit.session_state[key]
        return

    safe_user_value = fix_color_str(user_value, config().USER_SOURCE_COLOR_FORMAT)
    color = convert_str_to_color(safe_user_value, config().USER_SOURCE_COLOR_FORMAT)

    streamlit.session_state[key] = safe_user_value
    config().USER_SOURCE_COLOR = color


def create_color_preview():
    """
    Generate a small thumbnail displaying the picked color
    """
    color = config().color
    color = color.as_colorspace(sRGB_COLORSPACE)
    image_array = color.to_array(alpha=False)
    image_array = convert_float_to_int8(image_array)
    image_array = numpy.full((22, 32, 3), image_array, dtype=numpy.uint8)
    streamlit.image(image_array, caption="sRGB preview")


def create_color_picker():
    """
    Generate widgets allowing to submit a RGB color value.
    """

    create_colorspace_picker()

    column1, column2, column3 = streamlit.columns([0.15, 0.3, 0.55])

    with column1:
        create_color_preview()

    with column2:
        widget_color_format(force_update=True)
        options = [item.value for item in ColorStringFormat]
        streamlit.selectbox(
            label="Color Format",
            options=options,
            help="Choose how is formatted your RGB color.\nA `.4` means 4 digit precision.\nhexadecimal are always assume to be sRGB encoded",
            key=str(widget_color_format),
            on_change=widget_color_format,
        )
    with column3:
        widget_color_source(force_update=True)
        color_text = streamlit.text_input(
            label="Color Value",
            # label_visibility="collapsed",
            help="Color expressed under the RGB model.",
            key=str(widget_color_source),
            on_change=widget_color_source,
        )
