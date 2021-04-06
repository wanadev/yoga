import struct


def image_have_alpha(image, threshold=0xFE):
    if threshold <= 0:
        return False
    # TODO find transparent colors in indexed images (image.mode == "P")
    if image.mode != "RGBA":
        return False
    alpha_band = image.getdata(band=3)  # bands: R=0, G=1, B=2, A=3
    for pix in alpha_band:
        if pix <= threshold:
            return True
    return False


def little_endian_unint32_bytes_to_python_int(bytes_):
    return struct.unpack("<L", bytes_)[0]


def get_riff_structure(data):
    if data[0:4] != b"RIFF":
        raise ValueError("Unvalid RIFF: Not a RIFF file")

    result = {
        "formtype": data[8:12].decode(),
        "size": little_endian_unint32_bytes_to_python_int(data[4:8]),
        "chunks": [],
    }

    if result["size"] + 8 != len(data):
        raise ValueError("Unvalid RIFF: Truncated data")

    offset = 12  # RIFF header length

    while offset < len(data):
        chunk = {
            "type": data[offset : offset + 4].decode(),
            "data_offset": offset + 8,
            "size": little_endian_unint32_bytes_to_python_int(
                data[offset + 4 : offset + 8]
            ),
        }
        result["chunks"].append(chunk)
        offset += 8 + chunk["size"] + chunk["size"] % 2

    return result


def guess_image_format(image_bytes):
    if image_bytes.startswith(b"\xFF\xD8\xFF\xE0"):
        return "jpeg"

    if image_bytes.startswith(b"\x89PNG\r\n"):
        return "png"

    if image_bytes.startswith(b"RIFF"):
        riff = get_riff_structure(image_bytes)
        if riff["formtype"] == "WEBP":
            chunks = [chunk["id"] for chunk in riff["chunks"]]
            if "VP8 " in chunks:
                return "webp"
            if "VP8L" in chunks:
                return "webpl"

    raise ValueError("Unsupported image format")
