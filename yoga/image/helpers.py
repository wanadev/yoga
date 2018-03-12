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


def guess_image_format(image_initial_bytes):
    if image_initial_bytes.startswith(b"\xFF\xD8\xFF\xE0"):
        return "jpeg"
    elif image_initial_bytes.startswith(b"\x89PNG\r\n"):
        return "png"
    else:
        raise ValueError("Unsupported image format")
