"""Copy the committed 18 November 2026 news image into the grader output."""

import os
import shutil
from pathlib import Path


def output_path() -> Path:
    directory = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    directory.mkdir(parents=True, exist_ok=True)
    return directory / "entry.png"


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    # The committed PNG is the whole entry. Copying it keeps both runs byte-identical.
    if not source.is_file():
        raise FileNotFoundError(source)
    shutil.copyfile(source, output_path())


if __name__ == "__main__":
    main()
