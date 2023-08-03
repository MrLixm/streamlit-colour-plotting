import traceback

import numpy
import streamlit
import cocoon
import cocoon.color

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


def create_image_preview(image_array: numpy.ndarray, target_width):
    """
    Generate a small thumbnail displaying the submitted image
    """

    # we don't care about quality as it's a preview
    preview_array = streamlit_colourplotting.core.rescale_image_fast(
        image_array, target_width
    )

    source_colorspace = config()._source_colorspace
    preview_array = cocoon.colorspace_to_colorspace(
        preview_array,
        source_colorspace,
        cocoon.sRGB_COLORSPACE,
        cocoon.ChromaticAdaptationTransform.get_default(),
    )
    preview_array = cocoon.color.convert_float_to_int8(preview_array)
    streamlit.image(preview_array, caption=f"sRGB preview {image_array.shape}")


def create_image_picker():
    create_colorspace_picker()

    column1, column2 = streamlit.columns([0.3, 0.7])

    with column2:
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
            with column1:
                create_image_preview(image_array, 200)

                # streamlit.caption(f"<{image_array.dtype} {image_array.shape}>")

    config().USER_IMAGE.set(image_array)
