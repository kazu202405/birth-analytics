"""誕生日カラー — 月・数秘・星座から総合的なパーソナルカラーを算出"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult
from utils.constants import ZODIAC_SIGNS, ZODIAC_START_DATES


MONTH_COLORS = {
    1: {"name": "ガーネットレッド", "hex": "#9B2335", "meaning": "情熱・勇気・新たな始まり"},
    2: {"name": "アメジストパープル", "hex": "#6B3FA0", "meaning": "直感・精神性・高貴"},
    3: {"name": "アクアマリンブルー", "hex": "#7FCDCD", "meaning": "清浄・勇気・幸福"},
    4: {"name": "ダイヤモンドホワイト", "hex": "#F0F0F0", "meaning": "純粋・永遠・強さ"},
    5: {"name": "エメラルドグリーン", "hex": "#50C878", "meaning": "成長・調和・再生"},
    6: {"name": "パールホワイト", "hex": "#F5F5DC", "meaning": "純真・知恵・月の力"},
    7: {"name": "ルビーレッド", "hex": "#E0115F", "meaning": "愛・活力・王者の力"},
    8: {"name": "ペリドットグリーン", "hex": "#B4C424", "meaning": "太陽の力・豊穣・保護"},
    9: {"name": "サファイアブルー", "hex": "#0F52BA", "meaning": "真実・知恵・神聖"},
    10: {"name": "オパールホワイト", "hex": "#A8C3BC", "meaning": "希望・創造性・多面性"},
    11: {"name": "トパーズゴールド", "hex": "#FFC87C", "meaning": "友情・知性・温かさ"},
    12: {"name": "タンザナイトブルー", "hex": "#3B2F8A", "meaning": "変容・直感・覚醒"},
}

# 数秘ナンバー -> チャクラカラー
NUMEROLOGY_COLORS = {
    1: {"name": "レッド", "hex": "#FF0000", "chakra": "ルートチャクラ", "meaning": "行動力・生命力"},
    2: {"name": "オレンジ", "hex": "#FF8C00", "chakra": "サクラルチャクラ", "meaning": "感受性・創造性"},
    3: {"name": "イエロー", "hex": "#FFD700", "chakra": "ソーラープレクサスチャクラ", "meaning": "自信・表現力"},
    4: {"name": "グリーン", "hex": "#228B22", "chakra": "ハートチャクラ", "meaning": "安定・調和"},
    5: {"name": "ブルー", "hex": "#4169E1", "chakra": "スロートチャクラ", "meaning": "自由・コミュニケーション"},
    6: {"name": "インディゴ", "hex": "#4B0082", "chakra": "サードアイチャクラ", "meaning": "愛情・洞察力"},
    7: {"name": "バイオレット", "hex": "#8B00FF", "chakra": "クラウンチャクラ", "meaning": "霊性・内省"},
    8: {"name": "ローズゴールド", "hex": "#B76E79", "chakra": "ハイハートチャクラ", "meaning": "達成・豊かさ"},
    9: {"name": "ゴールド", "hex": "#FFD700", "chakra": "ソウルスターチャクラ", "meaning": "叡智・完成"},
}

# 星座カラー
ZODIAC_COLORS = {
    "牡羊座": {"name": "レッド", "hex": "#FF0000", "meaning": "情熱・開拓精神"},
    "牡牛座": {"name": "グリーン", "hex": "#228B22", "meaning": "豊かさ・安定"},
    "双子座": {"name": "イエロー", "hex": "#FFD700", "meaning": "知性・コミュニケーション"},
    "蟹座": {"name": "シルバー", "hex": "#C0C0C0", "meaning": "感受性・母性"},
    "獅子座": {"name": "ゴールド", "hex": "#FFD700", "meaning": "威厳・創造性"},
    "乙女座": {"name": "ネイビー", "hex": "#000080", "meaning": "分析力・誠実さ"},
    "天秤座": {"name": "ピンク", "hex": "#FF69B4", "meaning": "美・調和"},
    "蠍座": {"name": "ダークレッド", "hex": "#8B0000", "meaning": "深い情念・変容"},
    "射手座": {"name": "パープル", "hex": "#800080", "meaning": "冒険・哲学"},
    "山羊座": {"name": "ダークブラウン", "hex": "#654321", "meaning": "堅実・伝統"},
    "水瓶座": {"name": "エレクトリックブルー", "hex": "#7DF9FF", "meaning": "革新・独創性"},
    "魚座": {"name": "シーグリーン", "hex": "#2E8B57", "meaning": "直感・共感"},
}


def _get_zodiac_sign(month: int, day: int) -> str:
    """西洋星座を取得"""
    for i in range(len(ZODIAC_START_DATES)):
        start_m, start_d = ZODIAC_START_DATES[i]
        next_m, next_d = ZODIAC_START_DATES[(i + 1) % 12]

        if start_m <= next_m:
            if (month == start_m and day >= start_d) or (month > start_m and month < next_m) or (month == next_m and day < next_d):
                return ZODIAC_SIGNS[i]
        else:
            if (month == start_m and day >= start_d) or month > start_m or month < next_m or (month == next_m and day < next_d):
                return ZODIAC_SIGNS[i]
    return ZODIAC_SIGNS[0]


def _calc_life_path(year: int, month: int, day: int) -> int:
    """ライフパスナンバーを算出（1-9）"""
    total = sum(int(d) for d in str(year)) + sum(int(d) for d in str(month)) + sum(int(d) for d in str(day))
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date
    month = bd.month
    day = bd.day

    # 1. 月の誕生石カラー
    month_color = MONTH_COLORS[month]

    # 2. 数秘カラー
    life_path = _calc_life_path(bd.year, month, day)
    numerology_color = NUMEROLOGY_COLORS[life_path]

    # 3. 星座カラー
    zodiac = _get_zodiac_sign(month, day)
    zodiac_color = ZODIAC_COLORS[zodiac]

    details = {
        "month_color": {
            "name": month_color["name"],
            "hex": month_color["hex"],
            "meaning": month_color["meaning"],
        },
        "numerology_color": {
            "life_path_number": life_path,
            "name": numerology_color["name"],
            "hex": numerology_color["hex"],
            "chakra": numerology_color["chakra"],
            "meaning": numerology_color["meaning"],
        },
        "zodiac_color": {
            "zodiac": zodiac,
            "name": zodiac_color["name"],
            "hex": zodiac_color["hex"],
            "meaning": zodiac_color["meaning"],
        },
    }

    interpretation = (
        f"【誕生月カラー】{month_color['name']}（{month_color['hex']}）\n"
        f"  {month_color['meaning']}\n\n"
        f"【数秘カラー】{numerology_color['name']}（{numerology_color['hex']}）\n"
        f"  ライフパスナンバー{life_path} = {numerology_color['chakra']}\n"
        f"  {numerology_color['meaning']}\n\n"
        f"【星座カラー】{zodiac_color['name']}（{zodiac_color['hex']}）— {zodiac}\n"
        f"  {zodiac_color['meaning']}\n\n"
        f"これら3つのカラーがあなたの誕生日に宿るエネルギーを表しています。\n"
        f"身に着けるアクセサリーやインテリアに取り入れることで、運気の向上が期待できます。"
    )

    return DivinationResult(
        system_name="誕生日カラー",
        system_id="birthday_color",
        summary=f"誕生月: {month_color['name']} / 数秘: {numerology_color['name']} / 星座: {zodiac_color['name']}",
        details=details,
        interpretation=interpretation,
    )
