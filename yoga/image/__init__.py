from PIL import Image

from .options import normalize_options


def optimize(input_file, output_file, options={}):
    options = normalize_options(options)

    input_image = Image.open(input_file)

    if options["output_format"] == "orig" and input_image.format not in ("JPEG", "PNG"):                      # noqa
        raise ValueError("The input image must be a JPEG or a PNG when setting 'output_format' to 'orig'")    # noqa

    if not hasattr(output_file, "write"):
        output_file = open(output_file, "wb")

    # resize
    # TODO

    # output format
    output_format = None

    if options["output_format"] == "orig":
        output_format = input_image.format.lower()
    elif options["output_format"] in ("jpeg", "png"):
        output_format = options["output_format"]
    else:  # auto
        raise NotImplementedError()

    # convert / optimize
    # TODO

    # write to output_file
    input_image.save(output_file, format=output_format)  # FIXME
