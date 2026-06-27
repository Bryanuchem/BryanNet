from enum import Enum


class NextAction(str, Enum):

    START_ONBOARDING = "START_ONBOARDING"

    ENTER_NAME = "ENTER_NAME"

    ENTER_PHONE = "ENTER_PHONE"

    SHOW_MAIN_MENU = "SHOW_MAIN_MENU"