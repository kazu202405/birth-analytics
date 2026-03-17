"""曜日占い"""
import calendar
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult
from utils.constants import WEEKDAYS_JP, WEEKDAY_PLANETS


WEEKDAY_TRAITS = {
    0: "月曜日生まれ: 感受性豊か・想像力が強い・繊細で直感的。月の影響で感情が豊かで人の気持ちに敏感。",
    1: "火曜日生まれ: 情熱的・行動力がある・リーダーシップ。火星の影響でエネルギッシュで勇敢。",
    2: "水曜日生まれ: 知的好奇心・コミュニケーション上手・器用。水星の影響で情報収集力と表現力に優れる。",
    3: "木曜日生まれ: 楽観的・寛大・哲学的。木星の影響で幸運に恵まれやすく、視野が広い。",
    4: "金曜日生まれ: 愛情深い・美的センス・社交的。金星の影響で人間関係に恵まれ、芸術的才能がある。",
    5: "土曜日生まれ: 忍耐強い・責任感・現実的。土星の影響で堅実で信頼される存在。",
    6: "日曜日生まれ: 明るい・リーダー気質・存在感。太陽の影響で周囲を照らし、中心的存在になりやすい。",
}


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date
    weekday = bd.weekday()  # 0=月曜, 6=日曜

    weekday_name = WEEKDAYS_JP[weekday]
    planet = WEEKDAY_PLANETS[weekday]
    traits = WEEKDAY_TRAITS[weekday]

    return DivinationResult(
        system_name="曜日占い",
        system_id="youbi_uranai",
        summary=f"{weekday_name}生まれ（守護星: {planet}）",
        details={
            "weekday": weekday_name,
            "weekday_index": weekday,
            "guardian_planet": planet,
        },
        interpretation=traits,
    )
