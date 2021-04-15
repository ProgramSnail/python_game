import curses
import random
import copy

MAP_POS_X = 16
MAP_POS_Y = 2

WEAPON_SPEED = 1

PLAYER = 'P'
MONSTER = 'M'
EMPTY = ' '
DOOR = '>'
MARK = '!'
WALL = '#'
GOLD = '$'
WEAPON = '/'
ACTIVE_WEAPON = '.'
ADD_HEALTH = '+'
SCORE = '@'

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
SCORE_COLOR = 11
ACTIVE_WEAPON_COLOR = 12

MONSTER_DAMAGE = 1

P_POS = 0
P_HEALTH = 1
P_WEAPON = 2
P_GOLD = 3
P_ACTIVE_DOOR = 4
P_SCORE = 5

MOVE_UP_ACTION = "KEY_UP"
MOVE_DOWN_ACTION = "KEY_DOWN"
MOVE_LEFT_ACTION = "KEY_LEFT"
MOVE_RIGHT_ACTION = "KEY_RIGHT"

ATTACK_UP_ACTION = 'w'
ATTACK_DOWN_ACTION = 's'
ATTACK_LEFT_ACTION = 'a'
ATTACK_RIGHT_ACTION = 'd'

NEXT_DOOR_ACTION = 'q'
PREV_DOOR_ACTION = 'e'

DIRECTIONS = [
	[0, -1],
	[0, 1],
	[-1, 0],
	[1, 0]
]

EXTENDED_DIRECTIONS = DIRECTIONS + [
	[1, 1],
	[1, -1],
	[-1, 1],
	[-1, -1]
]


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
	curses.init_pair(SCORE_COLOR, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(ACTIVE_WEAPON_COLOR, curses.COLOR_YELLOW, curses.COLOR_BLACK)

	return stdscr


def end_curses(stdscr):
	#stdscr.nodelay(False)
	stdscr.keypad(False)
	curses.curs_set(1)
	curses.nocbreak()
	curses.echo()
	curses.endwin()



def gen_map_step(map):
	tmp_map = copy.deepcopy(map)
	for i in range(1, len(map) - 1):
		for j in range(1, len(map[i]) - 1):
			x = 0
			for d in EXTENDED_DIRECTIONS:
				if tmp_map[i + d[0]][j + d[1]][0] == WALL:
					x += 1
			if x < 2 or x >= 4:
				map[i][j] = [EMPTY, SIMPLE_COLOR]
			elif x >= 3 and x <= 3:
				map[i][j] = [WALL, WALL_COLOR]


def generate_map(map, sz_x, sz_y, map_symbols,
				 automata_iterations, wall_rand_range,
				 wall_rand_gen):
	rand_sum = 0
	for symbol in map_symbols:
		rand_sum += symbol[1]

	for i in range(sz_x):
		map.append([])
		for j in range(sz_y):
			if i == 0 or j == 0 or i == sz_x - 1 or j == sz_y - 1:
			   	map[i].append([WALL, WALL_COLOR])
			else:
				if random.randint(1, wall_rand_range) <= wall_rand_gen:
					map[i].append([WALL, WALL_COLOR])
				else:
					map[i].append([EMPTY, SIMPLE_COLOR])

	for i in range(automata_iterations):
		gen_map_step(map)

	for i in range(1, len(map) - 1):
		for j in range(1, len(map[i]) - 1):
			if (map[i][j][0] == EMPTY):
				x = random.randint(1, rand_sum)
				for symbol in map_symbols:
					x -= symbol[1]
					if x <= 0:
						map[i][j] = symbol[0]
						break



def map_mark_dfs(map, i, j):
	if map[i][j][0] == WALL or map[i][j][0] == MARK:
		return []

	positions = [(i, j)]

	map[i][j] = (MARK, SIMPLE_COLOR)
	for d in DIRECTIONS:
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
		if map[pos[0]][pos[1]][0] != WALL:
			monsters[i][0] = pos
			pass
		else:
			monsters[i][1] = random_direction()
			pass


def damage_player(monsters, player_state):
	for m in monsters:
		if abs(player_state[P_POS][0] - m[0][0]) + abs(player_state[P_POS][1] - m[0][1]) <= 1:
			player_state[P_HEALTH] -= MONSTER_DAMAGE
	pass


def game_step(map, monsters, player_state, doors):
	#if player_pos == door for any door ?
	move_monsters(map, monsters)
	damage_player(monsters, player_state)
	pass


def draw(stdscr, map, monsters, active_weapon, player_state):
	stdscr.addstr(0, 0, str(player_state))

	info_str = [
		"Health: " + str(player_state[P_HEALTH]),
		"Weapon: " + str(player_state[P_WEAPON]),
		"Gold: " + str(player_state[P_GOLD]),
		"",
		"Help:",
		"",
		"ARROWS - move",
		"",
		"WASD - use",
		"weapon",
		"",
		"QE - move",
		"through doors",
		"",
		"You must",
		"collect",
		"all score",
		"",
		"% - weapon",
		"# - wall",
		"@ - score",
		"M - monster",
		"P - player", 
		"> - door",
		"$ - money",
		"+ - add health"
	]

	for i in range(len(info_str)):
		stdscr.addstr(MAP_POS_Y - 1 + i, 0, info_str[i],
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

	for w in active_weapon:
		stdscr.addstr(w[0][1] + MAP_POS_Y, w[0][0] + MAP_POS_X,
			ACTIVE_WEAPON, curses.color_pair(ACTIVE_WEAPON_COLOR))

	stdscr.addstr(MAP_POS_Y + player_state[P_POS][1],
		MAP_POS_X + player_state[P_POS][0], PLAYER,
		curses.color_pair(PLAYER_COLOR))


def input(stdscr): # not work
	m = [0, 0]
	key = ""
	
	try:
		key = stdscr.getkey()
		if key == MOVE_UP_ACTION:
			m[1] -= 1
		elif key == MOVE_DOWN_ACTION:
			m[1] += 1
		elif key == MOVE_LEFT_ACTION:
			m[0] -= 1
		elif key == MOVE_RIGHT_ACTION:
			m[0] += 1
	except:
		pass
		# no input
	
	return (m, key)
	pass


def move_player(map, player_state, pos_change):
	p = copy.deepcopy(player_state[0])

	p[0] += pos_change[0]
	p[1] += pos_change[1]

	x = map[p[0]][p[1]][0]

	if x != WALL:
		player_state[0] = p
		if x == ADD_HEALTH:
			player_state[P_HEALTH] += 1
		elif x == WEAPON:
			player_state[P_WEAPON] += 1
		elif x == GOLD:
			player_state[P_GOLD] += 1
		elif x == SCORE:
			player_state[P_SCORE] += 1

	if x != WALL and x != DOOR:
		map[p[0]][p[1]] = [EMPTY, SIMPLE_COLOR]


def use_weapon(map, active_weapon, player_state, direction):
	p = copy.deepcopy(player_state[P_POS])
	p[0] += direction[0]
	p[1] += direction[1]
	if map[p[0]][p[1]][0] == WALL:
		if p[0] != 0 and p[1] != 0 and p[0] != len(map) - 1 and p[1] != len(map[0]):
			map[p[0]][p[1]] = [EMPTY, SIMPLE_COLOR]
	else: 
		active_weapon.append([p, copy.deepcopy(direction)])


def player_actions(map, doors, active_weapon, player_state, player_action):
	if doors[player_state[P_ACTIVE_DOOR]]:
		if player_action == NEXT_DOOR_ACTION:
			player_state[P_ACTIVE_DOOR] += 1
			player_state[P_ACTIVE_DOOR] %= len(doors)
			player_state[P_POS] = copy.deepcopy(
				doors[player_state[P_ACTIVE_DOOR]])
		elif player_action == PREV_DOOR_ACTION:
			player_state[P_ACTIVE_DOOR] = (player_state[P_ACTIVE_DOOR]
				+ len(doors) - 1) % len(doors)
			player_state[P_POS] = copy.deepcopy(
				doors[player_state[P_ACTIVE_DOOR]])
	k = -1
	if player_action == ATTACK_UP_ACTION:
		k = 0
	elif player_action == ATTACK_DOWN_ACTION:
		k = 1
	elif player_action == ATTACK_LEFT_ACTION:
		k = 2
	elif player_action == ATTACK_RIGHT_ACTION:
		k = 3
	
	if k >= 0:
		use_weapon(map, active_weapon, player_state, DIRECTIONS[k])
	


def move_weapon(map, active_weapon, player_state): # needed to test
	remove_list = []
	for i in range(len(active_weapon)):
		p = copy.deepcopy(active_weapon[i][0])
		p[0] += active_weapon[i][1][0]
		p[1] += active_weapon[i][1][1]
		if map[p[0]][p[1]][0] == WALL or \
		   map[p[0]][p[1]][0] == DOOR:
			p = active_weapon[i][0]
			if map[p[0]][p[1]][0] == SCORE:
				player_state[P_SCORE] += 1
			map[p[0]][p[1]] = [WALL, WALL_COLOR]
			remove_list.append(i)
		else:
			active_weapon[i][0] = p
	
	for i in remove_list:
		active_weapon.remove(active_weapon[i])
	

def calc_max_score(map):
	max_score = 0
	for row in map:
		for cell in row:
			if cell[0] == SCORE:
				max_score += 1
	return max_score


def main():
	map_symbols = [
		[[EMPTY, SIMPLE_COLOR], 90],
		[[GOLD, GOLD_COLOR], 2],
		[[WEAPON, WEAPON_COLOR], 4],
		[[ADD_HEALTH, ADD_HEALTH_COLOR], 2],
		[[SCORE, SCORE_COLOR], 2]
	]

	stdscr = begin_curses()

	map_size = [40, 20]

	active_weapon = [] # positions of active weapon

	map = []

	generate_map(map, map_size[0], map_size[1], map_symbols, 20, 100, 45)

	doors = generate_doors(map)

	monsters = generate_monsters(map, 100, 3)

	max_score = calc_max_score(map)

	player_state = [doors[0], 10, 2, 0, 0, 0]
	# pos = [x, y], lives, weapon, money, active door, score

	main_loop_exception = False

	player_win = False

	try:
		while(True):
			stdscr.clear()
			game_step(map, monsters, player_state, doors)
			draw(stdscr, map, monsters, active_weapon, player_state)
			stdscr.refresh()
			pos_change, player_action = input(stdscr)
			move_player(map, player_state, pos_change)
			player_actions(map, doors, active_weapon, player_state, player_action)
			for i in range(WEAPON_SPEED):
				move_weapon(map, active_weapon, player_state)
			if player_state[P_HEALTH] <= 0:
				break
			if player_state[P_SCORE] == max_score:
				player_win = True
				break # win
	except:
		main_loop_exception = True

	end_curses(stdscr)

	if main_loop_exception:
		print("Error during main loop")
	elif player_win:
		print("You win!")
	else:
		print("You lose(")


main()
