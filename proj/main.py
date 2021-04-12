import curses


stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
stdscr.keypad(True)

curses.start_color()

SIMPLE = 1
ACTIVE = 2

curses.init_pair(SIMPLE, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(ACTIVE, curses.COLOR_BLACK, curses.COLOR_WHITE)

def draw():
	stdscr.addstr(0, 0, "Hello World!", curses.color_pair(SIMPLE))


while(True):
	stdscr.clear()
	draw()
	stdscr.refresh()
	stdscr.getkey()


curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
