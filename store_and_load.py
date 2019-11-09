import os
from fpdf import FPDF

# Optimalized for bingo boards with 90 numbers
def generate_PDF_from_board(board_name, in_path, out_path):
  board = load_boards(in_path, board_name)

  pdf = FPDF()
  pdf.add_page()
  pdf.set_left_margin(pdf.w / 4)

  cols = len(board[0][0][1][1]) # board[0][0][1][1] is the first possible row in the board file
  rows = cols * 2

  spacing = 1
  col_width = pdf.w / 2 / cols
  row_height = pdf.h / rows - (len(board) * (rows / rows * 5))

  id_width = pdf.w / 2 / (cols * 2)
  id_height = pdf.h / (rows * 2)

  for route in board[0]:
    pdf.set_font('Arial', size=8)
    route_id = route[0]
    pdf.cell(id_width, id_height, txt=str(route_id))
    pdf.ln(id_height * spacing)

    pdf.set_font('Arial', style='B', size=14)

    for row in route[1]:
      for col in row:
        if col == None:
          col = ' '

        pdf.cell(col_width, row_height * spacing, txt=str(col), border=1, align='C')
      pdf.ln(row_height * spacing)
    pdf.ln(row_height / 2 * spacing / 4)

  pdf.output(out_path + board_name + '.pdf')

#path = os.getcwd() + '/bingo_boards/'
#out_path = path + 'pdf/'

# generate_PDF_from_board('bingo_board_1', path, out_path)

def store_board_to_file(board, path):
  file_names = [x for x in os.listdir(path) if os.path.isfile(path + x)]
  board_number = len(file_names) + 1
  board_filename = 'bingo_board_' + str(board_number)

  with open(path + board_filename, 'w') as file:
    file.write(str(board))

  out_path = path + 'pdf/'
  generate_PDF_from_board(board_filename, path, out_path)

def load_boards(path, board_name = None):
  file_names = [x for x in os.listdir(path) if os.path.isfile(path + x)] if not board_name else [board_name]

  boards = []

  for file_name in file_names:
    with open(path + file_name, 'r') as file:
      for line in file:
        boards.append(eval(line))
  
  return boards
