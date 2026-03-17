"""誕生数秘（バースデーナンバー）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult

MASTER_NUMBERS = {11, 22}

BIRTHDAY_MEANINGS = {
    1: "独立心・リーダーシップ・パイオニア精神",
    2: "協調性・外交力・パートナーシップ",
    3: "表現力・創造性・社交性",
    4: "安定・実務力・組織力",
    5: "自由・変化・冒険心",
    6: "責任感・愛情・家庭性",
    7: "分析力・探究心・内省",
    8: "実行力・ビジネスセンス・成功志向",
    9: "博愛・理想主義・完成",
    11: "直感力・霊性・インスピレーション【マスターナンバー】",
    22: "大器・建設力・グローバルな視点【マスターナンバー】",
}


def calculate(birth_data: BirthData) -> DivinationResult:
    day = birth_data.birth_date.day

    # まず桁を足す。結果がマスターナンバーなら保持
    number = day
    while number > 9 and number not in MASTER_NUMBERS:
        number = sum(int(d) for d in str(number))

    meaning = BIRTHDAY_MEANINGS.get(number, "")

    return DivinationResult(
        system_name="誕生数秘（バースデーナンバー）",
        system_id="birthday_number",
        summary=f"バースデーナンバー: {number}",
        details={
            "birth_day": day,
            "birthday_number": number,
            "is_master_number": number in MASTER_NUMBERS,
        },
        interpretation=f"バースデーナンバー {number}: {meaning}\n"
                       f"（誕生日の{day}日から算出）",
    )
