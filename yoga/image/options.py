import re


# fmt: off
DEFAULT_OPTIONS = {
    "output_format": "orig",         # orig|auto|jpeg|png|webp|webpl
    "resize": "orig",                # orig|[w,h]
    "jpeg_quality": 0.84,            # 0.00-1.00
    "webp_quality": 0.90,            # 0.00-1.00
    "opacity_threshold": 254,        # 0-255
    "png_slow_optimization": False,  # True|False
}
# fmt: on


_RESIZE_OPTION_REGEXP = re.compile(
    r"^([0-9]+)[x\s:,;]([0-9]+)$", flags=re.IGNORECASE
)


def normalize_options(options=None):
    if not options:
        return dict(DEFAULT_OPTIONS)

    result = dict(DEFAULT_OPTIONS)

    # "PNG" -> "png" (lower case)
    # "jpg" -> "jpeg"
    if "output_format" in options:
        value = options["output_format"].lower()

        if value == "jpg":
            value = "jpeg"

        if value not in ("orig", "auto", "jpeg", "png", "webp", "webpl"):
            raise ValueError("Invalid value for 'output_format': '%s'" % value)

        result["output_format"] = value

    # "ORIG"    -> "orig" (lower case)
    # 512       -> [512, 512]
    # "512"     -> [512, 512]
    # "512x512" -> [512, 512]
    # "512X512" -> [512, 512]
    # "512 512" -> [512, 512]
    # "512:512" -> [512, 512]
    # "512,512" -> [512, 512]
    # "512;512" -> [512, 512]
    if "resize" in options:
        value = options["resize"]

        if type(value) == bytes:
            value = value.decode()

        if type(value) in (str, bytes):
            value = value.lower()

            if value.isdigit():
                value = int(value)
            elif _RESIZE_OPTION_REGEXP.match(value):
                match = _RESIZE_OPTION_REGEXP.match(value)
                value = [
                    int(match.group(1)),
                    int(match.group(2)),
                ]
            elif value != "orig":
                raise ValueError("Invalid value for 'resize': %s" % value)

        if type(value) in (int, float):
            value = [value, value]

        result["resize"] = value

    # 0-100 -> 0.00-1.00
    # 110   -> 1.00
    # "100" -> 1.00
    if "jpeg_quality" in options:
        value = options["jpeg_quality"]

        if type(value) in (str, bytes):
            value = float(value)

        if value > 1:
            value = value / 100.0

        if value > 1:
            value = 1

        result["jpeg_quality"] = value

    # 0-100 -> 0.00-1.00
    # 110   -> 1.00
    # "100" -> 1.00
    if "webp_quality" in options:
        value = options["webp_quality"]

        if type(value) in (str, bytes):
            value = float(value)

        if value > 1:
            value = value / 100.0

        if value > 1:
            value = 1

        result["webp_quality"] = value

    # 0.00-1.00[ -> 0-255
    # 300        -> 255
    # "100"      -> 100
    if "opacity_threshold" in options:
        value = options["opacity_threshold"]

        if type(value) in (str, bytes):
            value = float(value)

        if value < 1:
            value = value * 255

        if value > 255:
            value = 255

        result["opacity_threshold"] = round(value)

    # "" -> False
    # 0 -> False
    # 1 -> True
    if "png_slow_optimization" in options:
        result["png_slow_optimization"] = bool(
            options["png_slow_optimization"]
        )

    return result
