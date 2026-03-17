"""数秘術（ピタゴラス式ヌメロロジー）"""
from datetime import date
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


MASTER_NUMBERS = {11, 22, 33}

LIFE_PATH_MEANINGS = {
    1: "リーダーシップ・独立・開拓精神。自分の道を切り開く先駆者。",
    2: "協調・調和・パートナーシップ。人と人をつなぐ橋渡し役。",
    3: "創造性・表現力・社交性。芸術的才能と喜びを広げる人。",
    4: "安定・堅実・努力。確実な基盤を築く実務家。",
    5: "自由・変化・冒険。多様な経験を通じて成長する人。",
    6: "愛情・責任・奉仕。家庭やコミュニティを守る人。",
    7: "探究・内省・精神性。真理を追い求める思索家。",
    8: "達成・権威・豊かさ。物質的・精神的成功を目指す人。",
    9: "博愛・完成・叡智。人類への奉仕と精神的完成を目指す人。",
    11: "【マスターナンバー】直感・霊感・啓示。高い理想とビジョンを持つ人。",
    22: "【マスターナンバー】大規模建設・実現力。壮大なビジョンを形にする人。",
    33: "【マスターナンバー】無条件の愛・癒し。高次の奉仕と慈悲の人。",
}


def _reduce_to_single(n: int) -> int:
    """数字を1桁に還元する（マスターナンバーは保持）"""
    while n > 9 and n not in MASTER_NUMBERS:
        n = sum(int(d) for d in str(n))
    return n


def _life_path_number(birth_date: date) -> int:
    """ライフパスナンバーを算出"""
    y = _reduce_to_single(sum(int(d) for d in str(birth_date.year)))
    m = _reduce_to_single(birth_date.month)
    d = _reduce_to_single(birth_date.day)
    total = y + m + d
    return _reduce_to_single(total)


def _birthday_number(day: int) -> int:
    """バースデーナンバー（生まれた日を還元）"""
    return _reduce_to_single(day)


def _personal_year(birth_date: date, target_year: int = None) -> int:
    """パーソナルイヤーナンバー"""
    if target_year is None:
        target_year = date.today().year
    m = _reduce_to_single(birth_date.month)
    d = _reduce_to_single(birth_date.day)
    y = _reduce_to_single(sum(int(c) for c in str(target_year)))
    return _reduce_to_single(m + d + y)


def _pinnacle_numbers(birth_date: date) -> list[dict]:
    """ピナクルナンバー（4つの人生の頂点期）"""
    m = _reduce_to_single(birth_date.month)
    d = _reduce_to_single(birth_date.day)
    y = _reduce_to_single(sum(int(c) for c in str(birth_date.year)))
    lp = _life_path_number(birth_date)

    first_end = 36 - lp
    pinnacles = [
        {"period": f"誕生〜{first_end}歳", "number": _reduce_to_single(m + d)},
        {"period": f"{first_end}歳〜{first_end + 9}歳", "number": _reduce_to_single(d + y)},
        {"period": f"{first_end + 9}歳〜{first_end + 18}歳", "number": _reduce_to_single(_reduce_to_single(m + d) + _reduce_to_single(d + y))},
        {"period": f"{first_end + 18}歳〜", "number": _reduce_to_single(m + y)},
    ]
    return pinnacles


def _challenge_numbers(birth_date: date) -> list[int]:
    """チャレンジナンバー"""
    m = _reduce_to_single(birth_date.month)
    d = _reduce_to_single(birth_date.day)
    y = _reduce_to_single(sum(int(c) for c in str(birth_date.year)))
    c1 = abs(m - d)
    c2 = abs(d - y)
    c3 = abs(c1 - c2)
    c4 = abs(m - y)
    return [c1, c2, c3, c4]


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date
    lp = _life_path_number(bd)
    bn = _birthday_number(bd.day)
    py = _personal_year(bd)
    pinnacles = _pinnacle_numbers(bd)
    challenges = _challenge_numbers(bd)

    meaning = LIFE_PATH_MEANINGS.get(lp, "")

    return DivinationResult(
        system_name="数秘術（ピタゴラス式）",
        system_id="numerology",
        summary=f"ライフパスナンバー: {lp}",
        details={
            "life_path_number": lp,
            "life_path_meaning": meaning,
            "birthday_number": bn,
            "personal_year": py,
            "personal_year_target": date.today().year,
            "pinnacle_numbers": pinnacles,
            "challenge_numbers": challenges,
            "is_master_number": lp in MASTER_NUMBERS,
        },
        interpretation=f"ライフパスナンバー {lp}: {meaning}\n"
                       f"バースデーナンバー {bn}: 生まれ持った才能と資質を示します。\n"
                       f"パーソナルイヤー {py}: {date.today().year}年のテーマです。",
    )
