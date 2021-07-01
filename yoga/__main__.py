import os
import sys
import signal
from concurrent.futures import ThreadPoolExecutor

from . import cli
from . import image  # noqa
from . import model  # noqa


def main(args=sys.argv[1:]):
    parser = cli.generate_main_cli()
    parsed_args = parser.parse_args(args if args else ["--help"])
    handler = getattr(sys.modules[__name__], parsed_args.subcommand)
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(
            handler.optimize,
            parsed_args.input,
            parsed_args.output,
            options=vars(parsed_args),
            verbose=parsed_args.verbose,
            quiet=parsed_args.quiet,
        )
    if future.exception():
        print(future.result())
        sys.exit(1)


def _on_sigint_received(signalnum, stackframe):
    print("Optimization canceled")
    os.kill(os.getpid(), signal.SIGTERM)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, _on_sigint_received)
    main()
