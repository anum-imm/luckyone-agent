import base64

def is_base64_image(data: str) -> bool:
    try:
        decoded = base64.b64decode(data)
        return decoded.startswith(b"\x89PNG")
    except Exception:
        return False
