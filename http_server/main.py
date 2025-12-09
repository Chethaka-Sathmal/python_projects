"""
1. Get a socket 
2. Bind the socket to a port 
3. Listen for connections 
4. Recieve request 
5. Send response 
6. Handle new connections
"""

"""
* Check later:
    * How multiple requests are queued
    * What is `setsockopt()`
"""

import socket
import sys
from config import HOST, DEFAULTPORT, BUFFER, ENCODING
from parse import parse_header


def main():
    res: str = (
        "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 16\r\nConnection: close\r\n\r\nHello"
    )
    port: int = DEFAULTPORT
    try:
        custom_port: str = sys.argv[1]
        if custom_port:
            port = int(custom_port)
    except Exception as e:
        pass

    try:
        listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 6) or None
        listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_sock.bind((HOST, port))
        listen_sock.listen()

        print("=" * 10 + f" Server listening on port: {port} " + "=" * 10)
        while True:
            client_con = listen_sock.accept()
            client_sock = client_con[0]

            req: bytes = b""
            while True:
                data = client_sock.recv(BUFFER)
                req += data
                if b"\r\n\r\n" in req:
                    break

            header, payload = req.split(b"\r\n\r\n")
            parse_header(header)

            client_sock.send(res.encode(ENCODING))
            client_sock.close()
    except Exception as e:
        print(f"Error: {e}")
    finally: 
        if listen_sock:
            listen_sock.close()


if __name__ == "__main__":
    main()
