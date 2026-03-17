"""マヤ暦（13の月の暦 / ツォルキン）-- ドリームスペル方式"""
from datetime import date
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult
from utils.constants import MAYA_SOLAR_SEALS


TONE_MEANINGS = {
    1: "磁気の音 -- 目的を引きつける・統一",
    2: "月の音 -- 挑戦を安定させる・二極性",
    3: "電気の音 -- 奉仕を活性化する・つなげる",
    4: "自己存在の音 -- 形を定義する・測る",
    5: "倍音の音 -- 力を与える・命じる",
    6: "律動の音 -- 平等を組織する・バランス",
    7: "共振の音 -- 調律する・チャネル",
    8: "銀河の音 -- 調和させる・モデルにする",
    9: "太陽の音 -- 意図を脈動させる・実現",
    10: "惑星の音 -- 現れを生み出す・完成",
    11: "スペクトルの音 -- 解放する・溶かす",
    12: "水晶の音 -- 協力を捧げる・普遍化",
    13: "宇宙の音 -- 存在を超越する・持ちこたえる",
}

SEAL_COLORS = {0: "赤", 1: "白", 2: "青", 3: "黄"}


def _calc_kin(birth_date: date) -> int:
    """KINナンバーを算出（ドリームスペル方式）"""
    # 基準日: 2013-07-26 = KIN 164
    base_date = date(2013, 7, 26)
    base_kin = 164
    diff = (birth_date - base_date).days
    kin = ((diff % 260) + base_kin - 1) % 260 + 1
    return kin


def _wavespell_seal(kin: int) -> int:
    """ウェイブスペルの紋章インデックスを返す"""
    # ウェイブスペル = 13日周期の最初の紋章
    ws_start = ((kin - 1) // 13) * 13 + 1
    return (ws_start - 1) % 20


def _guide_seal(kin: int, seal: int, tone: int) -> int:
    """ガイドキンの紋章インデックスを返す"""
    guide_offsets = {1: 0, 6: 0, 11: 0,
                     2: 12, 7: 12, 12: 12,
                     3: 4, 8: 4, 13: 4,
                     4: 16, 9: 16,
                     5: 8, 10: 8}
    offset = guide_offsets.get(tone, 0)
    return (seal + offset) % 20


def _antipodal_seal(seal: int) -> int:
    """反対キンの紋章インデックス"""
    return (seal + 10) % 20


def _occult_seal(seal: int) -> int:
    """神秘キンの紋章インデックス"""
    return (19 - seal) % 20


def _analog_seal(seal: int) -> int:
    """類似キンの紋章インデックス"""
    analog_map = {
        0: 17, 1: 18, 2: 19, 3: 16, 4: 15,
        5: 14, 6: 13, 7: 12, 8: 11, 9: 10,
        10: 9, 11: 8, 12: 7, 13: 6, 14: 5,
        15: 4, 16: 3, 17: 0, 18: 1, 19: 2,
    }
    return analog_map[seal]


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date
    kin = _calc_kin(bd)

    seal_index = (kin - 1) % 20
    tone = (kin - 1) % 13 + 1
    seal_name = MAYA_SOLAR_SEALS[seal_index]
    color_index = seal_index % 4
    color = SEAL_COLORS[color_index]

    ws_index = _wavespell_seal(kin)
    guide_index = _guide_seal(kin, seal_index, tone)
    anti_index = _antipodal_seal(seal_index)
    occult_index = _occult_seal(seal_index)
    analog_index = _analog_seal(seal_index)

    return DivinationResult(
        system_name="マヤ暦（ツォルキン）",
        system_id="maya_calendar",
        summary=f"KIN {kin} {seal_name} 音{tone}",
        details={
            "kin": kin,
            "solar_seal": seal_name,
            "solar_seal_index": seal_index,
            "tone": tone,
            "tone_meaning": TONE_MEANINGS[tone],
            "color": color,
            "wavespell": MAYA_SOLAR_SEALS[ws_index],
            "guide": MAYA_SOLAR_SEALS[guide_index],
            "antipodal": MAYA_SOLAR_SEALS[anti_index],
            "occult": MAYA_SOLAR_SEALS[occult_index],
            "analog": MAYA_SOLAR_SEALS[analog_index],
        },
        interpretation=f"KIN {kin}: {seal_name} / 銀河の音 {tone}\n"
                       f"{TONE_MEANINGS[tone]}\n"
                       f"ウェイブスペル: {MAYA_SOLAR_SEALS[ws_index]}（潜在意識）\n"
                       f"ガイド: {MAYA_SOLAR_SEALS[guide_index]}（導き）\n"
                       f"反対キン: {MAYA_SOLAR_SEALS[anti_index]}（挑戦・広げる力）\n"
                       f"神秘キン: {MAYA_SOLAR_SEALS[occult_index]}（突然変異的な力）\n"
                       f"類似キン: {MAYA_SOLAR_SEALS[analog_index]}（支え合う力）",
    )
