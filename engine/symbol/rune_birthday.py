"""ルーン誕生日（エルダー・フサルク24ルーン）"""
from datetime import date
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


ELDER_FUTHARK = [
    {"name": "フェフ (Fehu)", "letter": "ᚠ", "meaning": "富・豊穣・新しい始まり", "period": (6, 29, 7, 14), "aett": "フレイヤのアット"},
    {"name": "ウルズ (Uruz)", "letter": "ᚢ", "meaning": "力・健康・野性の力", "period": (7, 14, 7, 29), "aett": "フレイヤのアット"},
    {"name": "スリサズ (Thurisaz)", "letter": "ᚦ", "meaning": "守護・防御・反応力", "period": (7, 29, 8, 13), "aett": "フレイヤのアット"},
    {"name": "アンスズ (Ansuz)", "letter": "ᚨ", "meaning": "知恵・コミュニケーション・啓示", "period": (8, 13, 8, 29), "aett": "フレイヤのアット"},
    {"name": "ライゾ (Raidho)", "letter": "ᚱ", "meaning": "旅・リズム・正しい道", "period": (8, 29, 9, 13), "aett": "フレイヤのアット"},
    {"name": "ケナズ (Kenaz)", "letter": "ᚲ", "meaning": "知識・創造の火・技術", "period": (9, 13, 9, 28), "aett": "フレイヤのアット"},
    {"name": "ギーボ (Gebo)", "letter": "ᚷ", "meaning": "贈り物・パートナーシップ・均衡", "period": (9, 28, 10, 13), "aett": "フレイヤのアット"},
    {"name": "ウンジョ (Wunjo)", "letter": "ᚹ", "meaning": "喜び・調和・願望成就", "period": (10, 13, 10, 28), "aett": "フレイヤのアット"},
    {"name": "ハガラズ (Hagalaz)", "letter": "ᚺ", "meaning": "破壊と再生・自然の力・変容", "period": (10, 28, 11, 13), "aett": "ハガルのアット"},
    {"name": "ナウシズ (Nauthiz)", "letter": "ᚾ", "meaning": "必要性・忍耐・制約からの学び", "period": (11, 13, 11, 28), "aett": "ハガルのアット"},
    {"name": "イサ (Isa)", "letter": "ᛁ", "meaning": "停止・集中・内省", "period": (11, 28, 12, 13), "aett": "ハガルのアット"},
    {"name": "イェラ (Jera)", "letter": "ᛃ", "meaning": "収穫・サイクル・正当な報酬", "period": (12, 13, 12, 28), "aett": "ハガルのアット"},
    {"name": "エイワズ (Eihwaz)", "letter": "ᛇ", "meaning": "防御・持久力・生と死の架け橋", "period": (12, 28, 1, 13), "aett": "ハガルのアット"},
    {"name": "ペルス (Perthro)", "letter": "ᛈ", "meaning": "運命・神秘・隠された力", "period": (1, 13, 1, 28), "aett": "ハガルのアット"},
    {"name": "エルハズ (Algiz)", "letter": "ᛉ", "meaning": "守護・本能・精神的な盾", "period": (1, 28, 2, 13), "aett": "ハガルのアット"},
    {"name": "ソウィロ (Sowilo)", "letter": "ᛊ", "meaning": "太陽・勝利・生命力", "period": (2, 13, 2, 27), "aett": "ハガルのアット"},
    {"name": "ティワズ (Tiwaz)", "letter": "ᛏ", "meaning": "正義・勇気・自己犠牲", "period": (2, 27, 3, 14), "aett": "ティールのアット"},
    {"name": "ベルカナ (Berkano)", "letter": "ᛒ", "meaning": "誕生・成長・母性", "period": (3, 14, 3, 30), "aett": "ティールのアット"},
    {"name": "エワズ (Ehwaz)", "letter": "ᛖ", "meaning": "信頼・協力・進歩", "period": (3, 30, 4, 14), "aett": "ティールのアット"},
    {"name": "マンナズ (Mannaz)", "letter": "ᛗ", "meaning": "人間性・知性・自己認識", "period": (4, 14, 4, 29), "aett": "ティールのアット"},
    {"name": "ラグズ (Laguz)", "letter": "ᛚ", "meaning": "水・直感・潜在意識", "period": (4, 29, 5, 14), "aett": "ティールのアット"},
    {"name": "イングワズ (Ingwaz)", "letter": "ᛝ", "meaning": "豊穣・潜在力・内なる成長", "period": (5, 14, 5, 29), "aett": "ティールのアット"},
    {"name": "ダガズ (Dagaz)", "letter": "ᛞ", "meaning": "夜明け・突破・変容", "period": (5, 29, 6, 14), "aett": "ティールのアット"},
    {"name": "オシラ (Othala)", "letter": "ᛟ", "meaning": "遺産・家庭・精神的な故郷", "period": (6, 14, 6, 29), "aett": "ティールのアット"},
]


def _date_to_month_day_tuple(d: date) -> tuple[int, int]:
    """日付から (月, 日) タプルを返す。"""
    return (d.month, d.day)


def _is_in_period(month: int, day: int, period: tuple[int, int, int, int]) -> bool:
    """誕生日がルーンの期間内にあるか判定する。年をまたぐ期間にも対応。"""
    start_m, start_d, end_m, end_d = period
    target = (month, day)
    start = (start_m, start_d)
    end = (end_m, end_d)

    if start <= end:
        return start <= target < end
    else:
        # 年をまたぐ期間（例: 12/28 - 1/13）
        return target >= start or target < end


def _find_birth_rune(month: int, day: int) -> dict:
    """誕生日に対応するルーンを見つける。"""
    for rune in ELDER_FUTHARK:
        if _is_in_period(month, day, rune["period"]):
            return rune
    # フォールバック: 最も近いルーンを返す（境界日の場合）
    # 各ルーンの開始日を含み終了日を含まない設計だが、
    # 万一マッチしない場合は最後のルーンを返す
    return ELDER_FUTHARK[-1]


def _find_complementary_rune(birth_rune_index: int) -> dict:
    """補完ルーン: 対角位置（12個先）のルーンを返す。"""
    comp_index = (birth_rune_index + 12) % 24
    return ELDER_FUTHARK[comp_index]


def _get_aett_description(aett: str) -> str:
    """アットの説明を返す。"""
    descriptions = {
        "フレイヤのアット": "創造と豊穣の女神フレイヤに守護される。物質的・感情的な成長のエネルギー。",
        "ハガルのアット": "変容と試練の領域。困難を通じた精神的成長と内面の力の発見。",
        "ティールのアット": "戦いと正義の神ティールに守護される。社会的責任と精神的完成。",
    }
    return descriptions.get(aett, "")


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date
    month, day = bd.month, bd.day

    birth_rune = _find_birth_rune(month, day)
    birth_rune_index = ELDER_FUTHARK.index(birth_rune)
    complementary_rune = _find_complementary_rune(birth_rune_index)
    aett_desc = _get_aett_description(birth_rune["aett"])

    start_m, start_d, end_m, end_d = birth_rune["period"]
    period_str = f"{start_m}/{start_d} - {end_m}/{end_d}"

    return DivinationResult(
        system_name="ルーン誕生日（エルダー・フサルク）",
        system_id="rune_birthday",
        summary=f"誕生ルーン: {birth_rune['letter']} {birth_rune['name']}",
        details={
            "birth_rune": {
                "name": birth_rune["name"],
                "letter": birth_rune["letter"],
                "meaning": birth_rune["meaning"],
                "period": period_str,
                "aett": birth_rune["aett"],
                "aett_description": aett_desc,
            },
            "complementary_rune": {
                "name": complementary_rune["name"],
                "letter": complementary_rune["letter"],
                "meaning": complementary_rune["meaning"],
            },
            "rune_position": birth_rune_index + 1,
            "total_runes": 24,
        },
        interpretation=(
            f"誕生ルーン【{birth_rune['letter']} {birth_rune['name']}】: {birth_rune['meaning']}\n"
            f"所属アット【{birth_rune['aett']}】: {aett_desc}\n"
            f"補完ルーン【{complementary_rune['letter']} {complementary_rune['name']}】: "
            f"{complementary_rune['meaning']}"
        ),
    )
