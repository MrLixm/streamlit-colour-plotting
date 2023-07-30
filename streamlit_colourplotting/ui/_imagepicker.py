import traceback

import streamlit

import streamlit_colourplotting.core
from streamlit_colourplotting.ui import config
from ._colorspacepicker import create_colorspace_picker


SUPPORTED_EXTENSION = [
    ".png",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
    ".webp",
    ".hdr",
    ".exr",
    ".ico",
    ".targa",
    ".dds",
    ".psd",
]


@streamlit.cache_data
def _get_image_from_bytes(bytesio):
    return streamlit_colourplotting.core.read_image_from_bytes(bytesio)


def create_image_picker():
    create_colorspace_picker()

    user_image = streamlit.file_uploader(
        label="Image Path",
        type=SUPPORTED_EXTENSION,
    )
    image_array = None

    if user_image is not None:
        try:
            image_array = _get_image_from_bytes(user_image)
        except Exception as error:
            error_tb = "\n- ".join(
                [
                    line.split(",", 1)[-1]
                    for line in traceback.format_tb(error.__traceback__)
                ]
            )
            streamlit.error(f"Can't read provided image: {error}\n\n- {error_tb}")
        else:
            streamlit.caption(
                f"Image loaded as <{image_array.dtype} array {image_array.shape}>"
            )

    config().USER_IMAGE.set(image_array)
