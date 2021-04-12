import curses
import random

MAP_POS_X = 10
MAP_POS_Y = 10

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

	rand_sum = 0
	for i in map_symbols:
		rand_sum += map_symbols[i][1]

	for i in range(0, sz_x):
		map.append(str())
		for j in range(0, sz_y):
			x = random.randint(1, rand_sum)
			for k in map_symbols:
				i -= map_symbols[k][1]
				if i <= 0:
					map[i] += map_symbols[k][0]
					break


def game_step(map):
	pass


def draw(stdscr, map):
	stdscr.addstr(0, 0, "Hello World!", curses.color_pair(SIMPLE_COLOR))
	for i in map:
		stdscr.addstr(i + MAP_POS_Y, MAP_POS_X, map[i], curses.color_pair(SIMPLE_COLOR))


def input(stdscr):
	stdscr.getkey()


def main():
	map_symbols = [{'#', 10}, {'$', 1}, {'&', 2}, {'*', 1}]

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