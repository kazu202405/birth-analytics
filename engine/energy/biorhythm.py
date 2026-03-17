"""バイオリズム（Biorhythm）— 生体リズム理論に基づく運勢診断"""
import sys
import os
import math
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


# 3つの基本リズム周期（日数）
PHYSICAL_CYCLE = 23      # 身体リズム
EMOTIONAL_CYCLE = 28     # 感情リズム
INTELLECTUAL_CYCLE = 33  # 知性リズム

# リズム状態の閾値
HIGH_THRESHOLD = 50.0
LOW_THRESHOLD = -50.0
CRITICAL_THRESHOLD = 5.0  # ゼロ付近（注意日）

RHYTHM_NAMES = {
    "physical": "身体",
    "emotional": "感情",
    "intellectual": "知性",
}

RHYTHM_DESCRIPTIONS = {
    "physical": {
        "high": "体力・持久力・免疫力が充実。スポーツや肉体労働に最適。",
        "low": "体調を崩しやすい時期。無理をせず休息を優先。",
        "critical": "身体の注意日。事故やケガに気をつけて。",
        "rising": "体調が上向いている。活動量を徐々に増やすと良い。",
        "falling": "体力が下降気味。疲労を溜めないよう注意。",
    },
    "emotional": {
        "high": "感情が安定し、人間関係が良好。創造力も高まる時期。",
        "low": "感情が不安定になりやすい。重要な人間関係の判断は控えめに。",
        "critical": "感情の注意日。感情的な判断を避け、冷静に。",
        "rising": "気分が上向いてきている。人との交流を楽しめる。",
        "falling": "感情が下降気味。一人の時間を大切に。",
    },
    "intellectual": {
        "high": "思考力・判断力・記憶力が冴える。勉強や重要な判断に最適。",
        "low": "集中力が低下しやすい。単純作業を中心に。",
        "critical": "知性の注意日。判断ミスに注意。重要な決定は避ける。",
        "rising": "頭が冴えてきている。新しい学びを始めるのに良い。",
        "falling": "思考力が下降気味。複雑な判断は先送りが吉。",
    },
}


def _calc_rhythm(days_lived: int, cycle: int) -> float:
    """指定日数とサイクルからリズム値を算出する (-100.0 ~ 100.0)。"""
    return round(math.sin(2 * math.pi * days_lived / cycle) * 100, 1)


def _rhythm_state(value: float, days_lived: int, cycle: int) -> str:
    """リズム値から状態を判定する。"""
    if abs(value) < CRITICAL_THRESHOLD:
        return "critical"
    # 微分値（翌日との差）で上昇/下降を判定
    next_value = math.sin(2 * math.pi * (days_lived + 1) / cycle) * 100
    is_rising = next_value > value

    if value > HIGH_THRESHOLD:
        return "high"
    elif value < LOW_THRESHOLD:
        return "low"
    elif is_rising:
        return "rising"
    else:
        return "falling"


def _format_percentage(value: float) -> str:
    """リズム値を表示用文字列に変換する。"""
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1f}%"


def _calc_overall(physical: float, emotional: float, intellectual: float) -> str:
    """総合状態を判定する。"""
    avg = (physical + emotional + intellectual) / 3
    if avg > 60:
        return "絶好調"
    elif avg > 30:
        return "好調"
    elif avg > 0:
        return "やや好調"
    elif avg > -30:
        return "やや低調"
    elif avg > -60:
        return "低調"
    else:
        return "要注意"


def calculate(birth_data: BirthData) -> DivinationResult:
    """バイオリズムの算出を行う。"""
    bd = birth_data.birth_date
    today = date.today()
    days_lived = (today - bd).days

    # 今日のリズム値
    physical = _calc_rhythm(days_lived, PHYSICAL_CYCLE)
    emotional = _calc_rhythm(days_lived, EMOTIONAL_CYCLE)
    intellectual = _calc_rhythm(days_lived, INTELLECTUAL_CYCLE)

    # 状態判定
    phys_state = _rhythm_state(physical, days_lived, PHYSICAL_CYCLE)
    emot_state = _rhythm_state(emotional, days_lived, EMOTIONAL_CYCLE)
    intl_state = _rhythm_state(intellectual, days_lived, INTELLECTUAL_CYCLE)

    overall = _calc_overall(physical, emotional, intellectual)

    # 注意日の検出
    critical_rhythms = []
    if phys_state == "critical":
        critical_rhythms.append("身体")
    if emot_state == "critical":
        critical_rhythms.append("感情")
    if intl_state == "critical":
        critical_rhythms.append("知性")

    warnings = []
    if critical_rhythms:
        warnings.append(
            f"本日は{' / '.join(critical_rhythms)}の注意日です。"
            "無理をせず慎重に過ごしましょう。"
        )

    # 7日間予報
    forecast_7days = []
    for offset in range(7):
        target_date = today + timedelta(days=offset)
        d = (target_date - bd).days
        p = _calc_rhythm(d, PHYSICAL_CYCLE)
        e = _calc_rhythm(d, EMOTIONAL_CYCLE)
        i = _calc_rhythm(d, INTELLECTUAL_CYCLE)

        day_critical = []
        if abs(p) < CRITICAL_THRESHOLD:
            day_critical.append("身体")
        if abs(e) < CRITICAL_THRESHOLD:
            day_critical.append("感情")
        if abs(i) < CRITICAL_THRESHOLD:
            day_critical.append("知性")

        forecast_7days.append({
            "date": target_date.isoformat(),
            "day_label": "今日" if offset == 0 else f"{offset}日後",
            "physical": p,
            "emotional": e,
            "intellectual": i,
            "overall": _calc_overall(p, e, i),
            "critical": day_critical if day_critical else None,
        })

    # 次の注意日を探す（30日以内）
    next_critical_days = []
    for offset in range(1, 31):
        d = days_lived + offset
        target_date = today + timedelta(days=offset)
        crits = []
        if abs(_calc_rhythm(d, PHYSICAL_CYCLE)) < CRITICAL_THRESHOLD:
            crits.append("身体")
        if abs(_calc_rhythm(d, EMOTIONAL_CYCLE)) < CRITICAL_THRESHOLD:
            crits.append("感情")
        if abs(_calc_rhythm(d, INTELLECTUAL_CYCLE)) < CRITICAL_THRESHOLD:
            crits.append("知性")
        if crits:
            next_critical_days.append({
                "date": target_date.isoformat(),
                "rhythms": crits,
            })

    # 解釈テキスト構築
    phys_desc = RHYTHM_DESCRIPTIONS["physical"][phys_state]
    emot_desc = RHYTHM_DESCRIPTIONS["emotional"][emot_state]
    intl_desc = RHYTHM_DESCRIPTIONS["intellectual"][intl_state]

    interpretation = (
        f"【本日のバイオリズム】総合: {overall}\n\n"
        f"身体リズム: {_format_percentage(physical)}\n"
        f"  {phys_desc}\n\n"
        f"感情リズム: {_format_percentage(emotional)}\n"
        f"  {emot_desc}\n\n"
        f"知性リズム: {_format_percentage(intellectual)}\n"
        f"  {intl_desc}"
    )

    if next_critical_days:
        interpretation += "\n\n【今後30日以内の注意日】\n"
        for cd in next_critical_days[:5]:  # 最大5件表示
            interpretation += f"  {cd['date']}: {' / '.join(cd['rhythms'])}\n"

    return DivinationResult(
        system_name="バイオリズム",
        system_id="biorhythm",
        summary=f"総合: {overall} / 身体{_format_percentage(physical)} / "
                f"感情{_format_percentage(emotional)} / 知性{_format_percentage(intellectual)}",
        details={
            "days_lived": days_lived,
            "today": today.isoformat(),
            "physical": {"value": physical, "state": phys_state},
            "emotional": {"value": emotional, "state": emot_state},
            "intellectual": {"value": intellectual, "state": intl_state},
            "overall": overall,
            "forecast_7days": forecast_7days,
            "next_critical_days": next_critical_days[:10],
        },
        interpretation=interpretation,
        warnings=warnings,
    )
