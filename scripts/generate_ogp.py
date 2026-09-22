# This code is written by ChatGPT

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SOURCE = ROOT / "scripts" / "dummy.png"
OUTPUT = DOCS / "assets" / "ogp"


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Source image not found: {SOURCE}")

    for markdown in DOCS.rglob("*.md"):
        relative = markdown.relative_to(DOCS)

        # index.md はディレクトリ名を使う
        if relative.name == "index.md":
            name = relative.parent.as_posix()
        else:
            name = relative.with_suffix("").as_posix()

        # docs/index.md → index.png
        if not name:
            name = "index"

        filename = name.replace("/", "_") + ".png"
        destination = OUTPUT / filename

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE, destination)

        print(f"{markdown} -> {destination}")


if __name__ == "__main__":
    main()