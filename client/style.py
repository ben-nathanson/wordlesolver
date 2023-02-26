from enum import Enum


class AnsiEscapeSequence(str, Enum):
    GREEN_TEXT = "\u001b[32m"
    BLACK_TEXT = "\u001b[30m"
    RESET = "\033[0m"
    WHITE_TEXT = "\033[37m"
    YELLOW_TEXT = "\u001b[33m"


QWERTY_LAYOUT = [
    ['q','w','e','r','t','y','u','i','o','p'],
    ['a','s','d','f','g','h','j','k','l'],
    ['z','x','c','v','b','n','m',]
]