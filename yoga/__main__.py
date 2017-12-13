import sys

from . import cli
from . import image  # noqa
from . import model  # noqa


def main():
    parser = cli.generate_main_cli()
    args = parser.parse_args(sys.argv[1:])
    handler = getattr(sys.modules[__name__], args.subcommand)
    handler.optimize(args.input, args.output, vars(args))


if __name__ == "__main__":
    main()
