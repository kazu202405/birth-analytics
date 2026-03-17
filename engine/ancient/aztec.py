"""アステカ占星術（20デイサイン）"""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


# Base date: 1970-01-01 = sign index 4 (Coatl), trecena 1
_BASE_DATE = date(1970, 1, 1)
_BASE_SIGN_INDEX = 4
_BASE_TRECENA = 1

AZTEC_SIGNS = [
    {"name": "ワニ (Cipactli)", "trait": "始まり・エネルギー・積極性", "guardian": "トナカテクトリ"},
    {"name": "風 (Ehecatl)", "trait": "変化・自由・コミュニケーション", "guardian": "ケツァルコアトル"},
    {"name": "家 (Calli)", "trait": "安定・家庭・内省", "guardian": "テペヨロトル"},
    {"name": "トカゲ (Cuetzpalin)", "trait": "豊穣・活力・逆境に強い", "guardian": "ウェウェコヨトル"},
    {"name": "蛇 (Coatl)", "trait": "知恵・変容・治癒", "guardian": "チャルチウトリクエ"},
    {"name": "死 (Miquiztli)", "trait": "再生・変革・精神性", "guardian": "テクシステカトル"},
    {"name": "鹿 (Mazatl)", "trait": "優美・敏捷・自然との調和", "guardian": "トラロック"},
    {"name": "兎 (Tochtli)", "trait": "豊穣・多才・冒険心", "guardian": "マヤウェル"},
    {"name": "水 (Atl)", "trait": "感情・浄化・適応力", "guardian": "シウテクトリ"},
    {"name": "犬 (Itzcuintli)", "trait": "忠誠・導き・あの世との繋がり", "guardian": "ミクトランテクトリ"},
    {"name": "猿 (Ozomatli)", "trait": "芸術・遊び・創造性", "guardian": "ショチピリ"},
    {"name": "草 (Malinalli)", "trait": "粘り強さ・回復力・生命力", "guardian": "パテカトル"},
    {"name": "葦 (Acatl)", "trait": "権威・正義・知識", "guardian": "テスカトリポカ"},
    {"name": "ジャガー (Ocelotl)", "trait": "勇気・神秘・内なる力", "guardian": "トラルテクトリ"},
    {"name": "鷲 (Cuauhtli)", "trait": "自由・視野の広さ・精神的高み", "guardian": "シペトテック"},
    {"name": "禿鷹 (Cozcacuauhtli)", "trait": "長寿・知恵・浄化", "guardian": "イツパパロトル"},
    {"name": "地震 (Ollin)", "trait": "動き・変化・宇宙の力", "guardian": "ショロトル"},
    {"name": "火打石 (Tecpatl)", "trait": "決断力・犠牲・正義", "guardian": "テスカトリポカ"},
    {"name": "雨 (Quiahuitl)", "trait": "浄化・豊穣・感情の解放", "guardian": "トナティウ"},
    {"name": "花 (Xochitl)", "trait": "美・芸術・愛・喜び", "guardian": "ショチケツァル"},
]

# Directional associations for each sign (cycle of 4)
_DIRECTIONS = ["東", "北", "西", "南"]


def _compute_sign_and_trecena(birth_date: date) -> tuple[int, int]:
    """Compute Aztec day sign index and trecena number from birth date."""
    days_diff = (birth_date - _BASE_DATE).days
    sign_index = (days_diff + _BASE_SIGN_INDEX) % 20
    trecena = (days_diff + _BASE_TRECENA) % 13 + 1
    return sign_index, trecena


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date
    sign_index, trecena = _compute_sign_and_trecena(bd)
    sign = AZTEC_SIGNS[sign_index]
    direction = _DIRECTIONS[sign_index % 4]

    return DivinationResult(
        system_name="アステカ占星術",
        system_id="aztec",
        summary=f"デイサイン: {sign['name']} / トレセーナ: {trecena}",
        details={
            "sign_index": sign_index,
            "sign_name": sign["name"],
            "trecena": trecena,
            "guardian": sign["guardian"],
            "trait": sign["trait"],
            "direction": direction,
            "tonalpohualli": f"{trecena} {sign['name']}",
        },
        interpretation=(
            f"あなたのデイサインは{sign['name']}です。\n"
            f"トレセーナ（13日周期）: {trecena}\n"
            f"トナルポワリ暦: {trecena} {sign['name']}\n"
            f"守護神: {sign['guardian']}\n"
            f"方角: {direction}\n"
            f"性質: {sign['trait']}"
        ),
    )
