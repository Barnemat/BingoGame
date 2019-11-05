from random import randrange, choice

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
    route = generate_bingo_route(rowsInRoute, cols, maxNum, numsInRoute, values, rows, board)
    board.append(route)

  print(board)

bingo_route_id = 0 # TODO fix usage of this
def generate_bingo_route(rowsInRoute, cols, maxNum, numsInRoute, values, maxRows, board):
  route = []
  numsInRow = numsInRoute // rowsInRoute
  rowsLeft = maxRows - (len(board) * rowsInRoute)

  for i in range(rowsInRoute):
    row = []

    indices = generate_indices(values, numsInRow, rowsLeft)
    for j in range(cols):
      if j not in indices:
        col = None
      else:
        col = choice(values[j])
        values[j].remove(col)
      row.append(col)
    route.append(row)

    rowsLeft -= 1

  return route

# TODO Add functionality for at least one use of an index in each route
def generate_indices(values, numsInRow, rowsLeft):
  generatedIndices = []

  for i in range(len(values)):
    if len(values[i]) == rowsLeft and len(values[i]) > 0:
      generatedIndices.append(i)

  for i in range(numsInRow - len(generatedIndices)):
    index = randrange(len(values))

    while (len(values[index]) == 0 or index in generatedIndices):
      index = randrange(len(values))

    generatedIndices.append(index)

  return sorted(generatedIndices)

def print_board(board):
  for i in range(board):
    pass

generate_bingo_board()