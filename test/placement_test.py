from typing import List

import pytest

from lib.shared.gamerules import Gamerules
from lib.shared.internal_structures import Board, Placement, Tile, TileColor, TileShape
from lib.shared.player import Player


@pytest.mark.parametrize(
    ("board", "placements", "result"),
    [
        (Board(), [Placement(Tile(TileColor.BLUE, TileShape.DIAMOND), 110, 110)], True),
        (
            Board(),
            [
                Placement(Tile(TileColor.BLUE, TileShape.DIAMOND), 110, 110),
                Placement(Tile(TileColor.BLUE, TileShape.SQUARE), 110, 111),
            ],
            True,
        ),
        (
            Board(),
            [
                Placement(Tile(TileColor.BLUE, TileShape.DIAMOND), 110, 110),
                Placement(Tile(TileColor.RED, TileShape.SQUARE), 110, 111),
            ],
            False,
        ),
    ],
)
def test_move(board: Board, placements: List[Placement], result: bool):
    rule = Gamerules()
    assert result == rule.verify_move(placements, board)


@pytest.mark.parametrize(
    "placements, result",
    [
        (
            [
                Placement(Tile(TileColor.BLUE, TileShape.SQUARE), 110, 111),
                Placement(Tile(TileColor.BLUE, TileShape.CLUB), 110, 109),
            ],
            True,
        ),
        (
            [
                Placement(Tile(TileColor.BLUE, TileShape.SQUARE), 110, 109),
                Placement(Tile(TileColor.RED, TileShape.SQUARE), 111, 109),
            ],
            True,
        ),
        (
            [
                Placement(Tile(TileColor.BLUE, TileShape.DIAMOND), 109, 109),
                Placement(Tile(TileColor.RED, TileShape.DIAMOND), 109, 108),
            ],
            False,
        ),
        (
            [
                Placement(Tile(TileColor.BLUE, TileShape.CLUB), 110, 109),
                Placement(Tile(TileColor.BLUE, TileShape.CROSS), 110, 108),
            ],
            True,
        ),
        (
            [
                Placement(Tile(TileColor.RED, TileShape.CLUB), 111, 109),
                Placement(Tile(TileColor.RED, TileShape.CROSS), 111, 111),
            ],
            True,
        ),
        (
            [
                Placement(Tile(TileColor.BLUE, TileShape.DIAMOND), 109, 110),
            ],
            False,
        ),
    ],
    ids=repr,
)
def test_complex_move(placements: List[Placement], result: bool):
    board = Board()
    board.add_tile(Placement(Tile(TileColor.BLUE, TileShape.DIAMOND, False), 110, 110))
    board.add_tile(Placement(Tile(TileColor.RED, TileShape.DIAMOND, False), 111, 110))
    board.add_tile(
        Placement(Tile(TileColor.ORANGE, TileShape.DIAMOND, False), 112, 110)
    )
    board.add_tile(Placement(Tile(TileColor.GREEN, TileShape.DIAMOND, False), 113, 110))
    board.add_tile(
        Placement(Tile(TileColor.YELLOW, TileShape.DIAMOND, False), 114, 110)
    )
    board.add_tile(
        Placement(Tile(TileColor.VIOLET, TileShape.DIAMOND, False), 115, 110)
    )
    rule = Gamerules()
    assert result == rule.verify_move(placements, board)


def test_game_over():
    board = Board()
    bag = list()
    colors = list(TileColor)
    shapes = list(TileShape)
    players = [Player(), Player()]
    for i in range(6):
        for j in range(6):
            board.add_tile(
                Placement(Tile(colors[i], shapes[i], temp=False), 110 + i, 110 + j)
            )
            bag.append(Tile(colors[i], shapes[j]))
        for player in players:
            player[i] = Tile(colors[i], shapes[i])
    rule = Gamerules()

    assert rule.game_over(players, board, bag)
