"""アラビア占星術（12武器）"""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


ARABIAN_WEAPONS = [
    {
        "name": "短剣",
        "dates": [(1, 30, 2, 28)],
        "trait": "鋭い知性と決断力。素早く正確な判断ができる。",
        "lucky_number": 8,
        "lucky_day": "火曜日",
    },
    {
        "name": "棍棒",
        "dates": [(3, 1, 3, 10)],
        "trait": "力強さと忍耐力。困難に立ち向かう勇気を持つ。",
        "lucky_number": 3,
        "lucky_day": "木曜日",
    },
    {
        "name": "ハサミ",
        "dates": [(3, 11, 4, 20)],
        "trait": "器用さと正確さ。複雑な問題を解きほぐす力。",
        "lucky_number": 7,
        "lucky_day": "水曜日",
    },
    {
        "name": "鉄球",
        "dates": [(4, 21, 5, 1)],
        "trait": "圧倒的な存在感と影響力。周囲を動かす力。",
        "lucky_number": 1,
        "lucky_day": "日曜日",
    },
    {
        "name": "刀",
        "dates": [(5, 2, 6, 21)],
        "trait": "正義感と名誉。高い理想を持ち品格がある。",
        "lucky_number": 9,
        "lucky_day": "月曜日",
    },
    {
        "name": "鞭",
        "dates": [(6, 22, 7, 22)],
        "trait": "柔軟性と統率力。状況に応じた対応ができる。",
        "lucky_number": 5,
        "lucky_day": "金曜日",
    },
    {
        "name": "投石器",
        "dates": [(7, 23, 8, 22)],
        "trait": "遠くを見通す力と的確な行動力。戦略的思考。",
        "lucky_number": 4,
        "lucky_day": "火曜日",
    },
    {
        "name": "斧",
        "dates": [(8, 23, 9, 3)],
        "trait": "開拓精神と実行力。道を切り開く力強さ。",
        "lucky_number": 6,
        "lucky_day": "土曜日",
    },
    {
        "name": "弓",
        "dates": [(9, 4, 10, 3)],
        "trait": "集中力と精密さ。目標に向かって一直線。",
        "lucky_number": 2,
        "lucky_day": "水曜日",
    },
    {
        "name": "槍",
        "dates": [(10, 4, 11, 3)],
        "trait": "前進する勇気とリーチの広さ。広い視野を持つ。",
        "lucky_number": 11,
        "lucky_day": "木曜日",
    },
    {
        "name": "鎖",
        "dates": [(11, 4, 11, 29)],
        "trait": "結びつきの力と持続力。人との絆を大切にする。",
        "lucky_number": 6,
        "lucky_day": "金曜日",
    },
    {
        "name": "矢",
        "dates": [(11, 30, 1, 29)],
        "trait": "スピードと正確さ。迷いなく目標を射抜く。",
        "lucky_number": 3,
        "lucky_day": "月曜日",
    },
]


def _match_date_range(month: int, day: int, sm: int, sd: int, em: int, ed: int) -> bool:
    """Check if month/day falls within a date range, handling year-wrapping."""
    target = month * 100 + day
    start = sm * 100 + sd
    end = em * 100 + ed
    if start <= end:
        return start <= target <= end
    # Year-wrapping (e.g., 11/30 - 1/29)
    return target >= start or target <= end


def _find_weapon(month: int, day: int) -> dict | None:
    """Find the Arabian weapon for a given birth month and day."""
    for weapon in ARABIAN_WEAPONS:
        for sm, sd, em, ed in weapon["dates"]:
            if _match_date_range(month, day, sm, sd, em, ed):
                return weapon
    return None


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date
    weapon = _find_weapon(bd.month, bd.day)

    if weapon is None:
        return DivinationResult(
            system_name="アラビア占星術",
            system_id="arabian",
            summary="該当する守護武器が見つかりませんでした",
            details={"birth_month": bd.month, "birth_day": bd.day},
            interpretation="入力された誕生日に対応するアラビアの守護武器が特定できませんでした。",
            warnings=["該当する守護武器が見つかりません"],
        )

    return DivinationResult(
        system_name="アラビア占星術",
        system_id="arabian",
        summary=f"守護武器: {weapon['name']}",
        details={
            "weapon_name": weapon["name"],
            "trait": weapon["trait"],
            "lucky_number": weapon["lucky_number"],
            "lucky_day": weapon["lucky_day"],
            "birth_month": bd.month,
            "birth_day": bd.day,
        },
        interpretation=(
            f"あなたの守護武器は「{weapon['name']}」です。\n"
            f"性質: {weapon['trait']}\n"
            f"ラッキーナンバー: {weapon['lucky_number']} / ラッキーデー: {weapon['lucky_day']}"
        ),
    )
