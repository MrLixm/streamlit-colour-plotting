import enum

import streamlit


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

    @property
    def USER_SOURCE_TYPE(self) -> SourceType:
        return streamlit.session_state["USER_SOURCE_TYPE"]

    @USER_SOURCE_TYPE.setter
    def USER_SOURCE_TYPE(self, new_value: SourceType):
        streamlit.session_state["USER_SOURCE_TYPE"] = new_value


def config() -> UserConfig:
    """
    Return a user configuration instance.
    """
    return UserConfig()
