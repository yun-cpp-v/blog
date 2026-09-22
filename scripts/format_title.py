from PIL import ImageFont
from sudachipy import Dictionary, SplitMode


def text_width(text: str, font: ImageFont.FreeTypeFont) -> int:
    box = font.getbbox(text)
    return box[2] - box[0]


tokenizer = Dictionary().create()


# 行頭禁則文字
BAD_LINE_START = set("、。，．！？!?)]）］】」』〉》〕｝")

# 行末禁則文字
BAD_LINE_END = set("([（［【「『〈《〔｛")

# 句読点類
GOOD_BREAK_AFTER = set("、。，．！？!?：:；;")

# 括弧類
BRACKETS = {
    "(": ")",
    "（": "）",
    "[": "]",
    "［": "］",
    "【": "】",
    "「": "」",
    "『": "』",
    "〈": "〉",
    "《": "》",
    "〔": "〕",
    "｛": "｝",
}


def split_japanese_title(title: str, font: ImageFont.FreeTypeFont) -> str:

    if not title:
        return title

    # 形態素解析

    tokens = list(tokenizer.tokenize(title, SplitMode.C))

    if len(tokens) < 2:
        return title

    # 改行候補を作る

    candidates = []

    position = 0

    for i, token in enumerate(tokens[:-1]):
        position += len(token.surface())

        candidates.append(
            {
                "position": position,
                "left": token,
                "right": tokens[i + 1],
            }
        )

    # スコア

    def score(candidate) -> float:

        split = candidate["position"]

        left = title[:split]
        right = title[split:]

        left_token = candidate["left"]
        right_token = candidate["right"]

        score = 0.0

        # 行幅

        left_width = text_width(left, font)
        right_width = text_width(right, font)

        total_width = left_width + right_width

        balance = abs(left_width - right_width) / total_width

        score -= balance * 40

        # 禁則処理

        if right[0] in BAD_LINE_START or left[-1] in BAD_LINE_END:
            score -= 1000

        # 句読点の後

        if left[-1] in GOOD_BREAK_AFTER:
            score += 50

        # 形態素の品詞

        left_pos = left_token.part_of_speech()[0]
        right_pos = right_token.part_of_speech()[0]

        # 助詞の直後

        if left_pos == "助詞":

            surface = left_token.surface()

            if surface == "と":
                # 「Aと\nB」は比較的自然なので加点
                score += 15
            else:
                score -= 25

        # 助動詞の直後

        if left_pos == "助動詞":
            score -= 40

        # 行頭が助詞・助動詞

        if right_pos in {"助詞", "助動詞"}:
            score -= 100

        # 連続する名詞の間で切るのを避ける

        if left_pos == "名詞" and right_pos == "名詞":
            score -= 35

        # 文節的にまとまっている候補を評価

        if left_pos == "助詞":

            surface = left_token.surface()

            if surface in {"は", "が", "を", "に", "へ", "と", "で", "から", "まで", "より", "も", "や", "って"}:
                score += 30

        # 英数字の途中で切らない

        if left[-1].isascii() or left[-1].isalnum():
            if right[0].isascii() or right[0].isalnum():
                score -= 1000

        #  括弧

        for opening, closing in BRACKETS.items():
            if left.count(opening) > left.count(closing):
                score -= 100

        # 極端に短い行

        if len(left) <= 2:
            score -= 100

        if len(right) <= 2:
            score -= 100

        return score

    best = max(candidates, key=score)

    split = best["position"]

    return title[:split] + "\n" + title[split:]


def format_title(title: str, font: ImageFont.FreeTypeFont, max_width: int) -> str:

    if text_width(title, font) <= max_width:
        return title

    result = split_japanese_title(title, font)

    for line in result.splitlines():
        if text_width(line, font) <= max_width:
            continue
        raise ValueError("Title does not fit within the specified width " "even when split into two lines.")

    return result
