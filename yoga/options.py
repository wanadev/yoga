DEFAULT_OPTIONS = {
        "verbose": False,
        "quiet": False,
        }


def normalize_options(options=None):
    if not options:
        return dict(DEFAULT_OPTIONS)

    result = dict(DEFAULT_OPTIONS)

    for key in {"verbose", "quiet"}:
        if key in options:
            result[key] = options[key]

    # Quiet takes precedence over verbose
    if result["quiet"]:
        result["verbose"] = False

    return result
