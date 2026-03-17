"""算命学（さんめいがく）

干支暦をもとに人体星図（陽占）を作成し、性格・才能・運勢を読み解く。
四柱推命と同じ干支を用いるが、独自の十大主星・十二大従星の体系を持つ。
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult
from utils.kanshi import (
    get_year_kanshi, get_month_kanshi, get_day_kanshi,
    kanshi_to_gogyo, kanshi_to_inyo, get_kuubou,
)
from utils.constants import JIKKAN, JUNISHI, KAN_TO_GOGYO, KAN_TO_INYO

# ── 五行数値順序 ──
GOGYO_ORDER = {"木": 0, "火": 1, "土": 2, "金": 3, "水": 4}

# ── 通変星 → 十大主星マッピング ──
TSUHEN_TO_JUDAI = {
    "比肩": "貫索星",
    "劫財": "石門星",
    "食神": "鳳閣星",
    "傷官": "調舒星",
    "偏財": "禄存星",
    "正財": "司禄星",
    "偏官": "車騎星",
    "正官": "牽牛星",
    "偏印": "龍高星",
    "印綬": "玉堂星",
}

# ── 十大主星の性格記述 ──
JUDAI_DESCRIPTIONS = {
    "貫索星": {
        "keyword": "守備本能の陽（自立・頑固）",
        "personality": "自分の世界観を大切にし、独立心が非常に強い。一度決めたことは最後までやり抜く粘り強さがある。"
                       "自分のペースを崩されることを嫌い、マイペースに物事を進める。職人気質で、専門分野を極める力がある。",
        "strength": "忍耐力・一貫性・専門性",
        "weakness": "頑固さ・孤立しやすさ・融通の利かなさ",
    },
    "石門星": {
        "keyword": "守備本能の陰（協調・社交）",
        "personality": "人との和を大切にし、集団の中で力を発揮する。政治力や交渉力に優れ、人をまとめる才能がある。"
                       "表面的には穏やかだが、内面には強い意志を持つ。ボランティア精神や奉仕の心が厚い。",
        "strength": "協調性・交渉力・人脈構築",
        "weakness": "八方美人・優柔不断・本心が見えにくい",
    },
    "鳳閣星": {
        "keyword": "伝達本能の陽（楽観・自然体）",
        "personality": "おおらかで楽天的、自然体で生きることを好む。食や芸術など五感を楽しむ才能があり、"
                       "表現力が豊か。のんびりとした雰囲気だが、観察力は鋭い。人を和ませるムードメーカー。",
        "strength": "表現力・楽観性・観察力",
        "weakness": "怠惰・計画性の不足・危機感の薄さ",
    },
    "調舒星": {
        "keyword": "伝達本能の陰（繊細・孤高）",
        "personality": "繊細で感受性が豊か。芸術的センスに優れ、独自の美意識を持つ。孤独を恐れず、"
                       "むしろ一人の時間から創造力を生み出す。完璧主義で妥協を許さない。ロマンチスト。",
        "strength": "芸術性・直感力・完璧主義",
        "weakness": "神経質・孤独感・批判的になりやすい",
    },
    "禄存星": {
        "keyword": "引力本能の陽（魅力・奉仕）",
        "personality": "人を惹きつける華やかな魅力がある。面倒見が良く、気前が良い。人に尽くすことで"
                       "自分の存在価値を見出す。愛情深く、誰にでも平等に接する博愛主義者。",
        "strength": "人間的魅力・奉仕精神・愛情深さ",
        "weakness": "浪費・自己犠牲過多・見返りを求めがち",
    },
    "司禄星": {
        "keyword": "引力本能の陰（蓄積・堅実）",
        "personality": "堅実で慎重、コツコツと積み上げる力がある。家庭や身近な人を大切にし、"
                       "安定した生活基盤を築くことに長けている。記憶力が良く、細やかな配慮ができる。",
        "strength": "堅実さ・貯蓄力・家庭的",
        "weakness": "保守的・ケチと見られがち・変化を恐れる",
    },
    "車騎星": {
        "keyword": "攻撃本能の陽（行動・闘争）",
        "personality": "行動力と実行力に溢れ、じっとしていられない性格。正義感が強く、"
                       "不正には真っ向から立ち向かう。スポーツや肉体労働で力を発揮する。単純明快でまっすぐ。",
        "strength": "行動力・正義感・スピード",
        "weakness": "短気・粗暴さ・思慮不足",
    },
    "牽牛星": {
        "keyword": "攻撃本能の陰（名誉・品格）",
        "personality": "プライドが高く、名誉や地位を重んじる。責任感が強く、与えられた役割を"
                       "完璧にこなそうとする。礼儀正しく品格がある。組織の中で上を目指す向上心。",
        "strength": "責任感・品格・向上心",
        "weakness": "プライドの高さ・融通の利かなさ・見栄",
    },
    "龍高星": {
        "keyword": "習得本能の陽（冒険・改革）",
        "personality": "知的好奇心が旺盛で、未知の世界への冒険心がある。型にはまらない発想で"
                       "革新的なアイデアを生み出す。海外や異文化に縁がある。放浪癖とも言える自由さ。",
        "strength": "創造力・冒険心・改革力",
        "weakness": "落ち着きのなさ・飽きっぽさ・破壊的",
    },
    "玉堂星": {
        "keyword": "習得本能の陰（学問・伝統）",
        "personality": "学問や教養を重んじ、知識の探究に喜びを見出す。伝統や古典を大切にし、"
                       "母性的な優しさがある。教育者としての資質に恵まれ、人を導く力がある。",
        "strength": "学識・母性・教育力",
        "weakness": "保守的・理屈っぽさ・古い価値観への固執",
    },
}

# ── 地支の蔵干（主気） ──
ZOUKAN_MAIN = {
    "子": "癸", "丑": "己", "寅": "甲", "卯": "乙",
    "辰": "戊", "巳": "丙", "午": "丁", "未": "己",
    "申": "庚", "酉": "辛", "戌": "戊", "亥": "壬",
}


def _get_tsuhensei(day_kan: str, other_kan: str) -> str:
    """日干と他の干の関係から通変星を算出する。"""
    day_gogyo = GOGYO_ORDER[KAN_TO_GOGYO[day_kan]]
    other_gogyo = GOGYO_ORDER[KAN_TO_GOGYO[other_kan]]
    relation = (other_gogyo - day_gogyo) % 5

    day_idx = JIKKAN.index(day_kan)
    other_idx = JIKKAN.index(other_kan)
    same_polarity = (day_idx % 2) == (other_idx % 2)

    tsuhen_map = {
        (0, True): "比肩", (0, False): "劫財",
        (1, True): "食神", (1, False): "傷官",
        (2, True): "偏財", (2, False): "正財",
        (3, True): "偏官", (3, False): "正官",
        (4, True): "偏印", (4, False): "印綬",
    }
    return tsuhen_map[(relation, same_polarity)]


def _kan_to_judai(day_kan: str, other_kan: str) -> str:
    """日干と他の干から十大主星を算出する。"""
    tsuhen = _get_tsuhensei(day_kan, other_kan)
    return TSUHEN_TO_JUDAI[tsuhen]


def _build_jintai_seizu(
    day_kan: str, month_kan: str, year_kan: str,
    day_shi: str, month_shi: str, year_shi: str,
) -> dict[str, str]:
    """人体星図（陽占）を構築する。

    正しい配置ルール:
        中央: 日干 × 月支蔵干
        北:   日干 × 年干
        南:   日干 × 月干
        東:   日干 × 日支蔵干
        西:   日干 × 年支蔵干
    """
    month_zoukan = ZOUKAN_MAIN.get(month_shi, month_kan)
    day_zoukan = ZOUKAN_MAIN.get(day_shi, day_kan)
    year_zoukan = ZOUKAN_MAIN.get(year_shi, year_kan)

    center = _kan_to_judai(day_kan, month_zoukan)  # 日干 × 月支蔵干
    north = _kan_to_judai(day_kan, year_kan)        # 日干 × 年干
    south = _kan_to_judai(day_kan, month_kan)       # 日干 × 月干
    east = _kan_to_judai(day_kan, day_zoukan)       # 日干 × 日支蔵干
    west = _kan_to_judai(day_kan, year_zoukan)      # 日干 × 年支蔵干

    return {
        "center": center,
        "north": north,
        "south": south,
        "east": east,
        "west": west,
    }


def _build_interpretation(
    jintai: dict[str, str],
    day_kan: str,
    day_gogyo: str,
    day_inyo: str,
    kuubou: tuple[str, ...],
) -> str:
    """算命学の総合解釈テキストを生成する。"""
    lines = []

    lines.append(f"【日干】{day_kan}（{day_gogyo}の{day_inyo}）")
    lines.append("")

    # 人体星図
    lines.append("【人体星図（陽占）】")
    pos_labels = {
        "north": "頭（北）  ",
        "east": "左手（東）",
        "center": "胸（中央）",
        "west": "右手（西）",
        "south": "腹（南）  ",
    }
    display_order = ["north", "east", "center", "west", "south"]
    for pos in display_order:
        star = jintai[pos]
        label = pos_labels[pos]
        lines.append(f"  {label}: {star}")

    lines.append("")

    # 中央星（最も重要）の解説
    center_star = jintai["center"]
    center_info = JUDAI_DESCRIPTIONS.get(center_star, {})
    if center_info:
        lines.append(f"【中心星: {center_star}】")
        lines.append(f"  キーワード: {center_info.get('keyword', '')}")
        lines.append(f"  {center_info.get('personality', '')}")
        lines.append(f"  強み: {center_info.get('strength', '')}")
        lines.append(f"  課題: {center_info.get('weakness', '')}")
        lines.append("")

    # その他の主星
    other_stars = set()
    for pos in ["north", "south", "east", "west"]:
        star = jintai[pos]
        if star != center_star and star not in other_stars:
            other_stars.add(star)
            info = JUDAI_DESCRIPTIONS.get(star, {})
            if info:
                lines.append(f"【{star}】{info.get('keyword', '')}")
                lines.append(f"  {info.get('personality', '')}")
                lines.append("")

    # 天中殺
    kuubou_str = "・".join(kuubou)
    lines.append(f"【天中殺】{kuubou_str}")
    lines.append("天中殺の期間は、精神世界が活性化する時期です。")
    lines.append("新しい始まりよりも、内省と準備に適しています。")

    return "\n".join(lines)


def calculate(birth_data: BirthData) -> DivinationResult:
    """算命学の命式を算出する。"""
    bd = birth_data.birth_date
    warnings = []

    year_kan, year_shi = get_year_kanshi(bd.year, bd.month, bd.day)
    month_kan, month_shi = get_month_kanshi(bd.year, bd.month, bd.day, year_kan)
    day_kan, day_shi = get_day_kanshi(bd.year, bd.month, bd.day)

    day_gogyo = kanshi_to_gogyo(day_kan)
    day_inyo = kanshi_to_inyo(day_kan)

    # 人体星図
    jintai = _build_jintai_seizu(day_kan, month_kan, year_kan, day_shi, month_shi, year_shi)

    # 空亡（天中殺）
    kuubou = get_kuubou(day_kan, day_shi)

    interpretation = _build_interpretation(
        jintai, day_kan, day_gogyo, day_inyo, kuubou
    )

    center_star = jintai["center"]
    center_info = JUDAI_DESCRIPTIONS.get(center_star, {})

    return DivinationResult(
        system_name="算命学",
        system_id="sanmei_gaku",
        summary=f"日干: {day_kan}（{day_gogyo}の{day_inyo}） 中心星: {center_star}",
        details={
            "nishu": {
                "kan": day_kan,
                "gogyo": day_gogyo,
                "inyo": day_inyo,
            },
            "pillars": {
                "year": f"{year_kan}{year_shi}",
                "month": f"{month_kan}{month_shi}",
                "day": f"{day_kan}{day_shi}",
            },
            "jintai_seizu": jintai,
            "center_star": center_star,
            "center_keyword": center_info.get("keyword", ""),
            "tenchuu_satsu": list(kuubou),
        },
        interpretation=interpretation,
        warnings=warnings,
    )
