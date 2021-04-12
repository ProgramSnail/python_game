import curses
import random


SIMPLE_COLOR = 1
ACTIVE_COLOR = 2


def begin_curses():
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)
	stdscr.keypad(True)

	curses.start_color()

	curses.init_pair(SIMPLE_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(ACTIVE_COLOR, curses.COLOR_BLACK, curses.COLOR_WHITE)

	return stdscr


def end_curses(stdscr):
	curses.nocbreak()
	stdscr.keypad(False)
	curses.echo()
	curses.endwin()


def generate_map(map, seed, sz_x, sz_y, map_symbols):
	random.seed(seed)
	for i in range(0, sz_x):
		map.append(str())
		for j in range(0, sz_y):
			x = random.randint(0, len(map_symbols) - 1)
			map[i] += map_symbols[x]


def game_step(map):
	pass


def draw(stdscr, map):
	stdscr.addstr(0, 0, "Hello World!", curses.color_pair(SIMPLE_COLOR))


def input(stdscr):
	stdscr.getkey()


def main():
	map_symbols = [' ', '#', '$', '&', '*']

	stdscr = begin_curses()

	map = []

	generate_map(map, 2434343, 100, 100, map_symbols)

	while(True):
		stdscr.clear()
		game_step(map)
		draw(stdscr, map)
		stdscr.refresh()
		input(stdscr)

	end_curses(stdscr)

main()