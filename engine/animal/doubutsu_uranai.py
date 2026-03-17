"""動物占い（60分類版）

12種類の動物 x 5色のカラーバリエーション = 60分類。
生年月日から六十干支ベースのキャラクターナンバーを算出し、
基本動物・カラー・3分類グループを判定する。
"""

import calendar
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ANIMALS = [
    "こじか",     # 0
    "たぬき",     # 1
    "猿",         # 2
    "チータ",     # 3
    "黒ひょう",   # 4
    "ライオン",   # 5
    "虎",         # 6
    "ゾウ",       # 7
    "ひつじ",     # 8
    "ペガサス",   # 9
    "狼",         # 10
    "コアラ",     # 11
]

# Year -> base number lookup (1940-2026)
YEAR_TABLE: dict[int, int] = {
    1940: 37, 1941: 31, 1942: 26, 1943: 20, 1944: 15, 1945: 9,
    1946: 3,  1947: 58, 1948: 52, 1949: 47, 1950: 41, 1951: 35,
    1952: 30, 1953: 24, 1954: 19, 1955: 13, 1956: 7,  1957: 2,
    1958: 56, 1959: 51, 1960: 45, 1961: 39, 1962: 34, 1963: 28,
    1964: 23, 1965: 17, 1966: 11, 1967: 6,  1968: 0,  1969: 55,
    1970: 49, 1971: 43, 1972: 38, 1973: 32, 1974: 27, 1975: 21,
    1976: 15, 1977: 10, 1978: 4,  1979: 59, 1980: 53, 1981: 47,
    1982: 42, 1983: 36, 1984: 31, 1985: 25, 1986: 19, 1987: 14,
    1988: 8,  1989: 3,  1990: 57, 1991: 51, 1992: 46, 1993: 40,
    1994: 35, 1995: 29, 1996: 23, 1997: 18, 1998: 12, 1999: 7,
    2000: 1,  2001: 55, 2002: 50, 2003: 44, 2004: 39, 2005: 33,
    2006: 27, 2007: 22, 2008: 16, 2009: 11, 2010: 5,  2011: 59,
    2012: 54, 2013: 48, 2014: 43, 2015: 37, 2016: 31, 2017: 26,
    2018: 20, 2019: 15, 2020: 9,  2021: 3,  2022: 58, 2023: 52,
    2024: 47, 2025: 41, 2026: 35,
}

# 60 character -> (animal_index, color) mapping
CHAR_60: list[tuple[int, str]] = [
    (10, "イエロー"), (3, "シルバー"), (4, "ゴールド"), (8, "オレンジ"), (0, "グリーン"),
    (1, "シルバー"),  (2, "ゴールド"), (5, "イエロー"), (6, "ブラウン"), (9, "ゴールド"),
    (11, "ブルー"),   (7, "グリーン"), (10, "ブルー"),  (3, "ゴールド"), (4, "シルバー"),
    (8, "ブルー"),    (0, "レッド"),   (1, "グリーン"), (2, "レッド"),   (5, "グリーン"),
    (6, "オレンジ"),  (9, "シルバー"), (11, "パープル"),(7, "イエロー"), (10, "シルバー"),
    (3, "ブラウン"),  (4, "ブラウン"), (8, "パープル"), (0, "オレンジ"), (1, "イエロー"),
    (2, "オレンジ"),  (5, "レッド"),   (6, "ブルー"),   (9, "レッド"),   (11, "レッド"),
    (7, "レッド"),    (10, "ブラウン"),(3, "レッド"),   (4, "レッド"),   (8, "ブラック"),
    (0, "ブルー"),    (1, "ブルー"),   (2, "ブルー"),   (5, "ブルー"),   (6, "パープル"),
    (9, "イエロー"),  (11, "オレンジ"),(7, "ブルー"),   (10, "オレンジ"),(3, "パープル"),
    (4, "パープル"),  (8, "イエロー"), (0, "パープル"), (1, "レッド"),   (2, "パープル"),
    (5, "オレンジ"),  (6, "レッド"),   (9, "ブラウン"), (11, "グリーン"),(7, "オレンジ"),
]

# 3-group classification
GROUP_MOON = {0, 1, 8}       # 人志向 (こじか, たぬき, ひつじ)
GROUP_EARTH = {2, 6, 11}     # 城志向 (猿, 虎, コアラ)
GROUP_SUN = {3, 4, 5, 7, 9, 10}  # 大物志向 (チータ, 黒ひょう, ライオン, ゾウ, ペガサス, 狼)

GROUP_NAMES: dict[str, tuple[str, str]] = {
    "MOON":  ("MOON",  "人志向"),
    "EARTH": ("EARTH", "城志向"),
    "SUN":   ("SUN",   "大物志向"),
}

# Personality descriptions for each base animal
PERSONALITY: dict[int, str] = {
    0: (
        "こじか ── 純粋で警戒心が強く、心を許した相手にはとことん甘える。"
        "好奇心旺盛で学習能力が高いが、慣れない環境ではおとなしくなる。"
        "誠実で一途な性格が魅力。"
    ),
    1: (
        "たぬき ── 温厚で社交的、世渡り上手。"
        "愛嬌があり誰からも好かれるが、実は芯の強い努力家。"
        "人を立てながら自分の居場所を確保していく処世術を持つ。"
    ),
    2: (
        "猿 ── 頭の回転が速く器用で、何でもそつなくこなす。"
        "好奇心が強く新しいことに飛びつくが飽きも早い。"
        "明るいムードメーカーでサービス精神旺盛。"
    ),
    3: (
        "チータ ── 瞬発力と行動力に優れたスピードタイプ。"
        "目標を見つけると一直線に突き進むが、長期戦は苦手。"
        "プライドが高く、自由を愛するロマンチスト。"
    ),
    4: (
        "黒ひょう ── 感性が鋭くセンス抜群。流行に敏感でスタイリッシュ。"
        "正義感が強く曲がったことが嫌い。"
        "外見はクールだが内面は情熱的で面倒見がよい。"
    ),
    5: (
        "ライオン ── 堂々としたリーダー気質。存在感があり頼れる親分肌。"
        "完璧主義で自分にも他人にも厳しいが、弱い者には優しい。"
        "体面を重んじ、称賛を力に変えるタイプ。"
    ),
    6: (
        "虎 ── 義理人情に厚く、困っている人を放っておけない親分肌。"
        "バランス感覚に優れ、周囲からの信頼が厚い。"
        "慎重に見えて大胆な決断もできるパワフルな存在。"
    ),
    7: (
        "ゾウ ── 忍耐力と努力で目標を達成する大器晩成型。"
        "コツコツ積み上げる堅実さを持ち、信頼を勝ち取る。"
        "頑固に見えるが、実は繊細でデリケートな一面も。"
    ),
    8: (
        "ひつじ ── 寂しがりやで仲間意識が強い。"
        "情報通で世話好き、グループの潤滑油的存在。"
        "客観的で公平な判断ができるが、一人になるのが苦手。"
    ),
    9: (
        "ペガサス ── 自由奔放で気分屋、束縛を嫌う天才肌。"
        "直感力とひらめきに優れ、独創的な発想をする。"
        "感性が豊かで芸術的才能があるが、気まぐれで読めない。"
    ),
    10: (
        "狼 ── 一匹狼タイプで独自のペースを守る。"
        "マイルールを持ち、自分の世界観を大切にする。"
        "不器用だが誠実で、信頼できる存在。"
    ),
    11: (
        "コアラ ── マイペースで要領がよいロマンチスト。"
        "計算高い一面もあるが、根は優しく愛情深い。"
        "夢見がちだがここぞという時の集中力はすさまじい。"
    ),
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_day_offset(month: int, day: int, is_leap: bool) -> int:
    """Return 1-indexed day-of-year offset."""
    days_before = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    offset = days_before[month - 1] + day
    if is_leap and month > 2:
        offset += 1
    return offset


def _estimate_year_base(year: int) -> int:
    """Fallback estimation for years outside YEAR_TABLE.

    The pattern follows the sexagenary cycle with an approximate yearly
    shift of 5-6 (average ~5.75). We anchor on 2000 = 1 and extrapolate.
    """
    ref_year = 2000
    ref_base = 1
    diff = year - ref_year
    base = (ref_base - diff * 6) % 60
    return base


def get_character_number(year: int, month: int, day: int) -> int:
    """Calculate the 60-character index from a birth date."""
    is_leap = calendar.isleap(year)
    base = YEAR_TABLE.get(year)
    if base is None:
        base = _estimate_year_base(year)
    day_offset = _get_day_offset(month, day, is_leap)
    return (base + day_offset) % 60


def get_group(animal_index: int) -> tuple[str, str]:
    """Return (group_key, group_label) for the given animal index."""
    if animal_index in GROUP_MOON:
        return GROUP_NAMES["MOON"]
    if animal_index in GROUP_EARTH:
        return GROUP_NAMES["EARTH"]
    return GROUP_NAMES["SUN"]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def calculate(birth_data: BirthData) -> DivinationResult:
    """Run the 60-classification Animal Divination."""
    bd = birth_data.birth_date
    warnings: list[str] = []

    if bd.year not in YEAR_TABLE:
        warnings.append(
            f"{bd.year}年は年表の範囲外のため推定値を使用しています。"
            "結果の精度が下がる可能性があります。"
        )

    char_num = get_character_number(bd.year, bd.month, bd.day)
    animal_index, color = CHAR_60[char_num]
    animal_name = ANIMALS[animal_index]
    group_key, group_label = get_group(animal_index)
    full_name = f"{color}の{animal_name}"
    personality = PERSONALITY[animal_index]

    details: dict = {
        "character_number": char_num,
        "animal_index": animal_index,
        "animal_name": animal_name,
        "color": color,
        "full_name": full_name,
        "group": group_key,
        "group_label": group_label,
        "personality": personality,
    }

    summary = f"あなたの動物は「{full_name}」（{group_label}）です。"

    interpretation = (
        f"■ 60分類キャラクター: {full_name}\n"
        f"■ 基本動物: {animal_name}\n"
        f"■ カラー: {color}\n"
        f"■ 3分類: {group_key}（{group_label}）\n\n"
        f"【性格】\n{personality}"
    )

    return DivinationResult(
        system_name="動物占い（60分類版）",
        system_id="doubutsu_uranai_60",
        summary=summary,
        details=details,
        interpretation=interpretation,
        warnings=warnings,
    )
