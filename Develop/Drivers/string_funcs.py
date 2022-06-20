##################################################
# Program: string_funcs
##################################################

##################################################
# System Module Imports
##################################################
from enum import Enum
import re
##################################################
# Add-In Module Imports
##################################################

##################################################
# Local Module Imports
##################################################

##################################################
# Constant Variable Definitions
##################################################

##################################################
# Global Variable Definitions
##################################################


class TRIM_DIRECTION(Enum):
    LEFT = 0
    RIGHT = 1


def clear_spaces(stream: str, white_space: bool = True, double_spaces: bool = True, tabs: bool = True, new_line: bool = True):
    if white_space is True:
        stream = stream.replace(' ', '')
    if tabs is True:
        stream = stream.replace('\t', '')
    if new_line is True:
        stream = stream.replace('\n', '')
    return stream.strip()


# General function to clear white spaces, tabs, etc, with an overload function to add keywords
def complex_clear(stream: str, *keywords, white_space: bool = False, tabs: bool = False, new_line: bool = False):
    if white_space is True:
        stream = stream.replace(' ', '')
    if tabs is True:
        stream = stream.replace('\t', '')
    if new_line is True:
        stream = stream.replace('\n', '')
    for keyword in keywords:
        if type(keyword) != str:
            continue
        stream = stream.replace(keyword, '')
    return stream.strip()


def find_variable_ending(stream: str, begin: str, *ending, trim_start: bool = False, trim_end: bool = False):
    # create local variables
    _begin, _end, _end_var_len = 0, 0, 0

    # search for begin trigger
    _begin = stream.find(begin)
    # if no trigger is found, return None
    if _begin == -1:
        return None

    # search for end trigger by looping through overloaded arguments
    for end in ending:
        _end = stream.find(end)
        if _end != -1:
            # if the trigger was found capture the length for later parsing
            _end_var_len = len(end)
            break
    # if no trigger is found, return None
    if _end == -1:
        return None

    # apply trimming
    if trim_start is True:
        _begin += len(begin)
    if trim_end is False:
        _end += _end_var_len

    # set string variables based on all above parameters gathered
    string = stream[_begin:_end] if _begin < _end else None
    return string


def get_list_from_stream(begin: str, end: str, stream: str, trim_start: bool = False, trim_end: bool = False):
    local_stream: str = stream
    data: list = []
    try:
        while True:
            match = re.search(begin, local_stream)
            if not match:
                break
            beginning = match.start() if trim_start is False else match.end()
            parsed_string = local_stream[beginning:]
            match = re.search(end, parsed_string)
            if not match:
                break
            ending = (match.end() + beginning) if trim_end is False else (match.start() + beginning)
            data.append(local_stream[beginning:ending])
            trim_end = 0 if trim_end is False else len(end)
            local_stream = local_stream[ending+trim_end:]
    except re.error:
        return None
    return data


def get_string_from_stream(begin: str, end: str, stream: str, trim_start: bool = False, trim_end: bool = False):
    _begin, _end = 0, 0
    _begin = stream.find(begin) if trim_start is False else stream.find(begin) + len(begin)
    if _begin == -1:
        return None
    _end = stream.find(end, _begin) if trim_end is True else stream.find(end, _begin) + len(end)
    if _end == -1:
        return None
    return stream[_begin:_end]


def trim_split(trigger: str, stream: str, trim_trigger=False, trim_direction: TRIM_DIRECTION = TRIM_DIRECTION.LEFT):
    try:
        match = re.search(trigger, stream)
        if not match:
            return None
        switcher = {
            TRIM_DIRECTION.LEFT: stream[:match.end()] if trim_trigger is False else stream[:match.start()],
            TRIM_DIRECTION.RIGHT: stream[match.start():] if trim_trigger is False else stream[match.end():]
        }
        return switcher.get(trim_direction)
    except re.error:
        return None


def find_coords(begin: str, end: str, stream: str):
    # create local variables
    _begin, _end, _coords = 0, 0, [-1, -1]

    # search for begin trigger
    _begin = stream.find(begin)
    # if no trigger is found, return None
    if _begin == -1:
        return _coords

    # search for end trigger
    _end = stream.find(end, _begin)
    if _end == -1:
        return _coords
    _coords = [_begin, _end+len(end)]
    return _coords
