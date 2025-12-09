from config import ENCODING, CRLF


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


def _map_header_fields(header_lines: list[str])  -> dict:
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
    header: str = header_b.decode(ENCODING)
    header_lines: list[str] = header.split(CRLF)
    header_dict: dict = {}
    header_fields: dict = {}

    mrp: tuple[str, str, str] = _get_mrp(header_lines[0])
    header_fields: dict = _map_header_fields(header_lines[1:])

    header_dict["method"] = mrp[0]
    header_dict["resource"] = mrp[1]
    header_dict["protocol"] = mrp[2]
    header_dict["fields"] = header_fields

    return header_dict

