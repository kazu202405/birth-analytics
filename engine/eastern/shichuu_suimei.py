"""四柱推命（しちゅうすいめい）

生年月日時を四本の柱（年柱・月柱・日柱・時柱）として干支で表し、
命式から性格・運勢を読み解く東洋占術の中核的体系。
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult
from utils.kanshi import (
    get_year_kanshi, get_month_kanshi, get_day_kanshi,
    get_hour_kanshi, kanshi_to_gogyo, kanshi_to_inyo, get_kuubou,
)
from utils.constants import JIKKAN, JUNISHI, KAN_TO_GOGYO, KAN_TO_INYO, SHI_TO_GOGYO

# ── 五行の数値順序 ──
GOGYO_ORDER = {"木": 0, "火": 1, "土": 2, "金": 3, "水": 4}

# ── 通変星（十神） ──
# (五行関係オフセット, 同陰陽フラグ) -> 通変星名
TSUHENSEI_MAP = {
    (0, True): "比肩", (0, False): "劫財",
    (1, True): "食神", (1, False): "傷官",
    (2, True): "偏財", (2, False): "正財",
    (3, True): "偏官", (3, False): "正官",
    (4, True): "偏印", (4, False): "印綬",
}

TSUHENSEI_DESCRIPTIONS = {
    "比肩": "自立心・競争心が強く、独立独歩の精神を持つ。自分の力で切り拓く力。",
    "劫財": "社交的で行動力がある。人脈を活かす力と大胆な決断力。",
    "食神": "穏やかで楽天的。衣食住に恵まれ、表現力と創造性が豊か。",
    "傷官": "繊細で鋭い感性。芸術的才能と完璧主義。知性が際立つ。",
    "偏財": "社交的で人望がある。商才に長け、大きな財を動かす力。",
    "正財": "堅実で誠実。コツコツと努力し、安定した財を築く力。",
    "偏官": "行動力と正義感に溢れる。荒波を乗り越える強さと統率力。",
    "正官": "品格と信頼感がある。社会的地位と名誉を得る力。責任感が強い。",
    "偏印": "知的好奇心が旺盛。独創的な発想と学問への探求心。",
    "印綬": "学問・教養に秀でる。慈愛深く、精神的な充実を重視する。",
}

# ── 十二運星 ──
JUNI_UNSEI = [
    "長生", "沐浴", "冠帯", "臨官", "帝旺",
    "衰", "病", "死", "墓", "絶", "胎", "養",
]

JUNI_UNSEI_DESCRIPTIONS = {
    "長生": "成長力・発展性に優れる。新しい環境で力を発揮する。",
    "沐浴": "感受性が豊かで多芸多才。変化を好み、自由奔放。",
    "冠帯": "向上心が強く、社会的に活躍する。華やかさがある。",
    "臨官": "社会的に認められる時期。実力が評価され、地位が安定。",
    "帝旺": "最も勢いが強い。リーダーシップを発揮し、頂点に立つ力。",
    "衰": "穏やかで思慮深い。経験を活かし、安定した判断ができる。",
    "病": "繊細で直感力がある。芸術やスピリチュアルな分野に才能。",
    "死": "決断力と集中力がある。一つのことを極める力を持つ。",
    "墓": "蓄財能力と探究心がある。先祖や家系の影響を受けやすい。",
    "絶": "独創性と変革の力。ゼロからの創造力に優れる。",
    "胎": "直感力と適応力がある。新しいことへの感覚が鋭い。",
    "養": "温厚で包容力がある。人に愛され、引き立てを受けやすい。",
}

# 日干ごとの十二運の基準地支インデックス
JUNI_START = {
    "甲": 2, "乙": 5, "丙": 2, "丁": 5, "戊": 2,
    "己": 5, "庚": 2, "辛": 5, "壬": 2, "癸": 5,
}

# ── 日主の五行による性格特性 ──
NISHU_TRAITS = {
    ("木", "陽"): "甲木（きのえ）: 大木のような真っ直ぐな性格。正義感が強く、曲がったことを嫌う。リーダー気質で周囲を引っ張る力がある。",
    ("木", "陰"): "乙木（きのと）: 草花のようなしなやかさ。柔軟性があり、環境に適応する力がある。優しく協調性に富む。",
    ("火", "陽"): "丙火（ひのえ）: 太陽のような明るさと情熱。行動力があり、周囲を照らす存在。楽観的で人を惹きつける。",
    ("火", "陰"): "丁火（ひのと）: ろうそくの灯のような繊細な輝き。内面に強い信念を持ち、知性と感受性が豊か。",
    ("土", "陽"): "戊土（つちのえ）: 山のような安定感と包容力。信頼感があり、どっしりと構える器の大きさ。",
    ("土", "陰"): "己土（つちのと）: 田畑のような育成力。面倒見が良く、人を育てる力がある。堅実で現実的。",
    ("金", "陽"): "庚金（かのえ）: 剣のような鋭さと決断力。意志が強く、困難にも立ち向かう勇気がある。",
    ("金", "陰"): "辛金（かのと）: 宝石のような美意識と繊細さ。完璧主義で、美しいものへのこだわりが強い。",
    ("水", "陽"): "壬水（みずのえ）: 大河のようなスケールの大きさ。知恵と包容力があり、大きな流れを作る力。",
    ("水", "陰"): "癸水（みずのと）: 雨露のような潤いと繊細さ。直感力に優れ、人の心を察する力がある。",
}

# ── 地支の蔵干（主気のみ・簡易版） ──
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

    return TSUHENSEI_MAP[(relation, same_polarity)]


def _get_juni_unsei(day_kan: str, shi: str) -> str:
    """日干と地支から十二運星を算出する。"""
    start = JUNI_START.get(day_kan, 0)
    shi_idx = JUNISHI.index(shi)
    day_idx = JIKKAN.index(day_kan)

    if day_idx % 2 == 0:  # 陽干は順行
        offset = (shi_idx - start) % 12
    else:  # 陰干は逆行
        offset = (start - shi_idx) % 12

    return JUNI_UNSEI[offset]


def _build_pillar_info(
    pillar_name: str, kan: str, shi: str, day_kan: str
) -> dict:
    """柱の詳細情報を構築する。"""
    tsuhen = _get_tsuhensei(day_kan, kan) if kan != day_kan else "比肩"
    juni = _get_juni_unsei(day_kan, shi)
    zoukan = ZOUKAN_MAIN.get(shi, "")
    zoukan_tsuhen = _get_tsuhensei(day_kan, zoukan) if zoukan and zoukan != day_kan else "比肩"

    return {
        "pillar": f"{kan}{shi}",
        "kan": kan,
        "shi": shi,
        "kan_gogyo": KAN_TO_GOGYO[kan],
        "kan_inyo": KAN_TO_INYO[kan],
        "tsuhensei": tsuhen,
        "juni_unsei": juni,
        "zoukan": zoukan,
        "zoukan_tsuhensei": zoukan_tsuhen,
    }


def _build_interpretation(
    pillars: dict[str, dict],
    day_kan: str,
    day_gogyo: str,
    day_inyo: str,
    kuubou: tuple[str, ...],
    has_time: bool,
) -> str:
    """命式の総合解釈テキストを生成する。"""
    lines = []

    # 日主
    nishu_key = (day_gogyo, day_inyo)
    nishu_trait = NISHU_TRAITS.get(nishu_key, "")
    lines.append(f"【日主】{nishu_trait}")
    lines.append("")

    # 各柱の通変星と十二運
    lines.append("【命式】")
    pillar_labels = {"year": "年柱", "month": "月柱", "day": "日柱", "hour": "時柱"}
    for key in ["year", "month", "day", "hour"]:
        if key not in pillars:
            continue
        p = pillars[key]
        label = pillar_labels[key]
        lines.append(
            f"  {label}: {p['pillar']}（{p['kan_gogyo']}の{p['kan_inyo']}）"
            f" ─ 通変星: {p['tsuhensei']} / 十二運: {p['juni_unsei']}"
        )

    lines.append("")

    # 通変星の解説
    seen_tsuhen = set()
    for key in ["year", "month", "day", "hour"]:
        if key not in pillars:
            continue
        t = pillars[key]["tsuhensei"]
        if t not in seen_tsuhen:
            seen_tsuhen.add(t)
            desc = TSUHENSEI_DESCRIPTIONS.get(t, "")
            if desc:
                lines.append(f"【{t}】{desc}")

    lines.append("")

    # 十二運の解説
    seen_juni = set()
    for key in ["year", "month", "day", "hour"]:
        if key not in pillars:
            continue
        j = pillars[key]["juni_unsei"]
        if j not in seen_juni:
            seen_juni.add(j)
            desc = JUNI_UNSEI_DESCRIPTIONS.get(j, "")
            if desc:
                lines.append(f"【{j}】{desc}")

    lines.append("")

    # 空亡
    kuubou_str = "・".join(kuubou)
    lines.append(f"【空亡（天中殺）】{kuubou_str}")
    lines.append("空亡の地支に対応する年・月は、変化や転換期となりやすい時期です。")
    lines.append("既存の価値観が揺らぎ、新しい方向性が示される時でもあります。")

    if not has_time:
        lines.append("")
        lines.append("※出生時刻が不明のため、時柱は算出していません。")

    return "\n".join(lines)


def calculate(birth_data: BirthData) -> DivinationResult:
    """四柱推命の命式を算出する。"""
    bd = birth_data.birth_date
    warnings = []

    # 三柱（年・月・日）の算出
    year_kan, year_shi = get_year_kanshi(bd.year, bd.month, bd.day)
    month_kan, month_shi = get_month_kanshi(bd.year, bd.month, bd.day, year_kan)
    day_kan, day_shi = get_day_kanshi(bd.year, bd.month, bd.day)

    day_gogyo = kanshi_to_gogyo(day_kan)
    day_inyo = kanshi_to_inyo(day_kan)

    pillars_info = {
        "year": _build_pillar_info("年柱", year_kan, year_shi, day_kan),
        "month": _build_pillar_info("月柱", month_kan, month_shi, day_kan),
        "day": _build_pillar_info("日柱", day_kan, day_shi, day_kan),
    }

    # 時柱（出生時刻がある場合のみ）
    has_time = birth_data.birth_time is not None
    if has_time:
        hour = birth_data.birth_time.hour
        hour_kan, hour_shi = get_hour_kanshi(hour, day_kan)
        pillars_info["hour"] = _build_pillar_info("時柱", hour_kan, hour_shi, day_kan)
    else:
        warnings.append("出生時刻が不明のため、時柱は算出していません。")

    # 空亡（天中殺）
    kuubou = get_kuubou(day_kan, day_shi)

    # 五行カウント
    gogyo_counts = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
    for p in pillars_info.values():
        gogyo_counts[p["kan_gogyo"]] += 1
        gogyo_counts[SHI_TO_GOGYO[p["shi"]]] += 1

    interpretation = _build_interpretation(
        pillars_info, day_kan, day_gogyo, day_inyo, kuubou, has_time
    )

    # 命式サマリー
    pillar_strs = []
    for key in ["year", "month", "day", "hour"]:
        if key in pillars_info:
            pillar_strs.append(pillars_info[key]["pillar"])
    summary = f"日主: {day_kan}（{day_gogyo}の{day_inyo}） 命式: {' / '.join(pillar_strs)}"

    return DivinationResult(
        system_name="四柱推命",
        system_id="shichuu_suimei",
        summary=summary,
        details={
            "nishu": {
                "kan": day_kan,
                "gogyo": day_gogyo,
                "inyo": day_inyo,
            },
            "pillars": pillars_info,
            "kuubou": list(kuubou),
            "gogyo_counts": gogyo_counts,
        },
        interpretation=interpretation,
        warnings=warnings,
    )
