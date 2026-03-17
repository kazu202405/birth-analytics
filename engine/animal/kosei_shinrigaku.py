"""個性心理学（ISD）

動物占いと同じ六十干支ベースのキャラクターナンバーから、
3つの側面（本質・表面・意思決定）を算出し、
3分類・レール分類とあわせて多面的に性格を分析する。
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult

# Import shared calculation logic from doubutsu_uranai
from animal.doubutsu_uranai import (
    ANIMALS,
    CHAR_60,
    PERSONALITY,
    GROUP_MOON,
    GROUP_EARTH,
    GROUP_SUN,
    get_character_number,
    get_group,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Rail classification (char_num % 4)
RAILS: dict[int, tuple[str, str]] = {
    0: ("HOPE",  "希望のレール ── 夢や理想を追い求めて前進する。ポジティブな未来志向型。"),
    1: ("POWER", "パワーのレール ── 行動力と実行力で道を切り開く。現実主義の実力派。"),
    2: ("LOVE",  "愛情のレール ── 人との絆を大切にし、愛情で周囲を包む。共感力の高い調和型。"),
    3: ("ACE",   "エースのレール ── 独自の才能と個性で勝負する。カリスマ性を持つ一点突破型。"),
}

# Aspect labels
ASPECT_HONSHITSU = "本質キャラクター"
ASPECT_HYOUMEN = "表面キャラクター"
ASPECT_ISHIKETTEI = "意思決定キャラクター"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _calc_surface_index(char_num: int) -> int:
    """Derive the surface (outer) character index."""
    return (char_num + 7) % 12


def _calc_decision_index(char_num: int) -> int:
    """Derive the decision-making character index."""
    return (char_num * 2 + 3) % 12


def _build_aspect(label: str, animal_index: int, color: str | None = None) -> dict:
    """Build a dictionary describing one aspect of personality."""
    animal_name = ANIMALS[animal_index]
    group_key, group_label = get_group(animal_index)
    result: dict = {
        "label": label,
        "animal_index": animal_index,
        "animal_name": animal_name,
        "group": group_key,
        "group_label": group_label,
        "personality": PERSONALITY[animal_index],
    }
    if color is not None:
        result["color"] = color
        result["full_name"] = f"{color}の{animal_name}"
    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def calculate(birth_data: BirthData) -> DivinationResult:
    """Run the ISD (Individual Statistics Dynamics) personality analysis."""
    bd = birth_data.birth_date
    warnings: list[str] = []

    from animal.doubutsu_uranai import YEAR_TABLE
    if bd.year not in YEAR_TABLE:
        warnings.append(
            f"{bd.year}年は年表の範囲外のため推定値を使用しています。"
            "結果の精度が下がる可能性があります。"
        )

    char_num = get_character_number(bd.year, bd.month, bd.day)

    # --- Three aspects ---
    honshitsu_index, honshitsu_color = CHAR_60[char_num]
    hyoumen_index = _calc_surface_index(char_num)
    ishikettei_index = _calc_decision_index(char_num)

    honshitsu = _build_aspect(ASPECT_HONSHITSU, honshitsu_index, honshitsu_color)
    hyoumen = _build_aspect(ASPECT_HYOUMEN, hyoumen_index)
    ishikettei = _build_aspect(ASPECT_ISHIKETTEI, ishikettei_index)

    # --- Rail ---
    rail_key_index = char_num % 4
    rail_key, rail_description = RAILS[rail_key_index]

    # --- 3-group (based on honshitsu) ---
    group_key, group_label = get_group(honshitsu_index)

    details: dict = {
        "character_number": char_num,
        "honshitsu": honshitsu,
        "hyoumen": hyoumen,
        "ishikettei": ishikettei,
        "group": group_key,
        "group_label": group_label,
        "rail": rail_key,
        "rail_description": rail_description,
    }

    hon_name = honshitsu.get("full_name", ANIMALS[honshitsu_index])
    hyo_name = ANIMALS[hyoumen_index]
    ishi_name = ANIMALS[ishikettei_index]

    summary = (
        f"本質は「{hon_name}」、表面は「{hyo_name}」、"
        f"意思決定は「{ishi_name}」です。"
    )

    interpretation = (
        f"■ {ASPECT_HONSHITSU}（内面・本来の自分）\n"
        f"  {hon_name}（{group_label}）\n"
        f"  {PERSONALITY[honshitsu_index]}\n\n"
        f"■ {ASPECT_HYOUMEN}（他人から見た印象）\n"
        f"  {hyo_name}\n"
        f"  {PERSONALITY[hyoumen_index]}\n\n"
        f"■ {ASPECT_ISHIKETTEI}（決断時の傾向）\n"
        f"  {ishi_name}\n"
        f"  {PERSONALITY[ishikettei_index]}\n\n"
        f"■ 3分類: {group_key}（{group_label}）\n"
        f"■ レール: {rail_description}"
    )

    return DivinationResult(
        system_name="個性心理学",
        system_id="kosei_shinrigaku",
        summary=summary,
        details=details,
        interpretation=interpretation,
        warnings=warnings,
    )
