import curses
import random
import time
import copy

MAP_POS_X = 10
MAP_POS_Y = 1

PLAYER = 'P'
EMPTY = ' '
DOOR = '?'
MARK = '!'
WALL = '#'

SIMPLE_COLOR = 1
ACTIVE_COLOR = 2
WALL_COLOR = 3
GOLD_COLOR = 4
WEAPON_COLOR = 5
HIGHLIGHTED_COLOR = 6
PLAYER_COLOR = 7
DOOR_COLOR = 8


def begin_curses():
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)
	stdscr.keypad(True)
	stdscr.nodelay(True)

	curses.start_color()

	curses.init_pair(SIMPLE_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(ACTIVE_COLOR, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(WALL_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(GOLD_COLOR, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(WEAPON_COLOR, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(HIGHLIGHTED_COLOR, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(PLAYER_COLOR, curses.COLOR_BLUE, curses.COLOR_WHITE)
	curses.init_pair(DOOR_COLOR, curses.COLOR_GREEN, curses.COLOR_BLACK)

	return stdscr


def end_curses(stdscr):
	stdscr.nodelay(False)
	stdscr.keypad(False)
	curses.curs_set(1)
	curses.nocbreak()
	curses.echo()
	curses.endwin()


#!! add cellular automata !!
def generate_map(map, sz_x, sz_y, map_symbols):
	rand_sum = 0
	for symbol in map_symbols:
		rand_sum += symbol[1]

	for i in range(0, sz_x):
		map.append([])
		for j in range(0, sz_y):
			if i == 0 or j == 0 or i == \
			   sz_x - 1 or j == sz_y - 1:
			   	map[i].append((WALL, WALL_COLOR))
				continue
			x = random.randint(1, rand_sum)
			for symbol in map_symbols:
				x -= symbol[1]
				if x <= 0:
					map[i].append(symbol[0])
					break


def map_mark_dfs(map, i, j):
	positions = [(i, j)]
	directions = [
		[1, 0],
		[-1, 0],
		[0, 1],
		[0, -1]
	]
	map[i][j] = (MARK, SIMPLE_COLOR)
	for d in directions:
		if len(map) > d[0] + i and d[0] + i >= 0 and \
		   len(map[i + d[0]]) > d[1] + j and d[1] + j > 0:
		   positions += map_mark_dfs(map, i + d[0], j + d[1])

	return positions


def generate_doors(map):
	doors = []
	tmp_map = copy.deepcopy(map)
	for i in range(len(tmp_map)):
		for j in range(len(tmp_map[i])):
			if tmp_map[i][j][0] == EMPTY:
				map_mark_dfs(tmp_map, i, j)
				map[i][j] = (DOOR, DOOR_COLOR)
				doors.append((i, j))


def random_direction():
	k = random.randint(0, 3)
	return (((k % 2) * 2 - 1) * (k // 2),
		   ((k % 2) * 2 - 1) * (1 - k // 2))


def generate_monsters(map, rand_range, rand_monster):
	monsters = []
	for i in range(len(map)):
		for j in range(len(map[i])):
			if (map[i][j][0] == EMPTY):
				if random.randint(1, rand_range) <= rand_monster:
					
					monsters.append(((i, j), random_direction()))
					# position, move direction

	return monsters


def move_monsters(map, monsters):
	for i in range(len(monsters)):
		pos = monsters[i][0] + monsters[i][1]
		if map[pos[0]][pos[1]] == EMPTY:
		elif map[pos[0]][pos[1]] == PLAYER:
	pass


def game_step(map, monsters, player_pos):
	if player_pos == 
	move_monsters(map, monsters)
	pass


def draw(stdscr, map, monsters, player_pos):
	#stdscr.addstr(MAP_POS_Y - 1, 0, "Items:",
	#	curses.color_pair(HIGHLIGHTED_COLOR))

	for i in range(len(map)):
		stdscr.addstr(MAP_POS_Y - 1, i + MAP_POS_X,
			'-', curses.color_pair(SIMPLE_COLOR))
		stdscr.addstr(len(map[0]) + MAP_POS_Y, i + MAP_POS_X,
			'-', curses.color_pair(SIMPLE_COLOR))

	for i in range(len(map[0])): # ?? better ??
		stdscr.addstr(i + MAP_POS_Y, MAP_POS_X - 1,
			'|', curses.color_pair(SIMPLE_COLOR))
		stdscr.addstr(i + MAP_POS_Y, len(map) + MAP_POS_X,
			'|', curses.color_pair(SIMPLE_COLOR))

	for i in range(len(map)):
		for j in range(len(map[i])):
			stdscr.addstr(j + MAP_POS_Y, i + MAP_POS_X,
						  map[i][j][0], curses.color_pair(map[i][j][1]))

	for m in monsters:
		stdscr.addstr(m[0][1] + MAP_POS_Y, m[0][0] + MAP_POS_X,
			MONSTER, MONSTER_COLOR)

	stdscr.addstr(MAP_POS_Y + player_pos[1],
		MAP_POS_X + player_pos[0], PLAYER,
		curses.color_pair(PLAYER_COLOR))


def input(stdscr): # not work
	"""
	m = (0, 0)
	try:
		key = stdscr.getkey()
		if key == 'w':
			m[1] -= 1
		elif key == 's':
			m[1] += 1
		elif key == 'a':
			m[0] -= 1
		elif key == 'd':
			m[0] += 1
	except:
		pass
		# no input
	return m
	"""
	pass


def main():
	map_symbols = [
		((' ', SIMPLE_COLOR), 30),
		(('#', WALL_COLOR), 10),
		(('$', GOLD_COLOR), 1),
		(('&', WEAPON_COLOR), 2),
		(('*', WEAPON_COLOR), 1)
	]

	stdscr = begin_curses()

	map_size = (curses.COLS // 2, curses.LINES // 2)

	player_pos = (0, 0)

	map = []

	generate_map(map, map_size[0], map_size[1], map_symbols)

	doors = generate_doors(map)

	monsters = generate_monsters(map, 100, 7)

	main_loop_exception = False

	try:
		while(True):
			stdscr.clear()
			game_step(map, monsters, player_pos)
			draw(stdscr, map, monsters, player_pos)
			stdscr.refresh()
			player_pos += input(stdscr)
			time.sleep(0.1)

	except:
		main_loop_exception = True

	end_curses(stdscr)

	if main_loop_exception:
		print("Error during main loop");


main()