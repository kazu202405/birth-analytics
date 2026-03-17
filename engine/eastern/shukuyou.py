"""宿曜占星術（しゅくようせんせいじゅつ）― 27宿・簡易版

インド占星術の27ナクシャトラを起源とし、密教とともに日本に伝来した占術。
月の位置（宿）から性格・運勢・相性を読み解く。
精密な月経度計算には天文ライブラリが必要なため、本実装ではJDN周期による簡易版。
"""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult

# ── 27宿データ ──
SHUKUYOU_27 = [
    {
        "name": "角宿", "reading": "かくしゅく", "element": "木", "day": "日",
        "trait": "独立心旺盛で先見の明がある。社交的だが内面は孤高。開拓精神に満ち、新しい分野を切り拓く力を持つ。",
        "category": "和善宿",
    },
    {
        "name": "亢宿", "reading": "こうしゅく", "element": "金", "day": "月",
        "trait": "聡明で信念が強く、公正さを重んじる。白黒はっきりした性格で、妥協を嫌う。独自の哲学を持つ知性派。",
        "category": "悪害宿",
    },
    {
        "name": "氐宿", "reading": "ていしゅく", "element": "土", "day": "火",
        "trait": "穏やかで和を重んじるが、芯は非常に強い。忍耐力があり、地道な努力で大成する。家庭を大切にする。",
        "category": "安重宿",
    },
    {
        "name": "房宿", "reading": "ぼうしゅく", "element": "日", "day": "水",
        "trait": "華やかで人を惹きつける魅力がある。行動力と決断力に優れ、リーダーシップを発揮する。情熱家。",
        "category": "和善宿",
    },
    {
        "name": "心宿", "reading": "しんしゅく", "element": "月", "day": "木",
        "trait": "繊細で直感力に優れ、人の心の機微を読む力がある。多芸多才だが、内面に孤独を抱えやすい。",
        "category": "悪害宿",
    },
    {
        "name": "尾宿", "reading": "びしゅく", "element": "火", "day": "金",
        "trait": "正義感が強く、困難に立ち向かう勇気がある。努力家で忍耐力があり、晩年に大きく開花する。",
        "category": "急速宿",
    },
    {
        "name": "箕宿", "reading": "きしゅく", "element": "水", "day": "土",
        "trait": "自由奔放で束縛を嫌う。知的好奇心が旺盛で、海外や異文化に縁がある。独自の世界観を持つ。",
        "category": "猛悪宿",
    },
    {
        "name": "斗宿", "reading": "としゅく", "element": "木", "day": "日",
        "trait": "信念が強く、志を高く持つ。忍耐力と集中力に優れ、困難を乗り越えて目標を達成する力がある。",
        "category": "安重宿",
    },
    {
        "name": "女宿", "reading": "じょしゅく", "element": "金", "day": "月",
        "trait": "知性と美意識に優れ、努力を惜しまない。勤勉で責任感が強く、実務能力が高い。完璧主義の傾向。",
        "category": "急速宿",
    },
    {
        "name": "虚宿", "reading": "きょしゅく", "element": "土", "day": "火",
        "trait": "想像力が豊かで芸術的センスがある。理想主義で精神世界に関心が深い。繊細で傷つきやすい面も。",
        "category": "和善宿",
    },
    {
        "name": "危宿", "reading": "きしゅく", "element": "日", "day": "水",
        "trait": "行動力があり、冒険心に満ちている。波乱万丈な人生を好み、ドラマチックな展開を引き寄せる。",
        "category": "悪害宿",
    },
    {
        "name": "室宿", "reading": "しつしゅく", "element": "月", "day": "木",
        "trait": "パワフルで統率力がある。壁を突き破る力を持ち、大きなプロジェクトを動かす力がある。情熱的。",
        "category": "猛悪宿",
    },
    {
        "name": "壁宿", "reading": "へきしゅく", "element": "火", "day": "金",
        "trait": "温厚で人望がある。文学・芸術の才能に恵まれ、周囲を癒す力がある。安定志向で家庭的。",
        "category": "安重宿",
    },
    {
        "name": "奎宿", "reading": "けいしゅく", "element": "水", "day": "土",
        "trait": "知性と品格に溢れ、文武両道の才能がある。理想が高く、完璧を追求する。芸術や学問に秀でる。",
        "category": "和善宿",
    },
    {
        "name": "婁宿", "reading": "ろうしゅく", "element": "木", "day": "日",
        "trait": "明るく社交的で、人から好かれる。企画力と実行力を兼ね備え、新しいことを始める力がある。",
        "category": "和善宿",
    },
    {
        "name": "胃宿", "reading": "いしゅく", "element": "金", "day": "月",
        "trait": "行動力と開拓精神に満ちている。負けず嫌いで競争心が強い。リーダーとしての資質がある。",
        "category": "悪害宿",
    },
    {
        "name": "昴宿", "reading": "ぼうしゅく", "element": "土", "day": "火",
        "trait": "上品で洗練されたセンスを持つ。人に好かれる華やかさがあり、財運に恵まれる。おおらか。",
        "category": "安重宿",
    },
    {
        "name": "畢宿", "reading": "ひつしゅく", "element": "日", "day": "水",
        "trait": "忍耐力と粘り強さがある。慎重に計画を立て、着実に目標を達成する。実直で信頼される。",
        "category": "和善宿",
    },
    {
        "name": "觜宿", "reading": "ししゅく", "element": "月", "day": "木",
        "trait": "知性が鋭く、言葉の力に優れる。研究心旺盛で専門分野を極める力がある。やや神経質な面も。",
        "category": "和善宿",
    },
    {
        "name": "参宿", "reading": "さんしゅく", "element": "火", "day": "金",
        "trait": "華やかで存在感がある。好奇心旺盛で多趣味。波乱に富む人生を送りやすいが、逆境に強い。",
        "category": "猛悪宿",
    },
    {
        "name": "井宿", "reading": "せいしゅく", "element": "水", "day": "土",
        "trait": "知的で計算力に優れる。戦略的な思考ができ、状況を冷静に分析する力がある。やや頑固な面も。",
        "category": "急速宿",
    },
    {
        "name": "鬼宿", "reading": "きしゅく", "element": "木", "day": "日",
        "trait": "霊感が強く、目に見えない世界との繋がりがある。想像力が豊かで芸術的才能に恵まれる。27宿の中で最も吉。",
        "category": "安重宿",
    },
    {
        "name": "柳宿", "reading": "りゅうしゅく", "element": "金", "day": "月",
        "trait": "情熱的で感情豊か。執着心が強く、一度決めたことは諦めない。独特の美意識を持つ。",
        "category": "猛悪宿",
    },
    {
        "name": "星宿", "reading": "せいしゅく", "element": "土", "day": "火",
        "trait": "華やかでカリスマ性がある。自信に満ち、リーダーシップを発揮する。芸能・芸術の才能がある。",
        "category": "悪害宿",
    },
    {
        "name": "張宿", "reading": "ちょうしゅく", "element": "日", "day": "水",
        "trait": "堂々とした存在感と人を惹きつける魅力がある。祝い事や祭り事に縁がある。社交的で華やか。",
        "category": "安重宿",
    },
    {
        "name": "翼宿", "reading": "よくしゅく", "element": "月", "day": "木",
        "trait": "真面目で計画的、コツコツと地道に努力する。几帳面で責任感が強い。旅行や移動に縁がある。",
        "category": "急速宿",
    },
    {
        "name": "軫宿", "reading": "しんしゅく", "element": "火", "day": "金",
        "trait": "思慮深く慎重。人の気持ちを察する力に優れ、思いやりがある。完璧主義で自分に厳しい面も。",
        "category": "安重宿",
    },
]

# ── 相性カテゴリ（宿同士の距離に基づく） ──
AISHO_CATEGORIES = {
    "命": "運命的な縁。前世からの深い因縁があり、強く惹かれ合う。最も影響力の大きい関係。",
    "業": "前世の業（カルマ）による縁。学びと成長をもたらす重要な関係。試練も伴う。",
    "胎": "未来への縁。今生で新たに結ぶ関係性で、可能性と発展性がある。",
    "栄": "栄える関係。お互いに良い影響を与え合い、発展する吉の相性。",
    "親": "親しみやすい関係。自然と打ち解け、安心感のある相性。",
    "友": "友好的な関係。協力し合い、楽しい時間を共有できる相性。",
    "衰": "衰退の関係。一緒にいると気力が低下しやすい。注意が必要な相性。",
    "安": "安心の関係。穏やかで安定した関係性。居心地が良い。",
    "壊": "壊す関係。片方が相手のペースを乱す。最も注意が必要な相性。",
    "危": "危険の関係。予想外の展開をもたらす。刺激的だが不安定。",
    "成": "成就の関係。目標達成に向けて協力し合える建設的な相性。",
}


def _get_shukuyou_index(year: int, month: int, day: int) -> int:
    """JDN周期による宿の算出（簡易版）。

    27日周期の繰り返しとして近似計算する。
    基準日: 2000年1月7日 = 角宿（index 0）
    """
    base = date(2000, 1, 7)
    target = date(year, month, day)
    diff = (target - base).days
    return diff % 27


def calculate(birth_data: BirthData) -> DivinationResult:
    """宿曜占星術の宿を算出する。"""
    bd = birth_data.birth_date
    warnings = []

    idx = _get_shukuyou_index(bd.year, bd.month, bd.day)
    shuku = SHUKUYOU_27[idx]

    shuku_name = shuku["name"]
    reading = shuku["reading"]
    element = shuku["element"]
    day_assoc = shuku["day"]
    trait = shuku["trait"]
    category = shuku["category"]

    # 相性の参照（自分の宿番号から各距離の宿を算出）
    aisho_map = {}
    aisho_distances = {
        "命": 0, "業": 1, "胎": 2,
        "栄": 4, "親": 5, "友": 6,
        "衰": 9, "安": 10, "壊": 13,
        "危": 14, "成": 17,
    }
    for rel, dist in aisho_distances.items():
        partner_idx = (idx + dist) % 27
        partner = SHUKUYOU_27[partner_idx]
        aisho_map[rel] = {
            "partner_shuku": partner["name"],
            "description": AISHO_CATEGORIES[rel],
        }

    # カテゴリの説明
    category_descriptions = {
        "和善宿": "穏やかで協調性があり、人に好かれる宿。平和的で安定した運勢。",
        "悪害宿": "強い意志と行動力がある宿。困難を切り拓く力があるが、摩擦も起きやすい。",
        "急速宿": "スピーディーに物事を進める宿。行動力と決断力に優れるが、拙速に注意。",
        "猛悪宿": "強大なパワーを持つ宿。大きなことを成し遂げる力があるが、使い方次第で吉凶が分かれる。",
        "安重宿": "安定感と重厚さがある宿。着実に物事を積み上げ、大きな成果を得る。",
    }

    interpretation_lines = [
        f"【{shuku_name}（{reading}）】",
        f"  七曜: {day_assoc}曜 / 五行: {element}",
        f"  宿分類: {category}",
        f"  {category_descriptions.get(category, '')}",
        "",
        f"【性格・資質】",
        f"  {trait}",
        "",
        f"【相性の指針】",
    ]

    for rel in ["命", "業", "胎", "栄", "親", "友", "衰", "安", "壊", "危", "成"]:
        info = aisho_map[rel]
        interpretation_lines.append(
            f"  {rel}の関係: {info['partner_shuku']} ─ {info['description']}"
        )

    interpretation_lines.extend([
        "",
        "※本実装はJDN周期による簡易計算です。精密な宿の判定には、"
        "出生時の月の黄経に基づく天文学的計算が必要です。",
    ])

    warnings.append(
        "簡易計算のため、実際の宿と1-2宿程度のずれが生じる可能性があります。"
    )

    return DivinationResult(
        system_name="宿曜占星術",
        system_id="shukuyou",
        summary=f"{shuku_name}（{reading}）─ {category}",
        details={
            "shuku_index": idx,
            "shuku_name": shuku_name,
            "reading": reading,
            "element": element,
            "day": day_assoc,
            "category": category,
            "trait": trait,
            "aisho": aisho_map,
        },
        interpretation="\n".join(interpretation_lines),
        warnings=warnings,
    )
