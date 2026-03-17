"""陰陽五行（いんようごぎょう）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult
from utils.kanshi import get_year_kanshi, get_month_kanshi, get_day_kanshi, kanshi_to_gogyo, kanshi_to_inyo
from utils.constants import KAN_TO_GOGYO, SHI_TO_GOGYO, GOGYO_SOUSHOU, GOGYO_SOUKOKU


def _count_gogyo(pillars: list[tuple[str, str]]) -> dict[str, int]:
    """命式全体の五行カウント"""
    counts = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
    for kan, shi in pillars:
        counts[KAN_TO_GOGYO[kan]] += 1
        counts[SHI_TO_GOGYO[shi]] += 1
    return counts


def _analyze_balance(counts: dict[str, int], day_gogyo: str) -> str:
    """五行バランスの分析"""
    total = sum(counts.values())
    strong = [g for g, c in counts.items() if c >= 3]
    weak = [g for g, c in counts.items() if c == 0]

    analysis = []
    if strong:
        analysis.append(f"強い五行: {', '.join(strong)}")
    if weak:
        analysis.append(f"欠けている五行: {', '.join(weak)}")

    # 日主の五行と相生・相剋
    soushou_target = GOGYO_SOUSHOU[day_gogyo]
    soukoku_target = GOGYO_SOUKOKU[day_gogyo]
    analysis.append(f"日主の五行「{day_gogyo}」は「{soushou_target}」を生み、「{soukoku_target}」を剋す")

    return "\n".join(analysis)


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date

    year_kan, year_shi = get_year_kanshi(bd.year, bd.month, bd.day)
    month_kan, month_shi = get_month_kanshi(bd.year, bd.month, bd.day, year_kan)
    day_kan, day_shi = get_day_kanshi(bd.year, bd.month, bd.day)

    pillars = [(year_kan, year_shi), (month_kan, month_shi), (day_kan, day_shi)]
    day_gogyo = kanshi_to_gogyo(day_kan)
    day_inyo = kanshi_to_inyo(day_kan)

    counts = _count_gogyo(pillars)
    balance = _analyze_balance(counts, day_gogyo)

    return DivinationResult(
        system_name="陰陽五行",
        system_id="inyo_gogyo",
        summary=f"日主: {day_kan}（{day_gogyo}の{day_inyo}）",
        details={
            "day_kan": day_kan,
            "day_gogyo": day_gogyo,
            "day_inyo": day_inyo,
            "pillars": {
                "year": f"{year_kan}{year_shi}",
                "month": f"{month_kan}{month_shi}",
                "day": f"{day_kan}{day_shi}",
            },
            "gogyo_counts": counts,
            "soushou": f"{day_gogyo} → {GOGYO_SOUSHOU[day_gogyo]}",
            "soukoku": f"{day_gogyo} → {GOGYO_SOUKOKU[day_gogyo]}",
        },
        interpretation=f"日主: {day_kan}（{day_gogyo}の{day_inyo}）\n"
                       f"年柱: {year_kan}{year_shi} / 月柱: {month_kan}{month_shi} / 日柱: {day_kan}{day_shi}\n"
                       f"五行バランス: 木{counts['木']} 火{counts['火']} 土{counts['土']} 金{counts['金']} 水{counts['水']}\n"
                       f"{balance}",
    )
