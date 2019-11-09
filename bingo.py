import os
from random import choice

from store_and_load import load_boards
from generate_bingo_board import generate_bingo_board

def find_route(route_id, path):
  boards = load_boards(path)

  for board in boards:
    for route in board:
      if route_id == route[0]: return route

  return False

def draw_number(numbers, drawn_numbers):
  return choice(list(numbers.difference(drawn_numbers)))

def check_if_bingo(route, drawn_numbers, bingo_row):
  if route:
    rowsInRoute = len(route[1])
    numsInRoute = (len(set(route[1][0])) - 1) * rowsInRoute
    numsInRow = numsInRoute // rowsInRoute

    rows = 0
    for row in route[1]:
      nums = 0
      for value in row:
        if not value:
          continue

        if value in drawn_numbers:
          nums += 1
        else:
          break

      if nums == numsInRow:
        rows += 1

      if rows >= bingo_row:
        return True
    return False
  elif len(route_id) > 0:
    return False

def run_bingo_game(number_of_new_boards, maxNum):
  global bingo_route_id
  path = os.getcwd() + '/bingo_boards/'

  print('Remember to clean the /bingo_boards folder, if you need all new boards')

  boards = load_boards(path)

  cols = maxNum // 10
  rows = cols * 2
  bingo_route_id = 0 if len(boards) == 0 else len(boards) * (rows // 3)

  for i in range(number_of_new_boards):
    generate_bingo_board(maxNum)

  numbers = set([x for x in range(1, maxNum + 1)])
  drawn_numbers = set()

  last_number = None
  bingo_row = 1

  while True:
    generate = input('\nGenerate new Bingo board? y/N, else draw new number: ')

    if generate == 'y' or generate == 'Y':
      generate_bingo_board(maxNum)
      continue

    last_number = draw_number(numbers, drawn_numbers)
    drawn_numbers.add(last_number)

    print('Last drawn number: ', last_number, ' - Round: ', len(drawn_numbers))

    bingo = False
    while input('Bingo? y/N') == 'y':
      route_id = input('Type route id to control bingo route: ')

      if route_id.isdigit(): route_id = int(route_id) # separate into function
      
      route = find_route(route_id, path)
      last_was_bingo = check_if_bingo(route, drawn_numbers, bingo_row)

      if last_was_bingo:
        bingo = True
        print('Bingo was valid')
      else:
        print('Bingo was invalid')
    
    if len(drawn_numbers) == maxNum:
      break

    if bingo:
      bingo_row += 1
      if bingo_row > 3: break
      print('Switching to ', bingo_row, ' rows bingo')

  print('Bingo is done.')  

run_bingo_game(5, 90) # Functionality for numbers other than 90 does not work at the moment
