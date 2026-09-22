from pathlib import Path
from xml.sax.saxutils import escape
import cairosvg

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "site" / "docs"
OUTPUT = DOCS / "assets" / "ogp"
TEMPLATE = "ogp-template.svg"


def get_title(markdown):
    text = markdown.read_text(encoding="utf-8")

    for line in text.splitlines():
        line = line.strip()

        if line.startswith("# "):
            return line[2:].strip()

    return markdown.stem


def main():
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"Template not found: {TEMPLATE}")

    template = TEMPLATE.read_text(encoding="utf-8")

    for markdown in DOCS.rglob("*.md"):
        relative = markdown.relative_to(DOCS)

        name = relative.with_suffix("").as_posix()

        destination = OUTPUT / f"{name}.png"

        title = escape(get_title(markdown))
        svg = template.replace("{{TITLE}}", title)

        destination.parent.mkdir(parents=True, exist_ok=True)

        cairosvg.svg2png(
            bytestring=svg.encode("utf-8"),
            write_to=str(destination),
        )

        print(f"{markdown} -> {destination}")


if __name__ == "__main__":
    main()
