import os
from random import randrange, choice

def store_board_to_file(board, path):
  file_names = os.listdir(path)
  board_number = len(file_names) + 1
  board_filename = 'bingo_board_' + str(board_number)

  with open(path + board_filename, 'w') as file:
    file.write(str(board))

def load_boards(path, board_name = None):
  file_names = os.listdir(path) if not board_name else [board_name]

  boards = []

  for file_name in file_names:
    with open(path + file_name, 'r') as file:
      for line in file:
        boards.append(eval(line))
  
  return boards

def generate_bingo_board(maxNum = 90):
  maxNum = maxNum if maxNum % 10 == 0 else 90
  cols = maxNum // 10
  rows = cols * 2
  rowsInRoute = 3
  routes = rows // rowsInRoute
  numsInRoute = maxNum // routes

  values = [[x * 10 + y for y in range(0, cols + 1)] for x in range(0, cols)]
  del values[0][0]
  values[len(values) - 1].append(maxNum)

  board = []

  for i in range(routes):
    route = generate_bingo_route(rowsInRoute, cols, maxNum, numsInRoute, values, rows, board, True)
    board.append(route)

  fill_remaining_numbers(board, values, numsInRoute, maxNum, rowsInRoute)

  path = os.getcwd() + '/bingo_boards/'
  store_board_to_file(board, path)


global bingo_route_id
bingo_route_id = 0 # TODO fix usage of this
def generate_bingo_route(rowsInRoute, cols, maxNum, numsInRoute, values, maxRows, board, init, route = None, routeNum = 0):
  global bingo_route_id
  numsInRow = numsInRoute // rowsInRoute
  usedIndices = set()
  route = []

  for i in range(rowsInRoute):
    row = []
    indices = generate_init_indices(values, numsInRow, usedIndices, rowsInRoute)
    for j in range(cols):
      if j not in indices:
        col = None
      else:
        col = choice(values[j])
        values[j].remove(col)
      row.append(col)
    route.append(row)

  bingo_route_id += 1
  return [bingo_route_id, route]

# Used to make sure it's at least one of each number type (e.g. 1s, 10s, 20s...80s) in each route
def generate_init_indices(values, numsInRow, usedIndices, rowsInRoute):
  generatedIndices = []
  possibleIndices = [x for x in range(len(values))]

  notFromUsedIndices = 0
  for i in range(len(values)):
    possibleAndUsedDifference = list(set(possibleIndices).difference(usedIndices))
    if len(values[i]) > 0 and len(usedIndices) < len(values) and notFromUsedIndices < len(values) // rowsInRoute and len(possibleAndUsedDifference) > 0:
      notFromUsedIndices += 1
      number = choice(possibleAndUsedDifference)
      generatedIndices.append(number)
      usedIndices.add(number)

  return sorted(generatedIndices)

def fill_remaining_numbers(board, values, numsInRoute, maxNum, rowsInRoute):
  index_matrix = []
  numsInRow = numsInRoute // rowsInRoute
  
  for routes in board:
    for route in range(len(routes[1])):
      row = []
      for i in range(len(routes[1][route])):
        col = None if routes[1][route][i] == None else routes[1][route][i]
        row.append(col)
      index_matrix.append(row)

  old_index_matrix = [x[:] for x in index_matrix] # need deep copies (ref. e.g. Redux state)
  old_values = [x[:] for x in values]

  while True:
    col = len(values) - 1
    retry = False

    for i in range(len(values) - 1, -1, -1): # starts from top to maximize chances of convolution
      nums = values[i]
      count = 0
      row_index = 0

      while len(nums) > 0:
        row_index = randrange(len(index_matrix))
        row_set = set(index_matrix[row_index])

        if index_matrix[row_index][col] == None and not len(row_set) > numsInRow:
          value = choice(nums)
          index_matrix[row_index][col] = value
          nums.remove(value)
        elif count > maxNum:
          break

        count += 1
      col -= 1
    
    for index_values in values:
      if len(index_values) > 0: # Distribution of numbers has not worked, try again
        retry = True

    if retry:
      values = [x[:] for x in old_values]
      index_matrix = [x[:] for x in old_index_matrix]
      continue
    else:
      break

  index = 0
  for i in range(len(board)):
    for j in range(len(board[i][1])):
      board[i][1][j] = index_matrix[index]
      index += 1

def print_board(board):
  for route in board:
    width = (len(route[1][0]) * 5)
    print('Route id', route[0])
    print('_' * width)
    
    for row_index in range(len(route[1])):
      for value in route[1][row_index]:
        print(str(value if value else ' ').rjust(2, ' '), sep=' ', end=' | ')
      if row_index < len(route[1]):
        print('')

    print('_' * width)

# generate_bingo_board()

def find_route(route_id, path):
  boards = load_boards(path)

  for board in boards:
    for route in board:
      if route_id == route[0]: return route

  return False

# print(find_route(7, os.getcwd() + '/bingo_boards/'))

# TODO main function for generating a number of bingo boards (make sure this purges stored boards or something)

# TODO check if a route is winner function

# TODO running of a bingo game function
