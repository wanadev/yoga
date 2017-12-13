from .options import normalize_options


def optimize(input_file, output_file, options={}):
    options = normalize_options(options)
    # TODO input_file -> string (path), bytes, file-like
    # TODO output_file -> string (path), file-like
    raise NotImplementedError()  # TODO
