"""
1. Perform DNS
    1. `socket.getaddrinfo()` performs name service resolution 
    2. Maps both ip address and port
2. Create a socket 
    1. Specify it's an internet socket 
    2. Specify transport layer protocol 
3. Sends a request
4. Get data
5. Close the socket
* Connection close automatically after sending data
"""

"""
* Include:
    * A method for saving response to file
        * Add flags to specify saving format 
            * bin
            * pcap
            * json
        * Default to bin
    * Send payloads with request
"""

"""
* Issues:
    1. Value conflict for 'hostname'
        * If 'hotname' is a website name DNS finds the IP address 
        * Hence value of 'hostname' can be used for 'Host' HTTP header 
        * If 'hostname' is an IP address it cannot be used (ex: localhost)
"""

import socket 
import sys

ENCODING: str = "ISO 8859-1"
BUFFER: int = 4096
ADDR_FAM = socket.AF_INET


def main():
    hostname: str = sys.argv[1]
    service: str = sys.argv[2]
    http_req: str = f"GET / HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
    sock = None

    try:
        addr_info = socket.getaddrinfo(
            hostname,
            service,
            family=socket.AF_INET,
            type=socket.SOCK_STREAM
        )

        for i, (family, sock_type, proto, _, sockaddr) in enumerate(addr_info):
            print(f"Attempt: {i} Connecting to: {sockaddr}")

            sock = socket.socket(family, sock_type, proto)
            sock.connect(sockaddr)
            sock.sendall(http_req.encode(ENCODING))

            output: bytes = b""
            while True:
                http_res = sock.recv(BUFFER)
                if not http_res:
                    break
                output += http_res

            print(output.decode(ENCODING))
            
            if output:
                # Break the loop if a successful connection was made
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sock:
            sock.close()


if __name__ == "__main__":
    main()

