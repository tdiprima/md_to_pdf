import argparse
import logging
import sys
from pathlib import Path

from converter import convert_directory

LOG_LEVEL = __import__("os").environ.get("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert all *.md files in a directory to PDF.")
    parser.add_argument("input_dir", help="Directory containing .md files")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for output PDFs (default: same as input_dir)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_dir = Path(args.input_dir).resolve()
    if not input_dir.is_dir():
        logger.error("Not a directory: %s", input_dir)
        sys.exit(1)

    output_dir = Path(args.output_dir).resolve() if args.output_dir else input_dir

    pdfs = convert_directory(input_dir, output_dir)
    if not pdfs:
        sys.exit(1)


if __name__ == "__main__":
    main()
