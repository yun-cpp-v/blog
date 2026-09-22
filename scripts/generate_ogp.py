from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from format_title import format_title

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "site" / "docs"
TEMPLATE = ROOT / "scripts" / "ogp-template.png"
OUTPUT = DOCS / "assets" / "ogp"

FONT = ROOT / "scripts" / "fonts" / "GenJyuuGothicX-Medium.ttf"

FONT_SIZE = 75
MAX_WIDTH = 1000  # 左右余白100

TEXT_X = 600  # origin-x
TEXT_Y = 355  # origin-y + 40

TEXT_COLOR = "#000000"


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

    if not FONT.exists():
        raise FileNotFoundError(f"Font not found: {FONT}")

    font = ImageFont.truetype(FONT, FONT_SIZE)

    for markdown in DOCS.rglob("*.md"):
        relative = markdown.relative_to(DOCS)
        name = relative.with_suffix("").as_posix()

        destination = OUTPUT / f"{name}.png"
        destination.parent.mkdir(parents=True, exist_ok=True)

        title = format_title(get_title(markdown), font, MAX_WIDTH)

        image = Image.open(TEMPLATE).convert("RGBA")
        draw = ImageDraw.Draw(image)

        draw.multiline_text(
            xy=(TEXT_X, TEXT_Y),
            text=title,
            font=font,
            fill=TEXT_COLOR,
            anchor="mm",  # テキストの中央を座標の原点にする
            align="center",
        )

        image.save(destination, "PNG")

        print(f"{markdown} -> {destination}")


if __name__ == "__main__":
    main()
