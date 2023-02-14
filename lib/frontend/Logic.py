from typing import List

from ..shared.internal_structures import Board, Placement, Tile, TileColor, TileShape
from ..shared.player import Player
from ..shared import gamerules


class Logic:
    """ Controls all game logic.

    Responsible for recieving input messages from the player
    and verfiying the validity of the input. Passes the updated
    game state to the socket for transmission to the server
    Recieves game state data from the socket and updates the model
    accordingly. 

    Attributes:
        board: Contains the board
        tempMove: List that contains all temporary placements of current players move
        player: Contains the local player's data 
    """
    __board: Board
    __tempMove: Placement
    __player: Player
    __bag: List[Tile]

    def __init__(self) -> None:
        """Inits the game with one player"""
        self.start_game(1)

    def start_game(self, playerCount: int):
        """Collects playerCount data and sends a message to the socket to start the game

        !!!Right now acting as a temporary method for demo purposes
        Args:
            playerCount: amount of players in the game
        """
        self.__board = Board()
        self.__player = Player()
        self.__bag = list()

        for color in TileColor:
            for shape in TileShape:
                tile = Tile(color, shape, True)
                self.__bag.append(tile)

        temp_hand = []
        for i in range(6):
            temp_hand.append(self.__bag.pop())

        self.__player.update_hand(temp_hand)

    def play_tile(self, placement, index):
        """Plays a tile given an index and desired placement

        Args:
            placement: desired placement of the tile, contains tile, x_coord and y_coord data
            index: index of the tile within the players hand
        """
        self.board.add_tile(placement)
        self.player.play_tile(index)

    def update_board(self, board: Board):
        """Updates the board

        Args:
            board: new board
        """
        self.__board = board

    @property
    def board(self):
        return self.__board

    @property
    def player(self):
        return self.__player