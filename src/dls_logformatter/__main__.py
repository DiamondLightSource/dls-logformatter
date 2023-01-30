import json
import logging
from argparse import ArgumentParser

from dls_logformatter.dls_logformatter import DlsLogformatter
from dls_logformatter.version import meta, version


def deep3():
    raise RuntimeError("error in deep3")


def deep2():
    deep3()


def deep1():
    deep2()


def example(format_type: str) -> None:
    # Make handler which writes the logs to console.
    handler = logging.StreamHandler()

    # Make the formatter from this library.
    dls_logformatter = DlsLogformatter(format_type)

    # Let handler write the custom formatted messages.
    handler.setFormatter(dls_logformatter)

    # Let root logger use the handler.
    logging.getLogger().addHandler(handler)

    # Let debug output show also.
    logging.getLogger().setLevel(logging.DEBUG)

    logging.warning("this is a warning message")
    logging.info("this is an info message")
    logging.info("this is a debug message")

    try:
        deep1()
    except Exception as exception:
        logging.error("this is an error message", exc_info=exception)

    # Remove the handler from the logging system.
    logging.getLogger().removeHandler(handler)


def get_parser():
    parser = ArgumentParser(
        description="Command line accompanying the dls-logformatter library."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=version(),
        help="Print version string.",
    )
    parser.add_argument(
        "--version-json",
        action="store_true",
        help="Print version stack in json.",
    )
    parser.add_argument(
        "--example",
        choices=["long", "short", "bare"],
        help="Print some example output.",
    )
    return parser


def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    if args.version_json:
        print(json.dumps(meta(), indent=4))

    if args.example is not None:
        example(args.example)


if __name__ == "__main__":
    main()
