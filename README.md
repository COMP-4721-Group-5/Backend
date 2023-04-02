# 🔶 Qwirkle (Server) 🔷

[![CI](https://github.com/COMP-4721-Group-5/Backend/actions/workflows/ci.yml/badge.svg)](https://github.com/COMP-4721-Group-5/Backend/actions/workflows/ci.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Setup

### Dependencies

After cloning this repository, you should first navigate to the cloned directory and run the following command: ```pip install -r requirements.txt```

### Running the server

Simply run ```python run_server.py```. The server port will be displayed within the terminal.

### Command Line Arguments

```text
options:
  -h, --help         show this help message and exit
  --address ADDRESS  Address to bind the socket
  --port PORT        Port number to bind the socket (default: 1234)
  --players {2,3,4}  Number of players to join this server (default: 2)
```
