import copy
import curses
import random
from collections import namedtuple
from dataclasses import dataclass
from typing import List

import pyfiglet

vector = namedtuple('Vector', 'x y')


@dataclass
class IndexData:
    position_in_line: int = 0
    color: int = 1
    ascii_representation: str = ' '


background: List[List[IndexData]] = []
# line
updating_info: List[IndexData] = []


def cyber_rain(window):
    display_text = get_display_text()
    curses.curs_set(curses.A_INVIS)
    init_colors()
    init_background()
    while True:
        curses.update_lines_cols()
        update_background()
        window.clear()
        draw_background(window)
        draw_text(display_text, window)
        window.refresh()


def init_data() -> IndexData:
    if random.randint(0, 15) != 1:
        return IndexData()
    line_length = random.randint(5, 15)
    return IndexData(
        position_in_line=line_length,
        color=curses.color_pair(random.randint(1, 5)),  # add random
        ascii_representation=str(random.randint(0, 1))
    )


def init_display_info():
    for _ in range(curses.COLS - 1):
        updating_info.append(init_data())


def init_background():
    init_display_info()
    global background
    background = [[] for _ in range(curses.LINES - 1)]
    for line_index in range(curses.LINES - 1):
        for data_index, data in enumerate(updating_info):
            background[line_index].append(copy.deepcopy(data))
            if data.position_in_line != 0:
                updating_info[data_index].position_in_line -= 1
            else:
                updating_info[data_index] = init_data()


def init_colors():
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)


def draw_text(display_text, window):
    text_location = get_text_location(display_text)
    for letter_line_index, display_text in enumerate(display_text):
        if len(display_text) > 0:
            for character_index, character in enumerate(display_text):
                if character != ' ':
                    window.addstr(text_location.y + letter_line_index,
                                  text_location.x + character_index,
                                  ' ')


def get_text_location(display_text):
    terminal_dimensions = vector(curses.COLS - 1, curses.LINES - 1)
    text_location = vector(int((terminal_dimensions.x - len(max(display_text))) / 2),
                           int((terminal_dimensions.y - len(display_text)) / 2))
    return text_location


def get_display_text():
    """
    This will turn a string into a list containing an ascii character representation
    Each element in the list is a line containing the ascii characters
    :return str as ascii text:
    """
    return pyfiglet.figlet_format(list('Cyber'), font='banner3').split('\n')


def update_display_info():
    global updating_info

    # update size
    if len(updating_info) <= curses.COLS:
        updating_info = updating_info[:curses.COLS - 1]
    else:
        while len(updating_info) > curses.COLS - 1:
            updating_info.append(init_data())

    for index, data in enumerate(updating_info):
        if data.position_in_line == 0:
            updating_info[index] = init_data()
        else:
            updating_info[index].position_in_line -= 1


def update_background():
    update_display_info()
    # remove top line and add new one
    background.pop(0)
    new_line = [copy.deepcopy(data) for data in updating_info]
    background.append(new_line)


def draw_background(window):
    for line_index, line in enumerate(reversed(background)):
        for column_index, position_data in enumerate(line):
            window.addstr(line_index, column_index, position_data.ascii_representation, position_data.color)


def main():
    curses.wrapper(cyber_rain)


if __name__ == '__main__':
    main()
