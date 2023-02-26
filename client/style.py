from enum import Enum


class AnsiEscapeSequence(str, Enum):
    GREEN_TEXT = "\u001b[32;1m"
    BLACK_TEXT = "\u001b[30m"
    RESET = "\u001b[0m"
    WHITE_TEXT = "\u001b[37m"
    BRIGHT_WHITE_TEXT = "\u001b[37;1m"
    YELLOW_TEXT = "\u001b[33;1m"
    RED_TEXT = "\u001b[31m"


QWERTY_LAYOUT = [
    ['q','w','e','r','t','y','u','i','o','p'],
    ['a','s','d','f','g','h','j','k','l'],
    ['z','x','c','v','b','n','m',]
]