"""
1. Get a socket 
2. Bind the socket to a port 
3. Listen for connections 
4. Recieve request 
5. Send response 
6. Handle new connections
"""

"""
* Include:
    * How to queue multiple requests
    * How to handle multiple requests
        * Sequentially 
        * Asynchronously 
    * Set socket options (`setsockopt()`)
"""

import socket
import sys

HOST: str = "127.0.0.1"
PORT: int = 8080
BUFFER: int = 4096
ENCODING: str = "ISO 8859-1"

def main():
    res: str = (
        "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 16\r\nConnection: close\r\n\r\nHello"
    )

    try:
        listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 6) or None
        listen_sock.bind((HOST, PORT))
        listen_sock.listen()

        while True:
            client_con = listen_sock.accept()
            client_sock = client_con[0]

            req: bytes = b""
            while True:
                data = client_sock.recv(BUFFER)
                req += data
                if b"\r\n\r\n" in req:
                    break

            print(req.decode(ENCODING))

            client_sock.send(res.encode(ENCODING))
            client_sock.close()
    except Exception as e:
        print(f"Error: {e}")
    finally: 
        if listen_sock:
            listen_sock.close()


if __name__ == "__main__":
    main()
