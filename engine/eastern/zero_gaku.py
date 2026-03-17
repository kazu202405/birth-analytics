"""0学占い（ゼロがくうらない）— 御射山宇彦が提唱した運命学"""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


# 12支配星とその特性
ZERO_STARS = [
    {
        "name": "水王星",
        "group": "水のグループ",
        "trait": "知性・冷静・分析力。水のように深い思考と柔軟性を持つ。",
        "personality": "冷静沈着で分析力に優れる知性派。物事の本質を見抜く洞察力があり、"
                       "論理的な思考で問題を解決する。感情に流されず的確な判断ができるが、"
                       "冷たく見られることもある。",
        "love": "知的な会話を楽しめる相手に惹かれる。信頼関係を重視し、深い絆を築く。",
        "work": "研究者・アナリスト・プログラマーなど知的職業に適性。",
        "compatible": ["氷王星", "魚王星"],
    },
    {
        "name": "氷王星",
        "group": "水のグループ",
        "trait": "純粋・透明・完璧主義。美意識が高く理想を追求する。",
        "personality": "純粋で理想主義的。完璧を追い求める美意識の高さが特徴。"
                       "透明感のある存在で、嘘やごまかしを嫌う。理想が高すぎて"
                       "現実とのギャップに苦しむことがある。",
        "love": "理想の相手を求め続ける。純粋な愛情を捧げ、一途に相手を想う。",
        "work": "芸術家・デザイナー・品質管理など美と精度を求める職業に適性。",
        "compatible": ["水王星", "月王星"],
    },
    {
        "name": "魚王星",
        "group": "水のグループ",
        "trait": "感受性・直感・適応力。感情豊かで共感力に優れる。",
        "personality": "感受性が非常に豊かで、直感的に物事を理解する力を持つ。"
                       "周囲の感情を敏感に感じ取り、共感力に優れる。適応力が高いが、"
                       "感情に振り回されやすい面もある。",
        "love": "感情の交流を大切にする。相手の気持ちに寄り添い、深い愛情を注ぐ。",
        "work": "カウンセラー・看護師・作家など人の心に関わる職業に適性。",
        "compatible": ["水王星", "海王星"],
    },
    {
        "name": "月王星",
        "group": "火のグループ",
        "trait": "神秘・変化・ロマンチスト。内面世界が豊かで創造的。",
        "personality": "神秘的な魅力を放つロマンチスト。豊かな内面世界を持ち、"
                       "創造性に溢れている。月のように満ち欠けする感情の波があり、"
                       "気分の変動が大きいが、その変化が創造力の源泉となる。",
        "love": "ロマンチックな恋愛を好む。理想と現実の間で揺れることも。",
        "work": "アーティスト・音楽家・映像クリエイターなど創造的職業に適性。",
        "compatible": ["氷王星", "花王星"],
    },
    {
        "name": "火王星",
        "group": "火のグループ",
        "trait": "情熱・行動力・リーダーシップ。エネルギッシュで決断が速い。",
        "personality": "燃えるような情熱と行動力の持ち主。リーダーシップを発揮し、"
                       "周囲を引っ張っていく力がある。決断が速く実行力に優れるが、"
                       "衝動的になりやすく、後先考えずに突き進む面も。",
        "love": "情熱的な恋愛を求める。相手を強く引っ張るタイプ。",
        "work": "経営者・営業・スポーツ選手など行動力が活きる職業に適性。",
        "compatible": ["雷王星", "光王星"],
    },
    {
        "name": "海王星",
        "group": "火のグループ",
        "trait": "包容力・寛大・大局観。スケールの大きな発想と実行力。",
        "personality": "海のような広い心と大局観を持つ。スケールの大きな発想で"
                       "物事を捉え、包容力で周囲を包み込む。寛大で器が大きいが、"
                       "大雑把になりやすく、細部への注意が課題。",
        "love": "包容力のある愛情で相手を受け止める。懐の深さが魅力。",
        "work": "政治家・外交官・プロデューサーなど大局的視点の職業に適性。",
        "compatible": ["魚王星", "地王星"],
    },
    {
        "name": "山王星",
        "group": "地のグループ",
        "trait": "安定・忍耐・堅実。揺るぎない信念と持続力。",
        "personality": "山のように揺るぎない安定感と忍耐力の持ち主。堅実に物事を"
                       "進め、一度決めたことは最後までやり遂げる。信頼性が高いが、"
                       "融通が利かず、変化を嫌う傾向がある。",
        "love": "安定した関係を求める。誠実で一途な愛情を持つ。",
        "work": "公務員・銀行員・建築家など堅実さが求められる職業に適性。",
        "compatible": ["地王星", "風王星"],
    },
    {
        "name": "雷王星",
        "group": "地のグループ",
        "trait": "革新・突破力・独創性。既存の枠を壊す革命家。",
        "personality": "雷のような衝撃と突破力を持つ革新者。既存の枠を壊し、"
                       "新しい道を切り開く。独創的な発想と実行力で変革をもたらすが、"
                       "周囲との摩擦を生みやすい面がある。",
        "love": "刺激的な関係を求める。型にはまらない自由な恋愛観。",
        "work": "起業家・発明家・改革者など変革を起こす職業に適性。",
        "compatible": ["火王星", "風王星"],
    },
    {
        "name": "風王星",
        "group": "地のグループ",
        "trait": "自由・コミュニケーション・多才。社交的で情報収集に長ける。",
        "personality": "風のように自由で軽やかな存在。コミュニケーション能力が高く、"
                       "多才で幅広い分野に関心を持つ。情報収集力と発信力に優れるが、"
                       "一つのことに集中するのが苦手な面がある。",
        "love": "軽やかで楽しい恋愛を好む。束縛を嫌い自由を重視。",
        "work": "ジャーナリスト・広報・通訳など情報とコミュニケーションの職業に適性。",
        "compatible": ["山王星", "雷王星"],
    },
    {
        "name": "地王星",
        "group": "天のグループ",
        "trait": "現実・実務・責任感。地に足のついた堅実な実行者。",
        "personality": "大地のような安定感と現実的な実務能力を持つ。責任感が強く、"
                       "地に足のついた堅実な行動で成果を上げる。信頼性が高いが、"
                       "保守的になりすぎる傾向がある。",
        "love": "現実的で安定した関係を重視。誠実なパートナーシップを築く。",
        "work": "管理職・会計士・不動産など実務能力が活きる職業に適性。",
        "compatible": ["海王星", "山王星"],
    },
    {
        "name": "花王星",
        "group": "天のグループ",
        "trait": "美・調和・芸術性。華やかで人を惹きつける魅力。",
        "personality": "花のような華やかさと美しさを持つ存在。芸術的感性に優れ、"
                       "調和を大切にする。人を惹きつける魅力があり、周囲を明るくするが、"
                       "繊細で傷つきやすい面を隠していることも。",
        "love": "美しい恋愛を求める。ロマンチストで愛情深い。",
        "work": "芸能人・ファッション・フローリストなど美に関わる職業に適性。",
        "compatible": ["月王星", "光王星"],
    },
    {
        "name": "光王星",
        "group": "天のグループ",
        "trait": "輝き・リーダーシップ・カリスマ。太陽のように周囲を照らす。",
        "personality": "太陽のような輝きとカリスマ性を持つリーダー。周囲を照らし、"
                       "人々を導く力がある。自信に満ち、堂々とした存在感で注目を集めるが、"
                       "自己中心的になりやすい面に注意が必要。",
        "love": "華やかで情熱的な恋愛。相手を輝かせる力がある。",
        "work": "経営者・政治家・エンターテイナーなどリーダーシップが活きる職業に適性。",
        "compatible": ["火王星", "花王星"],
    },
]

# 12年運命周期（0学独自）
ZERO_CYCLE = [
    {"name": "開拓", "desc": "新しいステージの始まり。積極的に動くことで運が開ける。"},
    {"name": "生長", "desc": "着実に成長する時期。基盤を固め、力を蓄える。"},
    {"name": "決定", "desc": "重要な決断の時期。方向性を定め、迷わず進む。"},
    {"name": "健康", "desc": "心身のバランスを整える時期。無理は禁物。"},
    {"name": "人気", "desc": "人間関係が活発になる時期。人脈が広がり、評価が高まる。"},
    {"name": "浮気", "desc": "注意の時期。誘惑が多く、本質を見失いやすい。慎重に。"},
    {"name": "再開", "desc": "過去の縁が再び巡る時期。見直しと再出発に最適。"},
    {"name": "経済", "desc": "経済的に恵まれる時期。投資や財テクに適する。"},
    {"name": "充実", "desc": "実り多き時期。あらゆる面で充実し、満足感を得られる。"},
    {"name": "背信", "desc": "裏切りに注意の時期。信頼関係を慎重に見極める。"},
    {"name": "零落", "desc": "最も注意が必要な時期。耐え忍び、次の飛躍に備える。"},
    {"name": "精算", "desc": "清算と整理の時期。不要なものを手放し、身軽になる。"},
]


def _zero_fate(year: int, month: int, day: int) -> int:
    """0学の運命数を算出する。

    生年月日の全桁を合計し、1-12の範囲に収まるまで繰り返し畳み込む。
    """
    digits = f"{year:04d}{month:02d}{day:02d}"
    total = sum(int(d) for d in digits)
    while total > 12:
        total = sum(int(d) for d in str(total))
    return total if total > 0 else 12


def _get_cycle_position(year: int, fate: int) -> int:
    """指定年の12年運命周期における位置を返す (0-11)。"""
    return (year + fate) % 12


def calculate(birth_data: BirthData) -> DivinationResult:
    """0学占いの鑑定を行う。"""
    bd = birth_data.birth_date
    fate = _zero_fate(bd.year, bd.month, bd.day)
    star_idx = fate - 1  # 1-12 -> 0-11
    star = ZERO_STARS[star_idx]

    # 今年の運命周期
    current_year = date.today().year
    cycle_pos = _get_cycle_position(current_year, fate)
    current_cycle = ZERO_CYCLE[cycle_pos]

    # 注意時期の判定（背信・零落・精算）
    is_caution = current_cycle["name"] in ("背信", "零落", "精算")
    warnings = []
    if is_caution:
        warnings.append(
            f"現在「{current_cycle['name']}」の時期です。"
            "慎重な行動を心がけ、大きな決断は控えめに。"
        )

    # 3年分の周期予測
    forecast = {}
    for offset in range(1, 4):
        future_year = current_year + offset
        future_pos = _get_cycle_position(future_year, fate)
        fc = ZERO_CYCLE[future_pos]
        forecast[str(future_year)] = {
            "cycle": fc["name"],
            "description": fc["desc"],
        }

    # 相性の良い星
    compatible_names = ", ".join(star["compatible"])

    return DivinationResult(
        system_name="0学占い",
        system_id="zero_gaku",
        summary=f"支配星: {star['name']}（{star['group']}）/ {current_year}年: {current_cycle['name']}",
        details={
            "fate_number": fate,
            "ruling_star": star["name"],
            "group": star["group"],
            "keyword": star["trait"].split("。")[0],
            "love": star["love"],
            "work": star["work"],
            "compatible_stars": star["compatible"],
            "current_year": current_year,
            "cycle_position": current_cycle["name"],
            "cycle_description": current_cycle["desc"],
            "is_caution_period": is_caution,
            "forecast_3years": forecast,
        },
        interpretation=(
            f"あなたの支配星は「{star['name']}」（{star['group']}）です。\n\n"
            f"【特性】{star['trait']}\n\n"
            f"【性格】{star['personality']}\n\n"
            f"【恋愛】{star['love']}\n"
            f"【仕事】{star['work']}\n"
            f"【相性の良い星】{compatible_names}\n\n"
            f"【{current_year}年の運勢】{current_cycle['name']}\n"
            f"{current_cycle['desc']}"
        ),
        warnings=warnings,
    )
