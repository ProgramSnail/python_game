import curses
import random
import time
import copy

MAP_POS_X = 16
MAP_POS_Y = 2

PLAYER = 'P'
MONSTER = 'M'
EMPTY = ' '
DOOR = '>'
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
MONSTER_COLOR = 9
ADD_HEALTH_COLOR = 10


def begin_curses():
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)
	stdscr.keypad(True)
	#stdscr.nodelay(True)

	curses.start_color()

	curses.init_pair(SIMPLE_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(ACTIVE_COLOR, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(WALL_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(GOLD_COLOR, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(WEAPON_COLOR, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(HIGHLIGHTED_COLOR, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(PLAYER_COLOR, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(DOOR_COLOR, curses.COLOR_BLUE, curses.COLOR_BLACK)
	curses.init_pair(MONSTER_COLOR, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(ADD_HEALTH_COLOR, curses.COLOR_GREEN, curses.COLOR_BLACK)

	return stdscr


def end_curses(stdscr):
	#stdscr.nodelay(False)
	stdscr.keypad(False)
	curses.curs_set(1)
	curses.nocbreak()
	curses.echo()
	curses.endwin()


"""
def gen_map_step(map):
	tmp_map = copy.deepcopy(map)
	pass
"""


#!! needed to add cellular automata !!
def generate_map(map, sz_x, sz_y, map_symbols):
	rand_sum = 0
	for symbol in map_symbols:
		rand_sum += symbol[1]

	for i in range(sz_x):
		map.append([])
		for j in range(sz_y):
			if i == 0 or j == 0 or i == sz_x - 1 or j == sz_y - 1:
			   	map[i].append([WALL, WALL_COLOR])
			else:
				x = random.randint(1, rand_sum)
				for symbol in map_symbols:
					x -= symbol[1]
					if x <= 0:
						map[i].append(symbol[0])
						break


def map_mark_dfs(map, i, j):
	if map[i][j][0] != EMPTY:
		return []

	positions = [(i, j)]

	directions = [
		[1, 0],
		[-1, 0],
		[0, 1],
		[0, -1]
	]

	map[i][j] = (MARK, SIMPLE_COLOR)
	for d in directions:
	# walls on all sides, then no check needed there
		new_positions = map_mark_dfs(map, i + d[0], j + d[1])
		for pos in new_positions:
		   	positions.append(pos)

	return positions


def generate_doors(map):
	doors = []
	tmp_map = copy.deepcopy(map)

	for i in range(len(tmp_map)):
		for j in range(len(tmp_map[i])):
			if tmp_map[i][j][0] == EMPTY:
				map_mark_dfs(tmp_map, i, j)
				map[i][j] = [DOOR, DOOR_COLOR]
				doors.append([i, j])

	return doors


def random_direction():
	k = random.randint(0, 3)
	return [((k % 2) * 2 - 1) * (k // 2),
		   ((k % 2) * 2 - 1) * (1 - k // 2)]


def generate_monsters(map, rand_range, rand_monster):
	monsters = []
	for i in range(len(map)):
		for j in range(len(map[i])):
			if (map[i][j][0] == EMPTY):
				if random.randint(1, rand_range) <= rand_monster:
					
					monsters.append([[i, j], random_direction()])
					# position, move direction

	return monsters


def move_monsters(map, monsters):
	for i in range(len(monsters)):
		pos = [0, 0]
		pos[0] = monsters[i][0][0] + monsters[i][1][0]
		pos[1] = monsters[i][0][1] + monsters[i][1][1]
		if map[pos[0]][pos[1]][0] == EMPTY:
			monsters[i][0] = pos
			pass
		else:
			monsters[i][1] = random_direction()
			pass


def damage_player(monsters, player_state):
	for m in monsters:
		if abs(player_state[0][0] - m[0][0]) + abs(player_state[0][1] - m[0][1]) <= 1:
			player_state[1] -= 1
	pass


def game_step(map, monsters, player_state, doors):
	#if player_pos == door for any door ?
	move_monsters(map, monsters)
	damage_player(monsters, player_state)
	pass


def draw(stdscr, map, monsters, player_state):
	if player_state[1] <= 0:
		stdscr.addstr(max(curses.COLS // 2 - 4, 0),
				      max(curses.LINES // 2 - 4, 0), "You lose(")
		return

	stdscr.addstr(MAP_POS_Y - 1, 0, "Lives: " + str(player_state[1]),
		curses.color_pair(HIGHLIGHTED_COLOR))

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
			MONSTER, curses.color_pair(MONSTER_COLOR))

	stdscr.addstr(MAP_POS_Y + player_state[0][1],
		MAP_POS_X + player_state[0][0], PLAYER,
		curses.color_pair(PLAYER_COLOR))


def input(stdscr): # not work
	m = [0, 0]
	
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
	pass


def move_player(map, player_state, pos_change):
	new_player_pos = copy.deepcopy(player_state[0])

	new_player_pos[0] += pos_change[0]
	new_player_pos[1] += pos_change[1]

	if map[new_player_pos[0]][new_player_pos[1]][0] != WALL:
		player_state[0] = new_player_pos


def main():
	map_symbols = [
		[[EMPTY, SIMPLE_COLOR], 30],
		[[WALL, WALL_COLOR], 10],
		[['$', GOLD_COLOR], 1],
		[['/', WEAPON_COLOR], 2],
		[['+', ADD_HEALTH_COLOR], 1]
	]

	stdscr = begin_curses()

	map_size = [20, 20]

	player_state = [[0, 0], 10] # pos, lives

	map = []

	generate_map(map, map_size[0], map_size[1], map_symbols)

	doors = generate_doors(map)

	player_state[0] = doors[0]

	monsters = generate_monsters(map, 100, 7)

	main_loop_exception = False

	#try:
	while(True):
		stdscr.clear()
		game_step(map, monsters, player_state, doors)
		draw(stdscr, map, monsters, player_state)
		stdscr.refresh()
		pos_change = input(stdscr)
		move_player(map, player_state, pos_change)
		#time.sleep(0.1)

	#except:
	#	main_loop_exception = True

	end_curses(stdscr)

	if main_loop_exception:
		print("Error during main loop");


main()
