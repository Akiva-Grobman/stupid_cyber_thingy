import curses
import random
from collections import namedtuple
import pyfiglet


vector = namedtuple('Vector', 'x y')
counter = 0
display_background = []


def cyber_rain(window):
    display_text = get_display_text()
    curses.curs_set(curses.A_INVIS)
    init_background()
    while True:
        global prints
        prints += 1
        update_background(window)
        draw_text(display_text, window)
        window.refresh()
        # you might want to use sleep to slow down the refresh rate
        # time.sleep(0.002)


def init_background():
    global display_background
    display_background.clear()
    for _ in range((curses.LINES - 1) * 2):
        random_line = ''.join(
            [' ' * random.randint(0, 2)
             + str(random.randint(0, 1))
             + ' ' * random.randint(0, 3)
             for _ in range(curses.COLS - 1)]
        )[:curses.COLS - 1]
        display_background.append(random_line)


def update_background(window):
    window.clear()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    background_color = curses.color_pair(1)
    global counter
    counter += 1
    background = ''
    if counter >= curses.LINES - 1:
        counter = 0
        init_background()
    for index in range(counter, counter + curses.LINES - 1):
        background = f'{background}\n{display_background[index]}'
    window.addstr(0, 0, background, background_color)


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


def main():
    curses.wrapper(cyber_rain)


if __name__ == '__main__':
    main()
