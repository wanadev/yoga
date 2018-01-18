from .options import normalize_options, extract_image_options


def optimize(input_file, output_file, options={}):
    model_options = normalize_options(options)
    image_options = extract_image_options(options)

    print(model_options, image_options)

    # TODO input_file -> string (path), bytes, file-like
    # TODO output_file -> string (path), file-like
    raise NotImplementedError()  # TODO
