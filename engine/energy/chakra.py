"""チャクラ対応（Chakra Mapping）— 誕生数秘術に基づくチャクラ診断"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


# 7つのチャクラ詳細データ
CHAKRAS = {
    1: {
        "name": "ルートチャクラ（ムーラダーラ）",
        "sanskrit": "Muladhara",
        "color": "赤",
        "element": "地",
        "location": "脊柱の基底部",
        "theme": "安全・安定・生存本能・グラウンディング",
        "description": "生命の根源となるチャクラ。安全と安定を司り、"
                       "物質世界での生存に関わる基本的なエネルギーを管理する。"
                       "グラウンディング（地に足をつける力）の中心。",
        "balanced": "安定感・安心感・現実的な判断力・健全な体力・生きる力が強い",
        "imbalanced": "不安・恐怖・物質への執着・腰痛・免疫力の低下",
        "healing": "自然の中を歩く・赤い食べ物を食べる・ガーデニング・足裏マッサージ",
        "mantra": "LAM（ラム）",
        "crystal": "ルビー・ガーネット・赤メノウ・ブラックトルマリン",
        "aroma": "シダーウッド・パチュリ・ベチバー",
    },
    2: {
        "name": "サクラルチャクラ（スヴァディシュターナ）",
        "sanskrit": "Svadhisthana",
        "color": "橙",
        "element": "水",
        "location": "下腹部（仙骨の辺り）",
        "theme": "創造性・感情・セクシュアリティ・喜び",
        "description": "創造性と感情のチャクラ。喜び・快楽・感情表現を司る。"
                       "水の要素を持ち、流れるような柔軟性と適応力をもたらす。"
                       "人生を楽しむ力の源泉。",
        "balanced": "創造力豊か・感情表現が自然・喜びを感じる力・柔軟な対人関係",
        "imbalanced": "感情の抑圧・創造性の枯渇・依存症・罪悪感・腰回りの不調",
        "healing": "水に触れる（入浴・水泳）・ダンス・創作活動・オレンジ色の食べ物",
        "mantra": "VAM（ヴァム）",
        "crystal": "カーネリアン・オレンジカルサイト・サンストーン",
        "aroma": "イランイラン・サンダルウッド・オレンジ",
    },
    3: {
        "name": "ソーラープレクサスチャクラ（マニプーラ）",
        "sanskrit": "Manipura",
        "color": "黄",
        "element": "火",
        "location": "みぞおち（太陽神経叢）",
        "theme": "意志力・自信・個人の力・変容",
        "description": "意志と自信のチャクラ。個人の力（パーソナルパワー）を司り、"
                       "自己主張・決断力・行動力の源泉。火の要素を持ち、"
                       "変容と消化（物質的・精神的）を管理する。",
        "balanced": "自信・決断力・リーダーシップ・健全な自己主張・消化機能の安定",
        "imbalanced": "自信喪失・支配欲・怒り・胃腸の不調・慢性疲労",
        "healing": "日光浴・腹筋運動・黄色い花を飾る・目標設定と達成",
        "mantra": "RAM（ラム）",
        "crystal": "シトリン・タイガーアイ・イエロージャスパー",
        "aroma": "レモン・ジンジャー・カモミール",
    },
    4: {
        "name": "ハートチャクラ（アナハタ）",
        "sanskrit": "Anahata",
        "color": "緑",
        "element": "風",
        "location": "胸の中央",
        "theme": "愛・慈悲・共感・癒し",
        "description": "愛と調和のチャクラ。無条件の愛・慈悲・共感を司る。"
                       "上位チャクラと下位チャクラの橋渡し役。"
                       "風の要素を持ち、広がりと繋がりをもたらす。",
        "balanced": "深い愛情・共感力・許しの心・感謝の気持ち・人間関係の調和",
        "imbalanced": "嫉妬・孤独感・依存・心臓や肺の不調・境界線の欠如",
        "healing": "ハグ・緑の自然の中で過ごす・感謝日記・胸を開くヨガのポーズ",
        "mantra": "YAM（ヤム）",
        "crystal": "ローズクォーツ・エメラルド・グリーンアベンチュリン",
        "aroma": "ローズ・ゼラニウム・ベルガモット",
    },
    5: {
        "name": "スロートチャクラ（ヴィシュッダ）",
        "sanskrit": "Vishuddha",
        "color": "青",
        "element": "エーテル（空）",
        "location": "喉",
        "theme": "表現・真実・コミュニケーション",
        "description": "表現とコミュニケーションのチャクラ。真実を語る力、"
                       "自己表現、聴く力を司る。エーテルの要素を持ち、"
                       "空間と振動を通じた交流をもたらす。",
        "balanced": "明確な自己表現・傾聴力・創造的なコミュニケーション・歌や言葉の才能",
        "imbalanced": "言いたいことが言えない・喉の不調・嘘・過度なおしゃべり",
        "healing": "歌を歌う・日記を書く・青空を見上げる・首のストレッチ",
        "mantra": "HAM（ハム）",
        "crystal": "ラピスラズリ・ターコイズ・アクアマリン",
        "aroma": "ペパーミント・ユーカリ・ティーツリー",
    },
    6: {
        "name": "サードアイチャクラ（アージュニャー）",
        "sanskrit": "Ajna",
        "color": "藍",
        "element": "光",
        "location": "眉間（第三の目）",
        "theme": "直感・洞察・叡智・第六感",
        "description": "直感と洞察のチャクラ。第三の目とも呼ばれ、"
                       "物事の本質を見抜く力、直感、ビジョンを司る。"
                       "光の要素を持ち、内なる明晰さをもたらす。",
        "balanced": "鋭い直感・明晰なビジョン・洞察力・夢を通じた気づき・知恵",
        "imbalanced": "頭痛・不眠・幻想・現実逃避・集中力の欠如",
        "healing": "瞑想・星を見る・藍色の食べ物（ブルーベリーなど）・額のマッサージ",
        "mantra": "OM（オーム）",
        "crystal": "アメジスト・ラピスラズリ・フローライト",
        "aroma": "ラベンダー・フランキンセンス・クラリセージ",
    },
    7: {
        "name": "クラウンチャクラ（サハスラーラ）",
        "sanskrit": "Sahasrara",
        "color": "紫（白）",
        "element": "思考（宇宙意識）",
        "location": "頭頂",
        "theme": "霊性・宇宙意識・悟り・統合",
        "description": "霊性と統合のチャクラ。宇宙意識との繋がり、"
                       "悟り、全体性を司る。全てのチャクラを統合し、"
                       "高次の意識への扉を開く。",
        "balanced": "スピリチュアルな目覚め・宇宙との一体感・深い平和・叡智の統合",
        "imbalanced": "スピリチュアルな迷い・現実からの乖離・孤立感・目的の喪失",
        "healing": "瞑想・祈り・静寂の時間・白や紫の花を飾る",
        "mantra": "AUM（アウム）/ 沈黙",
        "crystal": "クリアクォーツ・アメジスト・セレナイト",
        "aroma": "フランキンセンス・ロータス・ミルラ",
    },
}

# ライフパス数からチャクラへのマッピング
# 1->1, 2->2, 3->3, 4->4, 5->5, 6->6, 7->7, 8->1, 9->2
# マスターナンバー: 11->4, 22->7, 33->6
LIFE_PATH_TO_CHAKRA = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 1,
    9: 2,
    11: 4,
    22: 7,
    33: 6,
}

# ライフパス数ごとのチャクラ的解釈の補足
LIFE_PATH_CHAKRA_NOTES = {
    1: "リーダーシップと独立心が、ルートチャクラのグラウンディングの力と共鳴します。"
       "物質世界での確固たる基盤を築くことが使命です。",
    2: "協調性と感受性が、サクラルチャクラの創造性と感情の流れに共鳴します。"
       "人間関係における調和と創造的な表現が鍵です。",
    3: "表現力と創造性が、ソーラープレクサスの自信と個人の力に共鳴します。"
       "自分の才能を信じ、堂々と表現することで開花します。",
    4: "堅実さと構築力が、ハートチャクラの愛と安定に共鳴します。"
       "愛を基盤とした確かな土台作りが人生のテーマです。",
    5: "自由と変化が、スロートチャクラのコミュニケーションと表現に共鳴します。"
       "真実の自分を自由に表現することで道が開けます。",
    6: "奉仕と責任が、サードアイチャクラの洞察力に共鳴します。"
       "深い直感と知恵で家族やコミュニティを導く役割です。",
    7: "探究と内省が、クラウンチャクラの霊性に共鳴します。"
       "深い精神性と叡智を追求する魂の旅です。",
    8: "成功と物質が、ルートチャクラの現実的な力に共鳴します。"
       "物質的な豊かさを通じてスピリチュアルな学びを得る道です。",
    9: "慈悲と完成が、サクラルチャクラの感情と創造性に共鳴します。"
       "全ての経験を統合し、人類への奉仕に昇華する使命です。",
    11: "マスターナンバー11: 霊的な直感がハートチャクラの愛と融合します。"
        "高い直感力で人々の心を照らすライトワーカーです。",
    22: "マスターナンバー22: 壮大なビジョンがクラウンチャクラの宇宙意識と共鳴します。"
        "霊的なビジョンを現実世界に顕現させるマスタービルダーです。",
    33: "マスターナンバー33: 無条件の愛がサードアイチャクラの叡智と融合します。"
        "慈悲と叡智で人類を癒すマスターヒーラーです。",
}

# 全チャクラのバランスアドバイス
BALANCE_ADVICE = {
    1: "大地と繋がるグラウンディングの実践を日課にしましょう。"
       "裸足で地面を歩く、根菜類を食べる、安定した日常リズムを作ることが効果的です。",
    2: "水の要素を生活に取り入れましょう。"
       "入浴の時間を大切にし、創作活動や身体的な表現を楽しむことでバランスが整います。",
    3: "太陽の光を浴び、自分に自信を持つ練習をしましょう。"
       "小さな成功体験を積み重ね、自分の力を信頼することが大切です。",
    4: "胸を開くヨガのポーズや深い呼吸を実践しましょう。"
       "感謝の気持ちを言葉にし、自然の緑の中で過ごす時間を増やしてください。",
    5: "歌を歌ったり、日記を書いたり、自分の気持ちを言葉にする習慣をつけましょう。"
       "真実を穏やかに伝える練習が、このチャクラを活性化します。",
    6: "静かな瞑想の時間を設けましょう。"
       "直感を信頼する練習をし、夢日記をつけることで洞察力が高まります。",
    7: "一日の中に静寂の時間を作りましょう。"
       "瞑想・祈り・自然の中での沈黙が、宇宙意識との繋がりを深めます。",
}


def _life_path_number(year: int, month: int, day: int) -> int:
    """ライフパス数を算出する。マスターナンバー（11, 22, 33）は保持する。"""
    # 年・月・日をそれぞれ一桁に畳み込み（マスターナンバーは保持）
    def reduce(n: int) -> int:
        while n > 9 and n not in (11, 22, 33):
            n = sum(int(d) for d in str(n))
        return n

    y = reduce(year)
    m = reduce(month)
    d = reduce(day)

    total = y + m + d
    return reduce(total)


def calculate(birth_data: BirthData) -> DivinationResult:
    """チャクラ対応の鑑定を行う。"""
    bd = birth_data.birth_date
    life_path = _life_path_number(bd.year, bd.month, bd.day)

    chakra_num = LIFE_PATH_TO_CHAKRA.get(life_path, 1)
    primary_chakra = CHAKRAS[chakra_num]
    chakra_note = LIFE_PATH_CHAKRA_NOTES.get(life_path, "")
    balance = BALANCE_ADVICE[chakra_num]

    is_master = life_path in (11, 22, 33)
    life_path_label = f"マスターナンバー {life_path}" if is_master else str(life_path)

    # サブチャクラ（隣接するチャクラ）
    sub_chakras = []
    if chakra_num > 1:
        sub_chakras.append(CHAKRAS[chakra_num - 1]["name"])
    if chakra_num < 7:
        sub_chakras.append(CHAKRAS[chakra_num + 1]["name"])

    # 全チャクラ一覧（概要）
    all_chakras_summary = []
    for i in range(1, 8):
        c = CHAKRAS[i]
        marker = " [主要]" if i == chakra_num else ""
        all_chakras_summary.append({
            "number": i,
            "name": c["name"],
            "color": c["color"],
            "theme": c["theme"],
            "is_primary": i == chakra_num,
        })

    return DivinationResult(
        system_name="チャクラ対応",
        system_id="chakra",
        summary=f"ライフパス数 {life_path_label} / 対応チャクラ: 第{chakra_num} {primary_chakra['name']}",
        details={
            "life_path_number": life_path,
            "is_master_number": is_master,
            "primary_chakra": {
                "number": chakra_num,
                "name": primary_chakra["name"],
                "sanskrit": primary_chakra["sanskrit"],
                "color": primary_chakra["color"],
                "element": primary_chakra["element"],
                "location": primary_chakra["location"],
                "theme": primary_chakra["theme"],
                "mantra": primary_chakra["mantra"],
                "crystal": primary_chakra["crystal"],
                "aroma": primary_chakra["aroma"],
            },
            "sub_chakras": sub_chakras,
            "all_chakras": all_chakras_summary,
        },
        interpretation=(
            f"【ライフパス数】{life_path_label}\n\n"
            f"【対応チャクラ】第{chakra_num}チャクラ — {primary_chakra['name']}\n"
            f"色: {primary_chakra['color']} / 元素: {primary_chakra['element']} / "
            f"位置: {primary_chakra['location']}\n\n"
            f"【テーマ】{primary_chakra['theme']}\n\n"
            f"【チャクラの意味】{primary_chakra['description']}\n\n"
            f"【バランスが取れている時】{primary_chakra['balanced']}\n"
            f"【バランスが崩れている時】{primary_chakra['imbalanced']}\n\n"
            f"【あなたとこのチャクラ】{chakra_note}\n\n"
            f"【ヒーリング方法】{primary_chakra['healing']}\n"
            f"【マントラ】{primary_chakra['mantra']}\n"
            f"【クリスタル】{primary_chakra['crystal']}\n"
            f"【アロマ】{primary_chakra['aroma']}\n\n"
            f"【バランスのアドバイス】{balance}"
        ),
    )
