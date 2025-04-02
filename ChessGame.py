import copy

WHITE = "White"
BLACK = "Black"

FILES = {"A":1, "B":2, "C":3, "D":4, "E":5, "F":6,"G":7, "H":8}
I_FILES = {j:i for i,j in FILES.items()}

class Square(): # an empty spot on the board

    def __init__(self, game, file, rank, square_colored):
        if not isinstance(game, Chess):
            raise TypeError("Game must be a Chess object")
        self.game = game
        self.file = file
        self.rank = rank
        # Using boolean for a positions color: True = black, False = white
        self.square_colored = square_colored
        self.passantable = False

    def __str__(self):
        return "    "
    
class Piece(Square): # the foundational class of all the following pieces
    def __init__(self, game, file, rank, square_colored, team):
        Square.__init__(self, game, file, rank, square_colored)
        self.team = team
        self.first_move = True # used for pieces that have a special move condition given it is their first move

    def move_to(self, file, rank):
        """
        Moves the piece to the specified file and rank on the board.

        Args:
            self: The instance of the piece object.
            file: The target file (column) coordinate of the move.
            rank: The target rank (row) coordinate of the move.

        Returns:
            A string describing the move in a human-readable format (e.g., "White Pawn at E2 moved to E4").
        """
        self.first_move = False # for pawn first move
        # Create an empty square to replace this location after this piece moves
        prev = Square(self.game, self.file, self.rank, self.square_colored)
        prev_file = self.file
        prev_rank = self.rank

        # Move this piece to the new location
        self.file = file
        self.rank = rank
        self.square_colored = self.game.board[file][rank].square_colored
        self.game.board[file][rank] = self

        # Set the empty square to replace the moved piece
        self.game.board[prev_file][prev_rank] = prev

        return (f"{self.team.title()} {self.__class__.__name__} at {I_FILES[prev_file]}{prev_rank} moved to {I_FILES[file]}{rank}")
        
    # Checks is a given position is a valid position on a chess board
    def on_board(self, file, rank):
        """
        Checks if the given file and rank coordinates are within the bounds of the chessboard.

        Args:
            self: The instance of the class containing the board information (optional).
            file: The file (column) coordinate of the position to check (1-8).
            rank: The rank (row) coordinate of the position to check (1-8).

        Returns:
            True if the coordinates are within the board bounds (1 <= file <= 8 and 1 <= rank <= 8), False otherwise.
        """
        if not (file in range(1,9) and rank in range(1,9)):
            #print("Not a valid position on the board!")
            return False
        else:
            return True
    
    # Checks if this piece is already at the given location
    def already_there(self, file, rank):
        """
        Checks if the piece is already located at the given file and rank.

        Args:
        self: The instance of the class containing the piece's current position.
        file: The file (column) to check.
        rank: The rank (row) to check.

        Returns:
        True if the piece is already at the given file and rank, False otherwise.
        """
        if (file == self.file and rank == self.rank):
            #print("Already there!")
            return True
        else:
            return False
    

    def your_piece_there(self, file, rank):
        """
        Checks if there is a piece belonging to the same team at the given file and rank.

        Args:
            self: The instance of the class containing the current player's information.
            file: The file (column) coordinate to check.
            rank: The rank (row) coordinate to check.

        Returns:
            True if there is a piece belonging to the same team at the specified location, False otherwise.
        """
        if (isinstance(self.game.board[file][rank], Piece) and self.game.board[file][rank].team == self.team):
            #print(f"{self} cannot move to {file}{rank} because {self.game.board[file][rank]} is already there!")
            return True
        else:
            return False
        
    def can_move_to(self, file, rank):
        """
        Checks if the piece can move to the user inputted file and rank.

        Args:
        self: The instance of the class containing the piece's current position.
        file: The file (column) to check.
        rank: The rank (row) to check.

        Returns:
        Represents an abstract as every child piece has its own can_move_to function.
        """
        pass

class Pawn(Piece):
    def __init__(self, game, file, rank, square_colored, team):
        super().__init__(game, file, rank, square_colored, team)

    def __str__(self):
        return " ♙  " if self.team == BLACK else " ♟  "

    def can_capture(self, file, rank):
        """
        Checks if the piece can capture the opponent's piece at the given file and rank.

        Args:
            self: The instance of the piece object.
            file: The file (column) coordinate of the target square.
            rank: The rank (row) coordinate of the target square.

        Returns:
            True if the piece can capture the opponent's piece at the given location, False otherwise.
        """
        # Check if the target square has an opponent's piece to capture
        if isinstance(self.game.board[file][rank], Piece):
            if self.team == WHITE:
                if rank == self.rank + 1 and abs(file - self.file) == 1:
                    return True
            else:
                if rank == self.rank - 1 and abs(file - self.file) == 1:
                    return True
        return False

    def can_move_to(self, file, rank):
        """
        Checks if the piece can legally move to the specified file and rank.

        Args:
            self: The instance of the piece object.
            file: The target file (column) coordinate of the move.
            rank: The target rank (row) coordinate of the move.

        Returns:
            True if the move is legal for the piece, False otherwise. The pawn specifically checks the color of the piece,
            the diagonal opponent pieces to determine if it can take diagonally, and first move to determine if the piece
            can move one or two spaces.
        """
        if self.already_there(file, rank) or not self.on_board(file, rank)  or self.your_piece_there(file, rank):
            return False
        
        # For White pawns (moving upwards (rank + 1) on the board)
        if self.team == WHITE:
            # First move: Can move 2 squares ahead, or 1 square ahead (without capture)
            if self.first_move:
                # Moving two squares forward
                if file == self.file and rank == self.rank + 2 and not isinstance(self.game.board[file][rank], Piece) and not isinstance(self.game.board[self.file][self.rank+1], Piece):
                    return True
                # Moving one square forward
                elif file == self.file and rank == self.rank + 1 and not isinstance(self.game.board[file][rank], Piece):
                    return True
                # Diagonal captures
                elif (file == self.file + 1 or file == self.file - 1) and rank == self.rank + 1 and self.can_capture(file, rank):
                    return True
                else:
                    return False
            else:
                # After the first move, can move only 1 square forward
                if file == self.file and rank == self.rank + 1 and not isinstance(self.game.board[file][rank], Piece):
                    return True
                elif (file == self.file + 1 or file == self.file - 1) and rank == self.rank + 1 and self.can_capture(file, rank):
                    return True
                else:
                    return False

        # For Black pawns (moving downwards (rank - 1) on the board)
        elif self.team == BLACK:
            if self.first_move:
                if file == self.file and rank == self.rank - 2 and not isinstance(self.game.board[file][rank], Piece) and not isinstance(self.game.board[self.file][self.rank-1], Piece):
                    return True
                elif file == self.file and rank == self.rank - 1 and not isinstance(self.game.board[file][rank], Piece):
                    return True
                elif (file == self.file + 1 or file == self.file - 1) and rank == self.rank - 1 and self.can_capture(file, rank):
                    return True
                else:
                    return False
            else:
                if file == self.file and rank == self.rank - 1 and not isinstance(self.game.board[file][rank], Piece):
                    return True
                elif (file == self.file + 1 or file == self.file - 1) and rank == self.rank - 1 and self.can_capture(file, rank):
                    return True
                else:
                    return False
        return False
    
    def move_to(self, file, rank):
        """
        Moves the pawn to the specified file and rank. 
        Promotes the pawn to a Queen if it reaches the opposite end of the board.

        Args:
            self: The instance of the pawn object.
            file: The target file (column) coordinate of the move.
            rank: The target rank (row) coordinate of the move.

        Returns:
            A string describing the move in a human-readable format. Calls the parent class's `move_to` method to handle 
            the basic movement logic. If the pawn reaches the opposite end of the board (rank 1 or 8), promotes the pawn to a Queen.
        """
        response = super().move_to(file, rank)
        if rank == 8 or rank == 1:
            self.promote()
        return response

    def promote(self):
        """
        Promotes the pawn to a chosen piece.

        This method allows the player to choose the piece to promote their pawn to 
        when it reaches the opposite end of the board.

        Args:
            self: The instance of the pawn object. Calls the `game.promote()` method to handle 
            the actual promotion within the game logic.
        """
        choice = input("Pawn promotion! Pick which piece (Q, B, R, K) you would like:\n")
        while choice not in ["Q", "q", "B", "b", "R", "r", "K", "k"]:
            print("Invalid choice! Try again:\n")
            choice = input("Pawn promotion! Pick which piece (Q, B, R, K) you would like:\n")
        self.game.promote(self, choice)
    

class Rook(Piece):
    def __init__(self, game, file, rank, square_colored, team):
        super().__init__(game, file, rank, square_colored, team)

    def __str__(self):
        return " ♖  " if self.team == BLACK else " ♜  "
    

    def can_move_to(self, file, rank):
        """
        Checks if the piece can legally move to the specified file and rank.

        Args:
            self: The instance of the piece object.
            file: The target file (column) coordinate of the move.
            rank: The target rank (row) coordinate of the move.

        Returns:
            True if the move is legal for the piece, False otherwise. The pawn specifically checks the color of the piece,
            the diagonal opponent pieces to determine if it can take diagonally, and first move to determine if the piece
            can move one or two spaces.
        """
        if self.already_there(file, rank) or not self.on_board(file, rank) or self.your_piece_there(file, rank):
            return False
        # Check vertical movement
        if self.file == file:
            step = 1 if rank > self.rank else -1
            for r in range(self.rank + step, rank, step):
                if isinstance(self.game.board[file][r], Piece):
                    return False
            return True
        # Check horizontal movement
        if self.rank == rank:
            step = 1 if file > self.file else -1
            for f in range(self.file + step, file, step):
                if isinstance(self.game.board[f][rank], Piece):
                    return False
            return True
        return False 

class Knight(Piece):

    def __str__(self):
        return " ♘  " if self.team == BLACK else " ♞  "
    
    def can_move_to(self, file, rank):
        """
        Checks if the Knight can legally move to the specified file and rank.

        Args:
            self: The instance of the Knight object.
            file: The target file (column) coordinate of the move.
            rank: The target rank (row) coordinate of the move.

        Returns:
            True if the move is legal for the Knight, False otherwise.
        """
        if self.already_there(file, rank) or not self.on_board(file, rank) or self.your_piece_there(file, rank):
            return False
        possible_moves = [(self.file+2, self.rank+1),
                          (self.file+2, self.rank-1),
                          (self.file+1, self.rank+2),
                          (self.file+1, self.rank-2),
                          (self.file-2, self.rank+1),
                          (self.file-2, self.rank-1),
                          (self.file-1, self.rank+2),
                          (self.file-1, self.rank-2)]
        return (file,rank) in possible_moves
    

class Bishop(Piece):

    def __str__(self):
        return " ♗  " if self.team == BLACK else " ♝  "
    
    def can_move_to(self, file, rank):
        """
        Checks if the Bishop can legally move to the specified file and rank.

        Args:
            self: The instance of the Bishop object.
            file: The target file (column) coordinate of the move.
            rank: The target rank (row) coordinate of the move.

        Returns:
            True if the move is legal for the Bishop, False otherwise. While loops check all spaces the bishop
            can move to in order to determine if a piece is in its path
        """
        if self.already_there(file, rank) or not self.on_board(file, rank) or self.your_piece_there(file, rank):
            return False
        if abs(file - self.file) != abs(rank - self.rank):
            return False # not a diagonal move
        
        # Calculate the change in position of the Bishop
        step_file = 1 if file > self.file else -1
        step_rank = 1 if rank > self.rank else -1
        current_file = self.file + step_file
        current_rank = self.rank + step_rank

        # While loop to see if a space is occupied by a piece or not
        while current_file != file and current_rank != rank:
            if isinstance(self.game.board[current_file][current_rank], Piece):
                return False
            current_file += step_file
            current_rank += step_rank
        return True
    

class King(Piece):
    def __init__(self, game, file, rank, square_colored, team):
        super().__init__(game, file, rank, square_colored, team)

    def __str__(self):
        return " ♔  " if self.team == BLACK else " ♚  "
    
    
    def can_castle(self, left): # Castle code check for King
        """
        Checks if the King can legally castle and performs the castling move.

        Args:
            self: The instance of the King object.
            left: Boolean indicating whether to castle to the left (True) or right (False).

        Returns:
            Moves the King and the corresponding Rook to their respective castling positions 
            if castling is legal. Updates the `first_move` attribute of the King and the Rook.
        """
        if self.team == WHITE:
            rank = 1
        else:
            rank = 8

        if left:
            if self.first_move and isinstance(self.game.board[1][rank], Rook) and self.game.board[1][rank].first_move:
                self.move_to(3,rank)
                rook = self.game.board[1][rank]
                #prev = Square(rook.game, rook.file, rook.rank, rook.square_colored)
                rook.move_to(4, rank)
                #self.game.board[1][rank] = prev
                return (f"{self.team} castled!")
        else:
            if self.first_move and isinstance(self.game.board[8][rank], Rook) and self.game.board[8][rank].first_move:
                self.move_to(7,rank)
                rook = self.game.board[8][rank]
                #prev = Square(rook.game, rook.file, rook.rank, rook.square_colored)
                rook.move_to(6, rank)
                #self.game.board[1][rank] = prev
                return (f"{self.team} castled!")
        return False

    def can_move_to(self, file, rank):
        """
        Checks if the King can legally move to the specified file and rank.

        Args:
            self: The instance of the King object.
            file: The target file (column) coordinate of the move.
            rank: The target rank (row) coordinate of the move.

        Returns:
            True if the move is legal for the King, False otherwise. Checks specifically if the King attempts to move
            more than one space, otherwise the movement is similar to the queens
        """
        if self.already_there(file, rank) or not self.on_board(file, rank) or self.your_piece_there(file, rank):
            return False
        moves = [(i, j) for i in range(self.file-1, self.file +2) for j in range(self.rank-1, self.rank+2)]
        return (file, rank) in moves


        

class Queen(Piece):

    def __str__(self):
        return " ♕  " if self.team == BLACK else " ♛  "
    
    def can_move_to(self, file, rank):
        """
        Checks if the Queen can legally move to the specified file and rank.

        Args:
            self: The instance of the Queen object.
            file: The target file (column) coordinate of the move.
            rank: The target rank (row) coordinate of the move.

        Returns:
            True if the move is legal for the Rook, False otherwise. Similar to the bishop and rook, checks if any other
            piece is in its path and would then return the move invalid.
        """
        if self.already_there(file, rank) or not self.on_board(file, rank) or self.your_piece_there(file, rank):
            return False
        if self.file == file or self.rank == rank: # copied in rook movement
            if self.file == file:
                step = 1 if rank > self.rank else -1
                for r in range(self.rank + step, rank, step):
                    if isinstance(self.game.board[file][r], Piece):
                        return False
                return True
            if self.rank == rank:
                step = 1 if file > self.file else -1
                for f in range(self.file + step, file, step):
                    if isinstance(self.game.board[f][rank], Piece):
                        return False
                return True
        else: # copied in bishop movement
            if abs(file - self.file) != abs(rank - self.rank):
                return False
            step_file = 1 if file > self.file else -1
            step_rank = 1 if rank > self.rank else -1
            current_file = self.file + step_file
            current_rank = self.rank + step_rank
            while current_file != file and current_rank != rank:
                if isinstance(self.game.board[current_file][current_rank], Piece):
                    return False
                current_file += step_file
                current_rank += step_rank
            return True
        return False
    

class Chess():

    def __init__(self):
        self.board = self.make_board()
        self.white_turn = True
        self.turn_number = 1
        # using a list here because tuples are not mutable and that causes issues
        self.white_king_pos = (5, 1)
        self.black_king_pos = (5, 8)

    def __str__(self):
        game_string = "\n"
        for rank in range(8, 0, -1):
            row = f"{rank}: " # adds rank numbers legend
            for file in range(1, 9):
                piece = self.board[file][rank]
                if isinstance(piece, Piece):
                    row += f"{str(piece)}"
                else:
                    row += " .  "
            game_string += row + "\n\n" # seperates the lines by a new line for visuals
        game_string += "    a   b   c   d   e   f   g   h\n" # adds files letters legend
        return game_string

    def play(self):
        """
        Plays a complete game of chess. This method handles the main game loop, alternating turns between players 
        until a winner is determined.

        Args:
            self: The instance of the Game class.

        Returns:
            Alternates turns between White and Black players, increments the turn number for each turn, determines the winner of the game,
            and prints the final board state and the winner.
        """
        winner = None
        while not winner:
            winner = self.turn()
            self.white_turn = not self.white_turn
            self.turn_number += 1
        print(self)
        print(winner)

    def turn(self):
        """
        Handles each turn in the game

        Prompts the user for an input, and handles translating that input into a location of their piece to be moved.
        This process is then repeated for the destination of the selected piece.
        There are loops in place to handle invalid selections and the move is checked for legality.
        The selected piece is then moved and the associated variables are updated.

        Args:
            self: The instance of the Game class.

        Returns: A string announcing the winner if the game is over, otherwise None
            
        """
        piece_selected = False
        to_move_position = ()
        destination_selected = False
        piece = None
        destination = None
        moved = False
        castled = False
        print(self)
        while not moved:
            while not (destination_selected and piece_selected):
                piece_selected = False
                color = BLACK
                if self.white_turn:
                    color = WHITE
                # Loop to insure a piece is properly selected to move
                while not piece_selected:
                    to_move_input = input(f"It is {color}'s turn. Enter the location of the piece you would like to move: ")
                    try:
                        to_move_position = (FILES[to_move_input[0].upper()], int(to_move_input[1]))
                        temp_piece = self.board[to_move_position[0]][to_move_position[1]]
                        if not (isinstance(temp_piece, Piece) and temp_piece.team == color):
                            print("Invalid location, try again!")
                            continue
                        else:
                            piece = temp_piece
                            piece_selected = True
                    except:
                        print("Invalid input, try again!")
                        continue

                # Loop to insure a destination is properly selected to move to
                destination_selected = False
                print(f"{color}'s {piece.__class__.__name__} at {to_move_input[0].upper()}{to_move_position[1]} selected, Enter the location of square you would like to move to:\n" +
                "(Enter 'R' to change selected piece)")
                while not destination_selected:
                    move_to_input = input()
                    try:
                        if move_to_input == "R" or move_to_input == "r":
                            # Break out of destination selection and return to piece selection
                            break
                        move_to_position = (FILES[move_to_input[0].upper()], int(move_to_input[1]))
                        # Check if the King is attempting to castle
                        if isinstance(piece, King) and isinstance(self.board[move_to_position[0]][move_to_position[1]], Rook) and self.board[move_to_position[0]][move_to_position[1]].team == piece.team:
                            if piece.team == WHITE:
                                other_team = BLACK
                            else:
                                other_team = WHITE

                            if move_to_position[0] == 1 and not (self.is_checked(other_team, 3,move_to_position[1]) or self.is_checked(other_team, 4,move_to_position[1]) or self.is_checked(other_team, 5,move_to_position[1])) and not isinstance(self.board[2][move_to_position[1]], Piece) and not isinstance(self.board[3][move_to_position[1]], Piece) and not isinstance(self.board[4][move_to_position[1]], Piece):
                                castled = piece.can_castle(True)
                                print(castled)
                                if not self.white_turn:
                                    self.black_king_pos = (3, move_to_position[1])
                                else:
                                    self.white_king_pos = (3, move_to_position[1])
                                return False
                            elif move_to_position[0] == 8 and not (self.is_checked(other_team, 5,move_to_position[1]) or self.is_checked(other_team, 6,move_to_position[1]) or self.is_checked(other_team, 7,move_to_position[1])) and not isinstance(self.board[6][move_to_position[1]], Piece) and not isinstance(self.board[7][move_to_position[1]], Piece):
                                castled = piece.can_castle(False)
                                print(castled)
                                if not self.white_turn:
                                    self.black_king_pos = (7, move_to_position[1])
                                else:
                                    self.white_king_pos = (7, move_to_position[1])
                                return False
                            else:
                                print("Cannot castle!")
                        elif piece.can_move_to(move_to_position[0], move_to_position[1]):
                            destination = move_to_position
                            destination_selected = True
                        else:
                            print(f"{piece.__class__.__name__} at {to_move_input[0].upper()}{to_move_position[1]} cannot move to {move_to_input[0].upper()}{move_to_position[1]}, try again!")
                    except Exception as e:
                        print(f"Invalid input, try again! {e}")
                        continue
                if not destination_selected:
                    continue
            

            temp_board = copy.deepcopy(self.board)
            wk_pos = self.white_king_pos
            bk_pos = self.black_king_pos

            out = piece.move_to(destination[0], destination[1])
            if isinstance(piece, King):
                if self.white_turn:
                    wk_pos = destination
                else:
                    bk_pos = destination

            moved = True
            if self.is_checked(WHITE, bk_pos[0], bk_pos[1]):
                if not self.white_turn:
                    print("Cannot do this move. Protect your king!")
                    self.board = temp_board
                    self.black_king_pos = bk_pos
                    piece.file = to_move_position[0]
                    piece.rank = to_move_position[1]
                    # Restart the turn function
                    moved = False
                    destination_selected = False
                    piece_selected = False

                else:
                    if self.is_checkmate(BLACK):
                        return self.winner(WHITE)
                    out += (f"\nBlack's king is checked!")
            if self.is_checked(BLACK, wk_pos[0], wk_pos[1]):
                if self.white_turn:
                    print("Cannot do this move. Protect your king!")
                    self.board = temp_board
                    self.white_king_pos = wk_pos
                    piece.file = to_move_position[0]
                    piece.rank = to_move_position[1]
                    # Restart the turn function
                    moved = False
                    destination_selected = False
                    piece_selected = False
                else:
                    if self.is_checkmate(WHITE):
                        return self.winner(BLACK)
                    out += (f"\nWhite's king is checked!")
        # If piece is a king, update its position
        if isinstance(piece, King):
            if not self.white_turn:
                self.black_king_pos = destination
            else:
                self.white_king_pos = destination
        print(out)

    def is_checked(self, by_team, file_to_check, rank_to_check):
        """
        Checks if the tile at the given position is in check.

        Args:
            self: The instance of the Game class.
            by_team: The team of the pieces to check for attacks (e.g., "WHITE", "BLACK").
            file_to_check: The file (column) coordinate of the tile to check.
            rank_to_check: The rank (row) coordinate of the tile to check.

        Returns:
            True if the tile at the given position is in check by the specified team, False otherwise.
        """
        for file in range(1,9):
            for rank in range(1,9):
                square = self.board[file][rank]
                if isinstance(square, Piece) and square.team == by_team and square.can_move_to(file_to_check, rank_to_check):
                    return True
        return False

    def is_checkmate(self, team):
        """
        Checks if the given team is in checkmate.

        Args:
            self: The instance of the Game class.
            team: The team to check for checkmate (e.g., "WHITE", "BLACK").

        Returns:
            True if the given team is in checkmate, False otherwise.
        """
        for file in range(1,9):
            for rank in range(1,9):
                square = self.board[file][rank]
                if isinstance(square, Piece) and square.team == team:
                    if self.any_valid_move(square):
                        return False
        print("CHECKMATE")
        return True
    
    
    def any_valid_move(self, piece: Piece):
        """
        Checks if the given piece has any legal moves available.

        Args:
            self: The instance of the Game class.
            piece: The Piece object to check for valid moves.

        Returns:
            True if the piece has at least one legal move, False otherwise.
        """
        if piece.team == WHITE:
            other_team = BLACK
            king_pos = self.white_king_pos
        else:
            other_team = WHITE
            king_pos = self.black_king_pos
        for file in range(1,9):
            for rank in range(1,9):
                # Determine if this move can save the king

                # Store the location of the piece we are testing so we can undo the move later
                temp_file = piece.file
                temp_rank = piece.rank

                if piece.can_move_to(file, rank):
                    temp_board = copy.deepcopy(self.board)
                    # Update the kings position if it moves
                    if isinstance(piece, King):
                        pos_to_test = (file, rank)
                    else:
                        pos_to_test = king_pos

                    piece.move_to(file, rank)
                    self.board[file][rank] = piece
                    
                    if not self.is_checked(other_team, pos_to_test[0], pos_to_test[1]):
                        self.board = temp_board
                        print(f"HINT! {piece.__class__.__name__} to {I_FILES[file]}{rank} can save you!")
                        return True
                    
                    self.board = temp_board
                    piece.file = temp_file
                    piece.rank = temp_rank

        return False

    def promote(self, piece: Piece, choice):
        """
        Promotes a pawn to the chosen piece.

        Args:
            self: The instance of the Game class.
            piece: The Pawn object to be promoted.
            choice: The character representing the chosen piece (Q for Queen, B for Bishop, R for Rook, K for Knight).

        Returns:
            Replaces the Pawn object on the board with the chosen piece. Prints a message indicating the successful promotion.
        """
        if choice.upper() == "Q":
            self.board[piece.file][piece.rank] = Queen(piece.game, piece.file, piece.rank, piece.square_colored, piece.team)
            msg = "Queen"
        elif choice.upper() == "B":
            self.board[piece.file][piece.rank] = Bishop(piece.game, piece.file, piece.rank, piece.square_colored, piece.team)
            msg = "Bishop"
        elif choice.upper() == "R":
            self.board[piece.file][piece.rank] = Rook(piece.game, piece.file, piece.rank, piece.square_colored, piece.team)
            msg = "Rook"
        else:
            self.board[piece.file][piece.rank] = Knight(piece.game, piece.file, piece.rank, piece.square_colored, piece.team)
            msg = "Knight"
        print(f"Pawn at {I_FILES[piece.file]}{piece.rank} promoted to a {msg}!")
    
    def winner(self, team):
        """
        Returns a string announcing the winner of the game.

        Args:
            self: The instance of the Game class.
            team: The team that has won the game (e.g., "WHITE", "BLACK").

        Returns:
            A string announcing the winner and the number of moves played.
        """
        return (f"{team} is the winner after {self.turn_number} moves!")

            
    def make_board(self):
        """
        Creates and initializes the chessboard.

        This function sets up the initial board state with all pieces 
        in their starting positions.

        Args:
            self: The instance of the Game class.

        Returns:
            A 2D list representing the chessboard, where each element is either a Piece object or a Square object.
        """
        # Board will use accurate rank/file numbers, therefore the 0 rank and 0 file exist as 'None' but are not used
        board = [[None for i in range(0,9)] for j in range(0,9)]

        # Build white's back row
        board [1][1] = Rook(self, 1, 1, True, WHITE)
        board [2][1] = Knight(self, 2, 1, False, WHITE)
        board [3][1] = Bishop(self, 3, 1, True, WHITE)
        board [4][1] = Queen(self, 4, 1, False, WHITE)
        board [5][1] = King(self, 5, 1, True, WHITE)
        board [6][1] = Bishop(self, 6, 1, False, WHITE)
        board [7][1] = Knight(self, 7, 1, True, WHITE)
        board [8][1] = Rook(self, 8, 1, False, WHITE)

        # Build white's pawn row
        color = False
        for i in range(1,9):
            board[i][2] = Pawn(self, i, 2, color, WHITE)
            color = not color
        
        # Build the empty middle section
        for rank in range (3, 8):
            color = not color
            for file in range(1, 9):
                board[file][rank] = Square(self, file, rank, color)
                color = not color
        
        # Build black's pawn row
        color = True
        for i in range(1,9):
            board[i][7] = Pawn(self, i, 7, color, BLACK)
            color = not color

        # Build black's back row
        board [1][8] = Rook(self, 1, 8, False, BLACK)
        board [2][8] = Knight(self, 2, 8, True, BLACK)
        board [3][8] = Bishop(self, 3, 8, False, BLACK)
        board [4][8] = Queen(self, 4, 8, True, BLACK)
        board [5][8] = King(self, 5, 8, False, BLACK)
        board [6][8] = Bishop(self, 6, 8, True  , BLACK)
        board [7][8] = Knight(self, 7, 8, False, BLACK)
        board [8][8] = Rook(self, 8, 8, True, BLACK)

        return board

# Game initialization
game = Chess()
game.play()