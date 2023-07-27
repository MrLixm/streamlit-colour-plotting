import enum

import streamlit
from cocoon.color import RGBAColor
from cocoon.color import ColorStringFormat


class SourceType(enum.Enum):
    color = "Color"
    image = "Image"

    @classmethod
    def labels(cls) -> list[str]:
        return [item.value for item in cls]


class UserConfig:
    def __init__(self):
        if "USER_SOURCE_TYPE" not in streamlit.session_state:
            streamlit.session_state["USER_SOURCE_TYPE"] = SourceType.color
        if "USER_SOURCE_COLOR" not in streamlit.session_state:
            streamlit.session_state["USER_SOURCE_COLOR"] = RGBAColor(0.0, 0.0, 0.0)
        if "USER_SOURCE_COLOR_FORMAT" not in streamlit.session_state:
            k = "USER_SOURCE_COLOR_FORMAT"
            streamlit.session_state[k] = ColorStringFormat.float_d4
        if "USER_SOURCE_ERROR" not in streamlit.session_state:
            streamlit.session_state["USER_SOURCE_ERROR"] = ""

    @property
    def USER_SOURCE_TYPE(self) -> SourceType:
        return streamlit.session_state["USER_SOURCE_TYPE"]

    @USER_SOURCE_TYPE.setter
    def USER_SOURCE_TYPE(self, new_value: SourceType):
        streamlit.session_state["USER_SOURCE_TYPE"] = new_value

    @property
    def USER_SOURCE_COLOR(self) -> RGBAColor:
        return streamlit.session_state["USER_SOURCE_COLOR"]

    @USER_SOURCE_COLOR.setter
    def USER_SOURCE_COLOR(self, new_value: RGBAColor):
        streamlit.session_state["USER_SOURCE_COLOR"] = new_value

    @property
    def USER_SOURCE_COLOR_FORMAT(self) -> ColorStringFormat:
        return streamlit.session_state["USER_SOURCE_COLOR_FORMAT"]

    @USER_SOURCE_COLOR_FORMAT.setter
    def USER_SOURCE_COLOR_FORMAT(self, new_value: ColorStringFormat):
        streamlit.session_state["USER_SOURCE_COLOR_FORMAT"] = new_value


    @property
    def USER_SOURCE_ERROR(self) -> str:
        return streamlit.session_state["USER_SOURCE_ERROR"]

    @USER_SOURCE_ERROR.setter
    def USER_SOURCE_ERROR(self, new_value: str):
        streamlit.session_state["USER_SOURCE_ERROR"] = new_value


def config() -> UserConfig:
    """
    Return a user configuration instance.
    """
    return UserConfig()
