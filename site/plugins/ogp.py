# This code is written by ChatGPT lol

from pathlib import Path

from mkdocs.plugins import BasePlugin
from PIL import Image, ImageDraw, ImageFont


class OGPPlugin(BasePlugin):

    def on_config(self, config):
        self.site_dir = Path(config["site_dir"])
        return config

    def on_page_context(self, context, page, config, nav):
        title = page.title or config["site_name"]

        filename = self.filename_for(page)
        output = self.site_dir / "assets" / "ogp" / filename

        self.generate(title, output)

        context["ogp_image"] = (
            config["site_url"].rstrip("/")
            + "/assets/ogp/"
            + filename
        )

        return context

    def filename_for(self, page):
        url = page.url.rstrip("/")
        return (url.replace("/", "_") or "index") + ".png"

    def generate(self, title, output):
        width = 1200
        height = 630

        image = Image.new(
            "RGB",
            (width, height),
            (248, 247, 252),
        )

        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(
            "NotoSansCJK-Regular.ttc",
            64,
        )

        small_font = ImageFont.truetype(
            "NotoSansCJK-Regular.ttc",
            32,
        )

        draw.text(
            (80, 220),
            title,
            fill=(40, 40, 45),
            font=font,
        )

        draw.text(
            (80, 500),
            "ゆんのブログ",
            fill=(40, 40, 45),
            font=small_font,
        )

        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output)