# Define the matrix with positions
matrix = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 9: (2, 2),
    0: (3, 1)
}

# Define possible moves for a knight in chess
knight_moves = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]


def get_knight_moves(position):
    if position not in matrix:
        return []

    # Get the current position in (row, col) format
    row, col = matrix[position]

    possible_positions = []

    for move in knight_moves:
        new_row = row + move[0]
        new_col = col + move[1]

        # Find the key in the matrix dictionary corresponding to (new_row, new_col)
        for key, value in matrix.items():
            if value == (new_row, new_col):
                possible_positions.append(key)
                break

    return possible_positions

if __name__ == "__main__":
    # Example usage:
    positions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    move_count = 0
    for position in positions:
        possible_moves = get_knight_moves(position)
        move_count += len(possible_moves)
        print(f"Possible moves for the knight from position {position}: {possible_moves}")
    print(f"Total number of possible moves: {move_count}")
