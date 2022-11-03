def construct_board(board_letters=[]):
    board = [[False for _i in range(15)] for _j in range(15)]
    for tile in board_letters:
        index, letter = tile['index'], tile['letter']
        row, col = index // 15, index % 15
        board[row][col] = letter
    return board
