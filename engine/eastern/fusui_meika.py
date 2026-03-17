"""風水の命卦（本命卦） — 八卦による東四命・西四命の分類"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult
from utils.kanshi import get_setsu_year


TRIGRAMS = {
    1: {"name": "坎", "reading": "かん", "direction": "北", "group": "東四命", "element": "水"},
    2: {"name": "坤", "reading": "こん", "direction": "南西", "group": "西四命", "element": "土"},
    3: {"name": "震", "reading": "しん", "direction": "東", "group": "東四命", "element": "木"},
    4: {"name": "巽", "reading": "そん", "direction": "南東", "group": "東四命", "element": "木"},
    5: {"name": "中宮", "reading": "ちゅうぐう", "direction": "中央", "group": None, "element": "土"},
    6: {"name": "乾", "reading": "けん", "direction": "北西", "group": "西四命", "element": "金"},
    7: {"name": "兌", "reading": "だ", "direction": "西", "group": "西四命", "element": "金"},
    8: {"name": "艮", "reading": "ごん", "direction": "北東", "group": "西四命", "element": "土"},
    9: {"name": "離", "reading": "り", "direction": "南", "group": "東四命", "element": "火"},
}

# 各命卦に対する八方位の吉凶
# 吉方位: 生気（最大吉）、天医（大吉）、延年（中吉）、伏位（小吉）
# 凶方位: 禍害（小凶）、六殺（中凶）、五鬼（大凶）、絶命（最大凶）
DIRECTIONS = {
    1: {"生気": "南東", "天医": "東", "延年": "南", "伏位": "北",
        "禍害": "西", "六殺": "北東", "五鬼": "北西", "絶命": "南西"},
    2: {"生気": "北東", "天医": "西", "延年": "北西", "伏位": "南西",
        "禍害": "東", "六殺": "南", "五鬼": "南東", "絶命": "北"},
    3: {"生気": "南", "天医": "北", "延年": "南東", "伏位": "東",
        "禍害": "南西", "六殺": "北西", "五鬼": "北東", "絶命": "西"},
    4: {"生気": "北", "天医": "南", "延年": "東", "伏位": "南東",
        "禍害": "北西", "六殺": "南西", "五鬼": "西", "絶命": "北東"},
    6: {"生気": "西", "天医": "北東", "延年": "南西", "伏位": "北西",
        "禍害": "南東", "六殺": "北", "五鬼": "南", "絶命": "東"},
    7: {"生気": "北西", "天医": "南西", "延年": "北東", "伏位": "西",
        "禍害": "北", "六殺": "南東", "五鬼": "東", "絶命": "南"},
    8: {"生気": "南西", "天医": "北西", "延年": "西", "伏位": "北東",
        "禍害": "南", "六殺": "東", "五鬼": "北", "絶命": "南東"},
    9: {"生気": "東", "天医": "南東", "延年": "北", "伏位": "南",
        "禍害": "北東", "六殺": "西", "五鬼": "南西", "絶命": "北西"},
}

KICHI_LABELS = ["生気", "天医", "延年", "伏位"]
KYOU_LABELS = ["禍害", "六殺", "五鬼", "絶命"]


def _calc_meika(year: int, month: int, day: int, gender: str) -> int:
    """命卦数を算出する。gender: 'M' or 'F'"""
    setsu_year = get_setsu_year(year, month, day)
    last2 = setsu_year % 100

    if setsu_year < 2000:
        if gender == "M":
            result = (100 - last2) % 9
        else:
            result = (last2 - 4) % 9
    else:
        if gender == "M":
            result = (9 - (last2 % 9)) % 9
        else:
            result = (last2 + 6) % 9

    if result == 0:
        result = 9

    # 中宮(5)の場合のリダイレクト
    if result == 5:
        result = 2 if gender == "M" else 8

    return result


def _format_directions(meika_num: int) -> str:
    """方位の吉凶を整形して返す"""
    dirs = DIRECTIONS[meika_num]
    lines = []
    lines.append("【吉方位】")
    for label in KICHI_LABELS:
        lines.append(f"  {label}: {dirs[label]}")
    lines.append("【凶方位】")
    for label in KYOU_LABELS:
        lines.append(f"  {label}: {dirs[label]}")
    return "\n".join(lines)


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date
    warnings = []

    if birth_data.gender is None:
        # 性別未指定の場合は両方算出
        male_num = _calc_meika(bd.year, bd.month, bd.day, "M")
        female_num = _calc_meika(bd.year, bd.month, bd.day, "F")
        male_tri = TRIGRAMS[male_num]
        female_tri = TRIGRAMS[female_num]

        warnings.append("性別が指定されていないため、男女両方の命卦を算出しています。正確な結果には性別の指定が必要です。")

        details = {
            "male": {
                "meika_number": male_num,
                "trigram": male_tri["name"],
                "reading": male_tri["reading"],
                "direction": male_tri["direction"],
                "group": male_tri["group"],
                "element": male_tri["element"],
                "auspicious_directions": {k: DIRECTIONS[male_num][k] for k in KICHI_LABELS},
                "inauspicious_directions": {k: DIRECTIONS[male_num][k] for k in KYOU_LABELS},
            },
            "female": {
                "meika_number": female_num,
                "trigram": female_tri["name"],
                "reading": female_tri["reading"],
                "direction": female_tri["direction"],
                "group": female_tri["group"],
                "element": female_tri["element"],
                "auspicious_directions": {k: DIRECTIONS[female_num][k] for k in KICHI_LABELS},
                "inauspicious_directions": {k: DIRECTIONS[female_num][k] for k in KYOU_LABELS},
            },
        }

        summary = f"命卦: 男性={male_tri['name']}({male_tri['group']}) / 女性={female_tri['name']}({female_tri['group']})"
        interpretation = (
            f"【男性の場合】\n"
            f"本命卦: {male_tri['name']}（{male_tri['reading']}）— {male_tri['group']}\n"
            f"本命方位: {male_tri['direction']} / 五行: {male_tri['element']}\n"
            f"{_format_directions(male_num)}\n\n"
            f"【女性の場合】\n"
            f"本命卦: {female_tri['name']}（{female_tri['reading']}）— {female_tri['group']}\n"
            f"本命方位: {female_tri['direction']} / 五行: {female_tri['element']}\n"
            f"{_format_directions(female_num)}"
        )
    else:
        meika_num = _calc_meika(bd.year, bd.month, bd.day, birth_data.gender)
        tri = TRIGRAMS[meika_num]

        details = {
            "meika_number": meika_num,
            "trigram": tri["name"],
            "reading": tri["reading"],
            "direction": tri["direction"],
            "group": tri["group"],
            "element": tri["element"],
            "gender": birth_data.gender,
            "auspicious_directions": {k: DIRECTIONS[meika_num][k] for k in KICHI_LABELS},
            "inauspicious_directions": {k: DIRECTIONS[meika_num][k] for k in KYOU_LABELS},
        }

        gender_label = "男性" if birth_data.gender == "M" else "女性"
        summary = f"命卦: {tri['name']}（{tri['group']}）"
        interpretation = (
            f"本命卦: {tri['name']}（{tri['reading']}）— {gender_label}\n"
            f"分類: {tri['group']} / 本命方位: {tri['direction']} / 五行: {tri['element']}\n\n"
            f"{_format_directions(meika_num)}\n\n"
            f"東四命は東・南東・南・北が吉方位、西四命は西・北西・南西・北東が吉方位です。\n"
            f"住居の玄関や寝室の向きをこの吉方位に合わせることで、気の流れが良くなるとされています。"
        )

    return DivinationResult(
        system_name="風水・本命卦",
        system_id="fusui_meika",
        summary=summary,
        details=details,
        interpretation=interpretation,
        warnings=warnings,
    )
