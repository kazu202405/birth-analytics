"""十二直（じゅうにちょく）― 暦注

日本の暦に古くから記載されてきた暦注の一つ。
北斗七星の方向と十二支の組み合わせから導かれる12種の日の吉凶。
建築・冠婚葬祭・旅行などの日取りの参考とされる。
"""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult

# ── 十二直データ ──
JUNICHOKU = [
    {
        "name": "建",
        "reading": "たつ",
        "meaning": "万事において吉。新しいことを始めるのに良い日。物事の基礎を築くのに最適。",
        "good_for": "開業・婚礼・移転・建築着工・新規事業",
        "bad_for": "土いじり・蔵開き",
        "nature": "大吉",
    },
    {
        "name": "除",
        "reading": "のぞく",
        "meaning": "不浄を払い清める日。障害を取り除き、新たな道を開く力がある。",
        "good_for": "掃除・治療・祭祀・種まき・井戸掘り",
        "bad_for": "婚礼・旅行・金貸し",
        "nature": "小吉",
    },
    {
        "name": "満",
        "reading": "みつ",
        "meaning": "万物が満ち溢れる日。物事が充実し、実りを得やすい。",
        "good_for": "婚礼・祝い事・引越し・新築・種まき",
        "bad_for": "訴訟・服薬・鍼灸",
        "nature": "大吉",
    },
    {
        "name": "平",
        "reading": "たいら",
        "meaning": "平穏で物事が平等に進む日。偏りのない安定した一日。",
        "good_for": "婚礼・道路修理・壁塗り・柱立て・旅行",
        "bad_for": "池や溝を掘ること・種まき",
        "nature": "小吉",
    },
    {
        "name": "定",
        "reading": "さだん",
        "meaning": "善悪が定まる日。物事を決定し、確定させるのに良い。",
        "good_for": "婚礼・開業・建築・移転・契約・種まき",
        "bad_for": "訴訟・旅行・樹木の植替え",
        "nature": "小吉",
    },
    {
        "name": "執",
        "reading": "とる",
        "meaning": "物事を執り行うのに良い日。地固めや実務に適する。",
        "good_for": "婚礼・祝い事・建築・種まき・井戸掘り",
        "bad_for": "旅行・金銭の出し入れ・引越し",
        "nature": "小吉",
    },
    {
        "name": "破",
        "reading": "やぶる",
        "meaning": "物事を突き破る日。既存のものを壊して新しくする力がある。",
        "good_for": "訴訟・出陣・漁猟・服薬・治療",
        "bad_for": "婚礼・祝い事・契約・建築",
        "nature": "凶",
    },
    {
        "name": "危",
        "reading": "あやぶ",
        "meaning": "危険を伴いやすい日。物事に注意が必要な一日。",
        "good_for": "祭祀・祈願・床敷き・壁塗り",
        "bad_for": "旅行・登山・船出・高所作業・婚礼",
        "nature": "凶",
    },
    {
        "name": "成",
        "reading": "なる",
        "meaning": "物事が成就する日。目標の達成や完成に恵まれる。",
        "good_for": "婚礼・開業・建築・種まき・移転・新規事業",
        "bad_for": "訴訟・談判",
        "nature": "大吉",
    },
    {
        "name": "納",
        "reading": "おさん",
        "meaning": "物事を納め収める日。収穫や蓄積に適する。",
        "good_for": "収穫・商品購入・建築・移転・結納",
        "bad_for": "婚礼・見合い・旅行・訴訟・葬儀",
        "nature": "小吉",
    },
    {
        "name": "開",
        "reading": "ひらく",
        "meaning": "運気が開ける日。新しいことを始めるのに最適な吉日。",
        "good_for": "開業・婚礼・移転・建築・井戸掘り",
        "bad_for": "葬儀・不浄事",
        "nature": "大吉",
    },
    {
        "name": "閉",
        "reading": "とづ",
        "meaning": "物事を閉じ込める日。静かに過ごし、内省するのに良い。",
        "good_for": "金銀の収納・建墓・池の造成・穴塞ぎ",
        "bad_for": "開業・婚礼・旅行・引越し・新規事業",
        "nature": "凶",
    },
]

# ── 吉凶の総合的な意味 ──
NATURE_DESCRIPTIONS = {
    "大吉": "非常に良い日取りです。積極的に行動するのに適しています。",
    "小吉": "概ね良い日取りです。適する事柄に絞って行動すると良いでしょう。",
    "凶": "注意が必要な日取りです。慎重に行動し、無理は避けましょう。",
}


def _get_junichoku_index(year: int, month: int, day: int) -> int:
    """十二直のインデックスを算出する。

    十二直は節月と日の十二支の組み合わせで決まる。
    簡易版として、基準日からの12日周期で算出する。
    基準日: 2000年1月6日（小寒）= 建
    """
    base = date(2000, 1, 6)
    target = date(year, month, day)
    diff = (target - base).days
    return diff % 12


def calculate(birth_data: BirthData) -> DivinationResult:
    """十二直を算出する。"""
    bd = birth_data.birth_date

    idx = _get_junichoku_index(bd.year, bd.month, bd.day)
    choku = JUNICHOKU[idx]

    name = choku["name"]
    reading = choku["reading"]
    meaning = choku["meaning"]
    good_for = choku["good_for"]
    bad_for = choku["bad_for"]
    nature = choku["nature"]
    nature_desc = NATURE_DESCRIPTIONS.get(nature, "")

    # 生まれた日の十二直が示す生来の資質
    birth_traits = {
        "建": "新しいことを始める力と、物事の基礎を築く才能がある。リーダーシップに恵まれた生まれ。",
        "除": "不要なものを見極め、本質を見抜く力がある。浄化と改革の才能に恵まれた生まれ。",
        "満": "豊かさと充実を引き寄せる力がある。人生に実りが多く、恵まれた才能に満ちた生まれ。",
        "平": "バランス感覚に優れ、公平で安定した判断ができる。調和を生み出す才能に恵まれた生まれ。",
        "定": "物事を決断し、確定させる力がある。信念が強く、ぶれない軸を持った生まれ。",
        "執": "物事を着実に実行する力がある。地道な努力で確実に成果を上げる才能に恵まれた生まれ。",
        "破": "既存の枠を破り、新しい道を切り拓く力がある。革新的な才能に恵まれた生まれ。",
        "危": "鋭い直感と危機察知能力がある。慎重さと大胆さを兼ね備えた才能に恵まれた生まれ。",
        "成": "物事を成就させる力に恵まれている。目標達成の才能があり、努力が実を結びやすい生まれ。",
        "納": "物事をまとめ、収束させる力がある。蓄積と収穫の才能に恵まれた生まれ。",
        "開": "運気を切り開く力がある。新しい扉を開き、チャンスを掴む才能に恵まれた生まれ。",
        "閉": "内省と深い思考の力がある。物事を静かに熟考し、本質を見極める才能に恵まれた生まれ。",
    }

    trait = birth_traits.get(name, "")

    interpretation_lines = [
        f"【十二直: {name}（{reading}）】",
        f"  吉凶: {nature} ─ {nature_desc}",
        "",
        f"【意味】",
        f"  {meaning}",
        "",
        f"【生まれた日の資質】",
        f"  {trait}",
        "",
        f"【{name}の日に適すること】",
        f"  {good_for}",
        "",
        f"【{name}の日に避けたいこと】",
        f"  {bad_for}",
        "",
        "【十二直について】",
        "十二直は、北斗七星の柄の方向と十二支の組み合わせから生まれた",
        "日本古来の暦注です。日々の吉凶を知り、行動の指針とするものですが、",
        "生まれた日の十二直は、その人が生来持つ資質や傾向を示すとされます。",
    ]

    return DivinationResult(
        system_name="十二直",
        system_id="junichoku",
        summary=f"{name}（{reading}）─ {nature}",
        details={
            "index": idx,
            "name": name,
            "reading": reading,
            "meaning": meaning,
            "nature": nature,
            "good_for": good_for,
            "bad_for": bad_for,
            "birth_trait": trait,
        },
        interpretation="\n".join(interpretation_lines),
    )
