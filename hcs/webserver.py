"""
1. Get a socket 
2. Bind the socket to a port 
3. Listen for connections 
4. Recieve request 
5. Send response 
6. Handle new connections
"""

import socket
import sys

HOST: str = "127.0.0.1"
PORT: int = 8080


def main():
    res: str = (
        "HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: 16\nConnection: close\r\n\r\nHello"
    )

    try:
        listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 6) or None
        listen_sock.bind((HOST, PORT))
    except Exception as e:
        print(f"Error: {e}")
    finally: 
        if sock:
            sock.close()


if __name__ == "__main__":
    main()
