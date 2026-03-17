"""ケルト占星術（木の占い・21種）"""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


CELTIC_TREES = [
    {
        "name": "バーチ（白樺）",
        "dates": [(12, 24, 1, 20)],
        "ogham": "ベイス",
        "trait": "新しい始まり・浄化・リーダーシップ",
    },
    {
        "name": "ローワン（ナナカマド）",
        "dates": [(1, 21, 2, 17)],
        "ogham": "ルイス",
        "trait": "ビジョン・保護・インスピレーション",
    },
    {
        "name": "アッシュ（トネリコ）",
        "dates": [(2, 18, 3, 17)],
        "ogham": "ニオン",
        "trait": "想像力・直感・内なる世界",
    },
    {
        "name": "アルダー（ハンノキ）",
        "dates": [(3, 18, 4, 14)],
        "ogham": "フェアン",
        "trait": "勇気・情熱・先見の明",
    },
    {
        "name": "ウィロー（柳）",
        "dates": [(4, 15, 5, 12)],
        "ogham": "サーユ",
        "trait": "感受性・直感・月のリズム",
    },
    {
        "name": "ホーソン（サンザシ）",
        "dates": [(5, 13, 6, 9)],
        "ogham": "ウアス",
        "trait": "矛盾の統合・忍耐・浄化",
    },
    {
        "name": "オーク（樫）",
        "dates": [(6, 10, 7, 7)],
        "ogham": "ドゥイル",
        "trait": "強さ・持久力・王者の気質",
    },
    {
        "name": "ホリー（柊）",
        "dates": [(7, 8, 8, 4)],
        "ogham": "ティンネ",
        "trait": "指導力・戦いの精神・王権",
    },
    {
        "name": "ヘーゼル（ハシバミ）",
        "dates": [(8, 5, 9, 1)],
        "ogham": "コル",
        "trait": "知恵・詩的才能・直感",
    },
    {
        "name": "ヴァイン（葡萄）",
        "dates": [(9, 2, 9, 29)],
        "ogham": "ムイン",
        "trait": "予言・感情の深さ・変容",
    },
    {
        "name": "アイビー（蔦）",
        "dates": [(9, 30, 10, 27)],
        "ogham": "ゲタル",
        "trait": "回復力・粘り強さ・螺旋的成長",
    },
    {
        "name": "リード（葦）",
        "dates": [(10, 28, 11, 24)],
        "ogham": "エイドル",
        "trait": "調和・直接性・秘密の知識",
    },
    {
        "name": "エルダー（ニワトコ）",
        "dates": [(11, 25, 12, 23)],
        "ogham": "ルイス",
        "trait": "変容・再生・妖精の木",
    },
]


def _match_date_range(month: int, day: int, sm: int, sd: int, em: int, ed: int) -> bool:
    """Check if month/day falls within a date range, handling year-wrapping."""
    target = month * 100 + day
    start = sm * 100 + sd
    end = em * 100 + ed
    if start <= end:
        return start <= target <= end
    # Year-wrapping (e.g., 12/24 - 1/20)
    return target >= start or target <= end


def _find_tree(month: int, day: int) -> dict | None:
    """Find the Celtic tree for a given birth month and day."""
    for tree in CELTIC_TREES:
        for sm, sd, em, ed in tree["dates"]:
            if _match_date_range(month, day, sm, sd, em, ed):
                return tree
    return None


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date
    tree = _find_tree(bd.month, bd.day)

    if tree is None:
        return DivinationResult(
            system_name="ケルト占星術（木の占い）",
            system_id="celtic_tree",
            summary="該当する守護樹が見つかりませんでした",
            details={"birth_month": bd.month, "birth_day": bd.day},
            interpretation="入力された誕生日に対応するケルトの守護樹が特定できませんでした。",
            warnings=["該当する守護樹が見つかりません"],
        )

    return DivinationResult(
        system_name="ケルト占星術（木の占い）",
        system_id="celtic_tree",
        summary=f"守護樹: {tree['name']}",
        details={
            "tree_name": tree["name"],
            "ogham_name": tree["ogham"],
            "trait": tree["trait"],
            "birth_month": bd.month,
            "birth_day": bd.day,
        },
        interpretation=(
            f"あなたの守護樹は{tree['name']}です。\n"
            f"オガム文字: {tree['ogham']}\n"
            f"性質: {tree['trait']}"
        ),
    )
