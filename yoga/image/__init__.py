import io

from PIL import Image
import pyguetzli
import zopfli

from .options import normalize_options


def optimize(input_file, output_file, options={}):
    options = normalize_options(options)

    image = Image.open(input_file)

    if options["output_format"] == "orig" and image.format not in ("JPEG", "PNG"):                      # noqa
        raise ValueError("The input image must be a JPEG or a PNG when setting 'output_format' to 'orig'")    # noqa

    if not hasattr(output_file, "write"):
        output_file = open(output_file, "wb")

    # resize
    if options["resize"] != "orig":
        image.thumbnail(options["resize"], Image.LANCZOS)

    # output format
    output_format = None

    if options["output_format"] == "orig":
        output_format = image.format.lower()
    elif options["output_format"] in ("jpeg", "png"):
        output_format = options["output_format"]
    else:  # auto
        raise NotImplementedError()

    # convert / optimize
    output_image_bytes = None
    if output_format == "jpeg":
        output_image_bytes = pyguetzli.process_pil_image(
                image, int(options["jpeg_quality"] * 100))
    else:
        pass
        image_io = io.BytesIO()
        image.save(image_io, format="PNG", optimize=False)
        image_io.seek(0)
        image_bytes = image_io.read()

        # Optimize using zopflipng
        zopflipng = zopfli.ZopfliPNG()
        zopflipng.lossy_8bit = True
        zopflipng.lossy_transparent = True
        zopflipng.filter_strategies = "01234mepb"
        zopflipng.iterations = 20
        zopflipng.iterations_large = 7
        output_image_bytes = zopflipng.optimize(image_bytes)

    # write to output_file
    output_file.write(output_image_bytes)
