#!/usr/bin/python3

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
import logging
import socket
from queue import Queue
from typing import Final, List

from lib.backend.Logic_backend import QwirkeleController
from lib.backend.server_components import ClientConnection
from lib.backend.server_components import Request

MIN_PLAYERS: Final[int] = 2
MAX_PLAYERS: Final[int] = 4


def main():
    parser = ArgumentParser(
        description="Qwirkle Server", formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "--address", nargs=1, help="Address to bind the socket", default=""
    )
    parser.add_argument(
        "--port",
        nargs=1,
        help="Port number to bind the socket (default: %(default)d)",
        type=int,
        default=1234,
    )
    parser.add_argument(
        "--players",
        nargs=1,
        help="Number of players to join this server (default: %(default)d)",
        type=int,
        choices=range(MIN_PLAYERS, MAX_PLAYERS + 1),
        default=MIN_PLAYERS,
    )

    args = parser.parse_args()

    address = args.address
    port: int = args.port
    if args.port != 1234:
        port = args.port[0]
    players = args.players

    if port <= 0:
        raise ValueError(f"Invalid port number: {port}")

    logging.basicConfig(
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    logging.info("Starting server...")

    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.bind((address, port))
    logging.info(f"Listening on {address}:{port}")
    sock_server.listen()

    connections: List[ClientConnection] = list()
    request_queue: Queue[Request] = Queue()

    for i in range(players):  # Arbitrary limitation of 2 players for POC
        csock, addr = sock_server.accept()
        logging.info(f"Received connection from {addr}")
        connections.append(ClientConnection(csock, addr, request_queue))

    sock_server.close()

    game_controller = QwirkeleController(connections, request_queue)

    while game_controller.in_game():
        try:
            game_controller.process_request()
        except KeyboardInterrupt:
            logging.critical("Ctrl+C received, exiting.")
            for connection in connections:
                connection.stop_listening()
            break
        except ConnectionError:
            logging.error("Closing all other connections.")
            for connection in connections:
                connection.stop_listening()
            logging.error("Exiting")
            break
        except Exception as ex:
            for connection in connections:
                connection.stop_listening()
            raise ex


if __name__ == "__main__":
    main()
