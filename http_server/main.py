"""
* TODO:
    * Setup socket for listening
    * Recieve request
    * Parse request
    * Find resource
    * Send response
"""

import socket
import sys
import os

HOST: str = "127.0.0.1"
DEFAULTPORT: int = 28333
ENCODING: str = "iso-8859-1"
BUFFER: int = 4096
CRLF: str = "\r\n"
CRLF_B: bytes = CRLF.encode(ENCODING)
DOCROOT = os.path.abspath(".")


def get_port() -> int | None:
    port: int = DEFAULTPORT
    try:
        custom_port = sys.argv[1]
        if custom_port:
            port = int(custom_port)
    except ValueError:
        err_msg = f"Invalid port number given. Using default port: {DEFAULTPORT}"
        raise ValueError(err_msg)
    return port


def setup(port: int):
    try:
        listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 6)
    except Exception as e:
        print(f"Error: {e}")

    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind((HOST, port))

    return listen_sock


def handle_request(listen_sock, port):
    listen_sock.listen()

    print("=" * 10 + f" Server listening on port: {port} " + "=" * 10)

    while True:
        client_con = listen_sock.accept()
        client_sock = client_con[0]

        request: bytes = b""
        while True:
            data = client_sock.recv(BUFFER)
            request += data
            if CRLF_B in request:
                break

    return request


def _get_mrp(line: str) -> tuple[str, str, str]:
    """
    Extract method, resource, and protocol from an HTTP request line

    Example: "GET /index.html HTTP/1.1" -> ("GET", "/index.html", "HTTP/1.1")

    Raises:
        ValueError: If the line does not contain exactly three space-separated parts
    """
    parts = line.strip().split(" ", 2)
    if len(parts) != 3:
        raise ValueError(f"Invalid HTTP request line: {line!r}")
    return tuple(parts)


def _map_header_fields(header_lines: list[str]) -> dict:
    header_fields: dict = {}
    for line in header_lines:
        try:
            _key, _val = line.split(":", 1)
        except ValueError:
            continue

        key = _key.strip()
        val = _val.strip()

        if key and val:
            header_fields[key] = val

    return header_fields


def parse_header(header_b: bytes) -> dict:
    print("\n\n")
    header: str = header_b.decode(ENCODING)
    header_lines = header.split(CRLF)

    header_dict: dict = {}
    header_fields: dict = {}

    mrp: tuple[str, str, str] = _get_mrp(header_lines[0])
    header_fields: dict = _map_header_fields(header_lines[1:])

    header_dict["method"] = mrp[0]
    header_dict["resource"] = mrp[1]
    header_dict["protocol"] = mrp[2]
    header_dict["fields"] = header_fields

    return header_dict


def main():
    port: int = get_port()
    listen_sock = setup(port)

    listen_sock.listen()
    print("=" * 10 + f" Server listening on port: {port} " + "=" * 10)

    while True:
        client_conn = listen_sock.accept()
        client_sock = client_conn[0]

        request: bytes = b""
        while True:
            data = client_sock.recv(BUFFER)
            request += data
            if CRLF_B in request:
                break

        parts = request.split(CRLF_B + CRLF_B, 1)
        if len(parts) != 2:
            raise ValueError("Malformed request: missing header-body separator")

        header, payload = parts
        header_data: dict = parse_header(header)  # Ignore payload for now

        for k, v in header_data.items():
            print(f"{k}: {v}")

        res: str = (
            "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 16\r\nConnection: close\r\n\r\nHello"
        )
        client_sock.send(res.encode(ENCODING))
        client_sock.close()


if __name__ == "__main__":
    main()
