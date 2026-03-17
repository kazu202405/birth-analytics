"""エジプト占星術（12神）"""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


EGYPTIAN_GODS = [
    {
        "name": "アモン・ラー",
        "dates": [(1, 1, 1, 7), (6, 19, 6, 28), (9, 1, 9, 7)],
        "trait": "自信と創造力に溢れるリーダー。太陽神の加護で周囲を明るく照らす。",
        "element": "火",
        "color": "黄金",
        "stone": "トパーズ",
    },
    {
        "name": "ムト",
        "dates": [(1, 22, 1, 31), (9, 8, 9, 22)],
        "trait": "養育と保護の力。母なる女神の慈愛で人々を包み込む。",
        "element": "水",
        "color": "赤",
        "stone": "ガーネット",
    },
    {
        "name": "ゲブ",
        "dates": [(2, 12, 2, 29), (8, 20, 8, 31)],
        "trait": "大地のように安定し信頼できる存在。実直で誠実な性格。",
        "element": "土",
        "color": "茶",
        "stone": "エメラルド",
    },
    {
        "name": "オシリス",
        "dates": [(3, 1, 3, 10), (11, 27, 12, 18)],
        "trait": "再生と変容の力。困難を乗り越え新しい自分に生まれ変わる。",
        "element": "水",
        "color": "緑",
        "stone": "ラピスラズリ",
    },
    {
        "name": "イシス",
        "dates": [(3, 11, 3, 31), (10, 18, 10, 29), (12, 19, 12, 31)],
        "trait": "知恵と魔法の力。直感に優れ、人々を癒す力を持つ。",
        "element": "風",
        "color": "青",
        "stone": "アメジスト",
    },
    {
        "name": "トート",
        "dates": [(4, 1, 4, 19), (11, 8, 11, 17)],
        "trait": "知識と学問の神。学びへの情熱と優れた知性で真理を探究する。",
        "element": "風",
        "color": "紫",
        "stone": "ターコイズ",
    },
    {
        "name": "ホルス",
        "dates": [(4, 20, 5, 7), (8, 12, 8, 19)],
        "trait": "天空の守護者。勇気と正義感に溢れ、弱い者を守る。",
        "element": "火",
        "color": "赤金",
        "stone": "ルビー",
    },
    {
        "name": "アヌビス",
        "dates": [(5, 8, 5, 27), (6, 29, 7, 13)],
        "trait": "洞察力と判断力。物事の本質を見抜く力を持つ。",
        "element": "土",
        "color": "黒",
        "stone": "オブシディアン",
    },
    {
        "name": "セト",
        "dates": [(5, 28, 6, 18), (9, 28, 10, 2)],
        "trait": "変革と力強さ。既存の枠を壊し新しい道を切り開く。",
        "element": "火",
        "color": "赤黒",
        "stone": "カーネリアン",
    },
    {
        "name": "バステト",
        "dates": [(7, 14, 7, 28), (9, 23, 9, 27), (10, 3, 10, 17)],
        "trait": "喜びと保護。優雅さと機敏さを兼ね備え、家庭を守る。",
        "element": "水",
        "color": "ピンク",
        "stone": "ムーンストーン",
    },
    {
        "name": "セクメト",
        "dates": [(7, 29, 8, 11), (10, 30, 11, 7)],
        "trait": "情熱と治癒の力。強い意志と癒しの二面性を持つ。",
        "element": "火",
        "color": "オレンジ",
        "stone": "サンストーン",
    },
    {
        "name": "ナイル",
        "dates": [(1, 8, 1, 21), (2, 1, 2, 11)],
        "trait": "流れのように柔軟で適応力が高い。新しい始まりをもたらす。",
        "element": "水",
        "color": "青緑",
        "stone": "アクアマリン",
    },
]


def _match_date_range(month: int, day: int, sm: int, sd: int, em: int, ed: int) -> bool:
    """Check if month/day falls within a date range (no year-wrapping in Egyptian)."""
    target = month * 100 + day
    start = sm * 100 + sd
    end = em * 100 + ed
    if start <= end:
        return start <= target <= end
    # Year-wrapping range (should not occur in Egyptian, but handle defensively)
    return target >= start or target <= end


def _find_god(month: int, day: int) -> dict | None:
    """Find the Egyptian god for a given birth month and day."""
    for god in EGYPTIAN_GODS:
        for sm, sd, em, ed in god["dates"]:
            if _match_date_range(month, day, sm, sd, em, ed):
                return god
    return None


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date
    god = _find_god(bd.month, bd.day)

    if god is None:
        return DivinationResult(
            system_name="エジプト占星術",
            system_id="egyptian",
            summary="該当する守護神が見つかりませんでした",
            details={"birth_month": bd.month, "birth_day": bd.day},
            interpretation="入力された誕生日に対応するエジプトの守護神が特定できませんでした。",
            warnings=["該当する守護神が見つかりません"],
        )

    return DivinationResult(
        system_name="エジプト占星術",
        system_id="egyptian",
        summary=f"守護神: {god['name']}",
        details={
            "god_name": god["name"],
            "trait": god["trait"],
            "element": god["element"],
            "sacred_color": god["color"],
            "power_stone": god["stone"],
            "birth_month": bd.month,
            "birth_day": bd.day,
        },
        interpretation=(
            f"あなたの守護神は{god['name']}です。\n"
            f"性質: {god['trait']}\n"
            f"守護元素: {god['element']} / 聖なる色: {god['color']} / 力の石: {god['stone']}"
        ),
    )
