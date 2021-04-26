import sys

from . import cli
from . import image  # noqa
from . import model  # noqa


def main(args=sys.argv[1:]):
    parser = cli.generate_main_cli()
    parsed_args = parser.parse_args(args if args else ["--help"])
    handler = getattr(sys.modules[__name__], parsed_args.subcommand)
    handler.optimize(
        parsed_args.input,
        parsed_args.output,
        options=vars(parsed_args),
        verbose=parsed_args.verbose,
        quiet=parsed_args.quiet,
    )


if __name__ == "__main__":
    main()
