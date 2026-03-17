"""六星占術（ろくせいせんじゅつ）— 細木数子提唱の運命学"""
import sys
import os
import calendar
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


# 六星 (6 destiny stars)
STARS = ["土星人", "金星人", "火星人", "天王星人", "木星人", "水星人"]

STAR_TRAITS = {
    "土星人": {
        "element": "土",
        "keyword": "現実・努力・忍耐",
        "personality": "堅実で努力家。現実的な思考を持ち、コツコツと積み上げることで大きな成果を得る。"
                       "責任感が強く、信頼される存在。慎重さが長所だが、変化を恐れる傾向も。",
        "strength": "持続力・計画性・信頼性",
        "weakness": "頑固・変化への抵抗・心配性",
    },
    "金星人": {
        "element": "金",
        "keyword": "美・調和・社交",
        "personality": "華やかで社交的。美的感覚に優れ、人間関係を大切にする。"
                       "バランス感覚が良く、周囲との調和を保つ能力がある。繊細で傷つきやすい面も。",
        "strength": "社交性・美的感覚・協調性",
        "weakness": "優柔不断・依存心・見栄",
    },
    "火星人": {
        "element": "火",
        "keyword": "情熱・行動・リーダーシップ",
        "personality": "行動力に溢れ、情熱的。リーダーシップを発揮し、周囲を引っ張る力を持つ。"
                       "直感が鋭く、決断力がある。せっかちで短気な面に注意。",
        "strength": "行動力・決断力・カリスマ性",
        "weakness": "短気・独断的・飽きやすい",
    },
    "天王星人": {
        "element": "天",
        "keyword": "独創・自由・革新",
        "personality": "独創的で自由を愛する。既成概念にとらわれず、新しい発想で道を切り開く。"
                       "個性的で魅力的だが、周囲との協調が課題になることも。",
        "strength": "独創性・直感力・先見性",
        "weakness": "わがまま・孤立・気分屋",
    },
    "木星人": {
        "element": "木",
        "keyword": "成長・知性・誠実",
        "personality": "知性的で向上心が強い。誠実な人柄で信頼を集め、着実に成長していく。"
                       "学ぶことが好きで、幅広い知識を持つ。理屈っぽくなりがちな面も。",
        "strength": "知性・誠実さ・向上心",
        "weakness": "理屈っぽい・頑固・プライドが高い",
    },
    "水星人": {
        "element": "水",
        "keyword": "柔軟・適応・感受性",
        "personality": "柔軟性があり適応力が高い。感受性豊かで、人の気持ちを理解する能力に優れる。"
                       "水のように自在に形を変え、どんな環境にも馴染む。流されやすい面に注意。",
        "strength": "適応力・共感力・柔軟性",
        "weakness": "優柔不断・流されやすい・自己主張が弱い",
    },
}

# 12年運命周期
CYCLE_12 = [
    "種子", "緑生", "立花", "健弱", "達成", "乱気",
    "再会", "財成", "安定", "陰影", "停止", "減退",
]

CYCLE_DESCRIPTIONS = {
    "種子": "新しい運命の始まり。可能性の種を蒔く時期。積極的に新しいことに挑戦すると吉。",
    "緑生": "芽生えの時期。種子期に蒔いた種が芽を出し始める。焦らず育てることが大切。",
    "立花": "開花の時期。才能や努力が花開く。自信を持って前に進む時。",
    "健弱": "小休止の時期。体調に注意し、無理をせず内面の充実を図る。",
    "達成": "実りの時期。これまでの努力が結実する最高の運気。チャンスを逃さずに。",
    "乱気": "変動の時期。予想外の出来事が起きやすい。冷静な判断が重要。",
    "再会": "再出発の時期。過去の縁や経験が新たな形で活きる。人間関係の見直しに最適。",
    "財成": "蓄積の時期。経済面・精神面ともに豊かになる。将来への投資に適する。",
    "安定": "穏やかな時期。安定した運気の中で、次のステップの準備をする。",
    "陰影": "大殺界・入口。運気が下降し始める。新しいことは控え、守りの姿勢で。",
    "停止": "大殺界・中心。最も運気が低迷する時期。忍耐と自己研鑽の時。",
    "減退": "大殺界・出口。試練の終わりが見え始める。回復に向けて心身を整える。",
}


def _fate_number(year: int, month: int, day: int) -> int:
    """運命数を計算する。

    年の干支的な基数と、年内の日数を合算して運命数を求める。
    """
    # 年ごとの基数: 元日からの通算日数を61周期で算出
    year_val = (
        (year - 1) * 365
        + (year - 1) // 4
        - (year - 1) // 100
        + (year - 1) // 400
    ) % 61 + 1

    # 誕生日の年内通算日数
    is_leap = calendar.isleap(year)
    days_in_month = [
        0, 31, 28 + (1 if is_leap else 0), 31, 30, 31, 30,
        31, 31, 30, 31, 30, 31,
    ]
    day_of_year = sum(days_in_month[1:month]) + day

    fate = (year_val + day_of_year) % 61
    if fate == 0:
        fate = 61
    return fate


def _get_star_index(fate: int) -> int:
    """運命数から六星のインデックスを返す (0-5)。"""
    if fate <= 10:
        return 0
    elif fate <= 20:
        return 1
    elif fate <= 30:
        return 2
    elif fate <= 40:
        return 3
    elif fate <= 50:
        return 4
    else:
        return 5


def _get_polarity(fate: int) -> str:
    """運命数の奇偶から霊合星人かどうか (+/-) を判定する。"""
    return "+" if fate % 2 != 0 else "-"


def _get_cycle_position(year: int, fate: int) -> int:
    """指定年の12年周期における位置を返す (0-11)。"""
    # 運命数を基に12年周期の開始年を算出
    return (year + fate) % 12


def calculate(birth_data: BirthData) -> DivinationResult:
    """六星占術の鑑定を行う。"""
    bd = birth_data.birth_date
    fate = _fate_number(bd.year, bd.month, bd.day)
    star_idx = _get_star_index(fate)
    star_name = STARS[star_idx]
    polarity = _get_polarity(fate)
    polarity_label = "陽" if polarity == "+" else "陰"

    full_star = f"{star_name}（{polarity_label}）"
    traits = STAR_TRAITS[star_name]

    # 今年の12年周期位置
    current_year = date.today().year
    cycle_pos = _get_cycle_position(current_year, fate)
    current_cycle = CYCLE_12[cycle_pos]
    cycle_desc = CYCLE_DESCRIPTIONS[current_cycle]

    # 大殺界判定
    is_daisatsugai = current_cycle in ("陰影", "停止", "減退")
    warnings = []
    if is_daisatsugai:
        warnings.append(
            f"現在「{current_cycle}」の時期（大殺界）です。"
            "新規事業や大きな決断は慎重に。守りの姿勢が吉。"
        )

    # 来年以降3年分の周期予測
    forecast = {}
    for offset in range(1, 4):
        future_year = current_year + offset
        future_pos = _get_cycle_position(future_year, fate)
        future_cycle = CYCLE_12[future_pos]
        forecast[str(future_year)] = {
            "cycle": future_cycle,
            "description": CYCLE_DESCRIPTIONS[future_cycle],
        }

    return DivinationResult(
        system_name="六星占術",
        system_id="rokusei",
        summary=f"{full_star} / {current_year}年の運命周期: {current_cycle}",
        details={
            "fate_number": fate,
            "star": star_name,
            "polarity": polarity_label,
            "full_star": full_star,
            "element": traits["element"],
            "keyword": traits["keyword"],
            "strength": traits["strength"],
            "weakness": traits["weakness"],
            "current_year": current_year,
            "cycle_position": current_cycle,
            "cycle_description": cycle_desc,
            "is_daisatsugai": is_daisatsugai,
            "forecast_3years": forecast,
        },
        interpretation=(
            f"あなたの六星は「{full_star}」です。\n\n"
            f"【性格】{traits['personality']}\n\n"
            f"【長所】{traits['strength']}\n"
            f"【短所】{traits['weakness']}\n\n"
            f"【{current_year}年の運命周期】{current_cycle}\n"
            f"{cycle_desc}"
        ),
        warnings=warnings,
    )
