"""オーラソーマ誕生日ボトル（Aura-Soma Birth Bottle）— 色彩療法に基づく魂の診断"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


# イクイリブリアムボトル（主要ボトル 0-41: 誕生日ボトルとして頻出する範囲）
# 各ボトルは上層色・下層色・テーマ・メッセージを持つ
BOTTLES = {
    0: {
        "name": "スピリチュアルレスキュー",
        "upper": "ロイヤルブルー",
        "lower": "ディープマゼンタ",
        "theme": "光・純粋・始まり",
        "message": "深い平和と霊的な保護。瞑想と内なる静寂を通じて自己を見つめる。"
                   "全ての始まりであり、無限の可能性を秘めた存在。",
    },
    1: {
        "name": "フィジカルレスキュー",
        "upper": "ブルー",
        "lower": "ディープマゼンタ",
        "theme": "平和・スピリチュアルな使命",
        "message": "平和をもたらす使命を持つ。深い癒しの力と霊的な洞察力。"
                   "言葉を通じて真実を伝える能力がある。",
    },
    2: {
        "name": "ピースボトル",
        "upper": "ブルー",
        "lower": "ブルー",
        "theme": "平和・コミュニケーション",
        "message": "内なる平和とコミュニケーション能力。穏やかで調和的な存在。"
                   "言葉と沈黙のバランスを通じて真実を伝える。",
    },
    3: {
        "name": "ハートボトル / アトランティアンボトル",
        "upper": "ブルー",
        "lower": "グリーン",
        "theme": "心のコミュニケーション・創造性",
        "message": "ハートからのコミュニケーション。創造性と感情表現の調和。"
                   "芸術的才能と心の深い理解力を持つ。",
    },
    4: {
        "name": "サンライトボトル",
        "upper": "イエロー",
        "lower": "ゴールド",
        "theme": "太陽の知恵・喜び",
        "message": "太陽のような明るさと知恵。自信と喜びを周囲に広げる力。"
                   "学びを通じて自己成長する道を歩む。",
    },
    5: {
        "name": "サンセットボトル / サンライズボトル",
        "upper": "イエロー",
        "lower": "レッド",
        "theme": "エネルギー・活力・自己認識",
        "message": "生命力に溢れたエネルギー。自己認識と行動力のバランス。"
                   "情熱と知性を兼ね備え、道を切り開く。",
    },
    6: {
        "name": "エナジーボトル",
        "upper": "レッド",
        "lower": "レッド",
        "theme": "生命力・グラウンディング・情熱",
        "message": "強い生命力とグラウンディングの力。地に足のついた情熱的な存在。"
                   "現実世界での行動力と実現力に優れる。",
    },
    7: {
        "name": "ゲッセマネの園 / 信仰のテスト",
        "upper": "イエロー",
        "lower": "グリーン",
        "theme": "信頼・知恵・ハートの真実",
        "message": "信頼と知恵の融合。ハートの真実に従って生きる勇気。"
                   "自然界との深い繋がりを持つ。",
    },
    8: {
        "name": "アヌビス",
        "upper": "イエロー",
        "lower": "ブルー",
        "theme": "コミュニケーション・知恵・喜び",
        "message": "知恵とコミュニケーションの調和。喜びを通じた自己表現。"
                   "教育や指導の才能がある。",
    },
    9: {
        "name": "ハートの中のハート / クリスタルの洞窟",
        "upper": "ターコイズ",
        "lower": "グリーン",
        "theme": "ハートからの創造性・感受性",
        "message": "深い感受性と創造的表現力。ハートの中のハートに触れる力。"
                   "芸術的直感と自然への共感に優れる。",
    },
    10: {
        "name": "Go Hug a Tree",
        "upper": "グリーン",
        "lower": "グリーン",
        "theme": "自然との調和・ハートの癒し",
        "message": "自然との深い結びつき。ハートの癒しと成長。"
                   "植物や動物との共感力を持ち、環境への意識が高い。",
    },
    11: {
        "name": "エッセネボトルI / 花の鎖",
        "upper": "クリア",
        "lower": "ピンク",
        "theme": "無条件の愛・明晰さ",
        "message": "純粋な愛と明晰さ。無条件の愛を体現する存在。"
                   "透明な視点で物事を見る力がある。",
    },
    12: {
        "name": "メッシーナの新しい時代 / 平和の使者",
        "upper": "クリア",
        "lower": "ブルー",
        "theme": "平和・明晰さ・新しい時代",
        "message": "新しい時代の平和の使者。明晰さと平和を広げる役割。"
                   "クリアな思考と穏やかなコミュニケーション。",
    },
    13: {
        "name": "チェンジ イン ザ ニューイーオン / 新しい始まり",
        "upper": "クリア",
        "lower": "グリーン",
        "theme": "変容・新しい始まり・方向性",
        "message": "変容と新しい方向性。自分自身の真実を見つける旅。"
                   "明晰な意識でハートの声に従う。",
    },
    14: {
        "name": "叡智の新しい始まり",
        "upper": "クリア",
        "lower": "ゴールド",
        "theme": "叡智・明晰さ・自己認識",
        "message": "叡智と自己認識の光。内なる知恵に目覚め、明晰な意識で導く。"
                   "古代の知恵と現代の明晰さの融合。",
    },
    15: {
        "name": "ヒーリング イン ザ ニューイーオン",
        "upper": "クリア",
        "lower": "バイオレット",
        "theme": "癒し・奉仕・スピリチュアリティ",
        "message": "新しい時代のヒーラー。癒しと奉仕の道を歩む。"
                   "スピリチュアルな明晰さを通じて他者を導く。",
    },
    16: {
        "name": "バイオレットローブ",
        "upper": "バイオレット",
        "lower": "バイオレット",
        "theme": "奉仕・変容・スピリチュアリティ",
        "message": "深いスピリチュアリティと奉仕の精神。変容を通じて成長する。"
                   "高い意識レベルと癒しの力を持つ。",
    },
    17: {
        "name": "吟遊詩人 / 希望のボトル",
        "upper": "グリーン",
        "lower": "バイオレット",
        "theme": "希望・信頼・ハートとスピリットの融合",
        "message": "希望と信頼の力。ハートとスピリットの調和。"
                   "芸術的表現を通じて霊的なメッセージを伝える。",
    },
    18: {
        "name": "エジプシャンボトル / ターニングタイド",
        "upper": "イエロー",
        "lower": "バイオレット",
        "theme": "叡智・変容・自己認識",
        "message": "古代の叡智と現代の変容。自己認識を深める旅。"
                   "知恵とスピリチュアリティの統合。",
    },
    19: {
        "name": "物質世界に生きる",
        "upper": "レッド",
        "lower": "パープル",
        "theme": "物質とスピリットの統合・愛のエネルギー",
        "message": "物質世界での霊的な生き方。愛のエネルギーを地上で体現する。"
                   "情熱とスピリチュアリティの調和。",
    },
    20: {
        "name": "スターチャイルド",
        "upper": "ブルー",
        "lower": "ピンク",
        "theme": "愛とコミュニケーション・スターチャイルド",
        "message": "星の子供。愛とコミュニケーションを通じて光を広げる。"
                   "無条件の愛と平和の波動を持つ。",
    },
    21: {
        "name": "新しい始まりの愛 / 直感からの愛",
        "upper": "グリーン",
        "lower": "ピンク",
        "theme": "ハートの新しい始まり・無条件の愛",
        "message": "ハートからの新しい始まり。無条件の愛を体験し表現する。"
                   "直感に従い、愛の道を歩む。",
    },
    22: {
        "name": "リバーサーズボトル / 覚醒",
        "upper": "イエロー",
        "lower": "ピンク",
        "theme": "覚醒・自己受容・喜び",
        "message": "自己受容と喜びの覚醒。自分自身を愛し、認める力。"
                   "知恵と愛の調和による深い理解。",
    },
    23: {
        "name": "愛と光",
        "upper": "ローズピンク",
        "lower": "ピンク",
        "theme": "無条件の愛・優しさ・思いやり",
        "message": "愛と光の存在。深い優しさと思いやりで周囲を包む。"
                   "無条件の愛を体現し、癒しの力を広げる。",
    },
    24: {
        "name": "新しいメッセージ",
        "upper": "バイオレット",
        "lower": "ターコイズ",
        "theme": "創造性・コミュニケーション・変容",
        "message": "新しいメッセージを伝える使命。創造性と変容の力。"
                   "芸術的表現を通じて新時代のビジョンを共有する。",
    },
    25: {
        "name": "フローレンスナイチンゲール / 回復期のボトル",
        "upper": "パープル",
        "lower": "マゼンタ",
        "theme": "癒し・奉仕・献身",
        "message": "献身的な癒しの力。奉仕の精神と深い慈愛。"
                   "困っている人に手を差し伸べる使命感を持つ。",
    },
    26: {
        "name": "エーテルレスキュー / ショックボトル",
        "upper": "オレンジ",
        "lower": "オレンジ",
        "theme": "ショックからの回復・洞察・深い喜び",
        "message": "ショックからの回復と深い洞察力。困難を乗り越える力。"
                   "深い喜びと生命エネルギーの回復。",
    },
    27: {
        "name": "ロビンフッド",
        "upper": "レッド",
        "lower": "グリーン",
        "theme": "情熱とハート・正義感",
        "message": "正義感と行動力。ハートの声に従い、弱者のために立ち上がる。"
                   "情熱をハートの目的のために使う。",
    },
    28: {
        "name": "メイドマリアン",
        "upper": "グリーン",
        "lower": "レッド",
        "theme": "ハートの勇気・自然への回帰",
        "message": "ハートからの勇気。自然との繋がりを大切にし、"
                   "愛と調和の中で真の強さを発揮する。",
    },
    29: {
        "name": "起き上がって進め",
        "upper": "レッド",
        "lower": "ブルー",
        "theme": "エネルギーと平和の統合",
        "message": "行動と平和の調和。エネルギッシュでありながら穏やか。"
                   "力と平和を同時に体現する存在。",
    },
    30: {
        "name": "天を地にもたらす",
        "upper": "ブルー",
        "lower": "レッド",
        "theme": "天と地の統合・使命の実現",
        "message": "天のビジョンを地上で実現する使命。スピリチュアルな意識と"
                   "現実的な行動力の統合。",
    },
    31: {
        "name": "ファウンテン",
        "upper": "グリーン",
        "lower": "ゴールド",
        "theme": "豊かさ・ハートの叡智",
        "message": "ハートからの豊かさの泉。内なる叡智に従い、豊かさを創造する。"
                   "自然の恵みと黄金の知恵の融合。",
    },
    32: {
        "name": "ソフィア",
        "upper": "ロイヤルブルー",
        "lower": "ゴールド",
        "theme": "叡智・直感・内なる知恵",
        "message": "ソフィアの叡智。深い直感と内なる知恵に導かれる。"
                   "霊的な洞察力と自己認識の光。",
    },
    33: {
        "name": "ドルフィンボトル / 平和の目的",
        "upper": "ロイヤルブルー",
        "lower": "ターコイズ",
        "theme": "平和・創造性・深い直感",
        "message": "イルカのような遊び心と深い直感。平和と創造性の調和。"
                   "深い意識の海から叡智を汲み上げる。",
    },
    34: {
        "name": "ヴィーナスの誕生",
        "upper": "ピンク",
        "lower": "ターコイズ",
        "theme": "愛と創造性の誕生",
        "message": "美と愛の誕生。創造的な表現を通じて愛を広げる。"
                   "ヴィーナスのような美しさと慈愛の力。",
    },
    35: {
        "name": "親切の精神 / カインドネス",
        "upper": "ピンク",
        "lower": "バイオレット",
        "theme": "優しさ・奉仕・慈愛",
        "message": "深い親切心と奉仕の精神。優しさを通じて世界を変える力。"
                   "愛とスピリチュアリティの融合。",
    },
    36: {
        "name": "チャリティ / 慈善",
        "upper": "バイオレット",
        "lower": "ピンク",
        "theme": "慈善・無条件の愛・変容",
        "message": "慈善の精神。無条件の愛と変容の力を持ち、"
                   "他者への奉仕を通じて自己も成長する。",
    },
    37: {
        "name": "ガーディアンエンジェルが土に降りる",
        "upper": "バイオレット",
        "lower": "ブルー",
        "theme": "守護・平和・スピリチュアルな導き",
        "message": "守護天使のような存在。平和とスピリチュアルな導きの力。"
                   "目に見えない世界との繋がりが深い。",
    },
    38: {
        "name": "吟遊詩人II / 識別力",
        "upper": "バイオレット",
        "lower": "グリーン",
        "theme": "識別力・ハートとスピリットの統合",
        "message": "深い識別力と洞察力。ハートとスピリットの統合。"
                   "真実を見分け、正しい方向に導く力。",
    },
    39: {
        "name": "エジプシャンボトルII / 操り人形師",
        "upper": "バイオレット",
        "lower": "ゴールド",
        "theme": "叡智・変容・内なる権威",
        "message": "古代の叡智と内なる権威。自分自身の主人となる力。"
                   "スピリチュアルな叡智を日常に活かす。",
    },
    40: {
        "name": "アイアムボトル",
        "upper": "レッド",
        "lower": "ゴールド",
        "theme": "「私は在る」・自己認識・知恵",
        "message": "「私は在る」という深い自己認識。存在の本質に触れる力。"
                   "生命力と叡智の黄金の融合。",
    },
    41: {
        "name": "叡智のボトル / エルドラド",
        "upper": "ゴールド",
        "lower": "ゴールド",
        "theme": "叡智・豊かさ・黄金の知恵",
        "message": "黄金の叡智。深い知恵と豊かさの体現。"
                   "自己認識を通じて真の豊かさを見出す。",
    },
}

# ボトルの色が対応するチャクラ・エネルギー
COLOR_MEANINGS = {
    "レッド": "生命力・グラウンディング・情熱・第1チャクラ",
    "オレンジ": "喜び・創造性・洞察・第2チャクラ",
    "イエロー": "知恵・自信・太陽の力・第3チャクラ",
    "ゴールド": "叡智・自己認識・内なる知恵",
    "グリーン": "ハート・調和・成長・第4チャクラ",
    "ターコイズ": "創造的コミュニケーション・遊び心",
    "ブルー": "平和・コミュニケーション・信頼・第5チャクラ",
    "ロイヤルブルー": "直感・深い洞察・第3の目",
    "バイオレット": "変容・スピリチュアリティ・奉仕・第7チャクラ",
    "パープル": "霊性・奉仕・献身",
    "マゼンタ": "神聖な愛・小さなことへの愛",
    "ディープマゼンタ": "神聖な目的・第8チャクラ",
    "ピンク": "無条件の愛・優しさ・自己受容",
    "ローズピンク": "深い愛・慈悲",
    "クリア": "明晰さ・浄化・光",
}


def _digit_sum(n: int) -> int:
    """数値の各桁を合算する。"""
    total = sum(int(d) for d in str(n))
    return total


def _reduce_to_range(n: int, max_val: int) -> int:
    """桁を畳み込んで指定範囲内に収める。"""
    while n > max_val:
        n = _digit_sum(n)
    return n


def _birth_bottle_number(year: int, month: int, day: int) -> int:
    """誕生日ボトル番号を算出する。

    YYYYMMDD の全桁を合計し、ボトル範囲（0-41）に収まるまで畳み込む。
    """
    digits = f"{year:04d}{month:02d}{day:02d}"
    total = sum(int(d) for d in digits)
    return _reduce_to_range(total, 41)


def _soul_bottle_number(birth_bottle: int) -> int:
    """ソウルボトル番号を算出する（誕生日ボトル番号をさらに一桁に畳み込み）。"""
    result = birth_bottle
    while result > 9:
        result = _digit_sum(result)
    return result


def calculate(birth_data: BirthData) -> DivinationResult:
    """オーラソーマ誕生日ボトルの鑑定を行う。"""
    bd = birth_data.birth_date
    birth_num = _birth_bottle_number(bd.year, bd.month, bd.day)
    soul_num = _soul_bottle_number(birth_num)

    birth_bottle = BOTTLES.get(birth_num)
    soul_bottle = BOTTLES.get(soul_num)

    if not birth_bottle:
        return DivinationResult(
            system_name="オーラソーマ",
            system_id="aura_soma",
            summary=f"誕生日ボトル: #{birth_num}（データ範囲外）",
            details={"birth_bottle_number": birth_num, "soul_bottle_number": soul_num},
            interpretation="ボトルデータが見つかりませんでした。",
            warnings=["ボトル番号がデータ範囲外です。"],
        )

    # 色の意味を取得
    upper_meaning = COLOR_MEANINGS.get(birth_bottle["upper"], "")
    lower_meaning = COLOR_MEANINGS.get(birth_bottle["lower"], "")

    soul_info = ""
    soul_details = {}
    if soul_bottle:
        soul_info = (
            f"\n\n【ソウルボトル】#{soul_num} {soul_bottle['name']}\n"
            f"色: {soul_bottle['upper']} / {soul_bottle['lower']}\n"
            f"テーマ: {soul_bottle['theme']}\n"
            f"魂のメッセージ: {soul_bottle['message']}"
        )
        soul_details = {
            "number": soul_num,
            "name": soul_bottle["name"],
            "upper_color": soul_bottle["upper"],
            "lower_color": soul_bottle["lower"],
            "theme": soul_bottle["theme"],
            "message": soul_bottle["message"],
        }

    return DivinationResult(
        system_name="オーラソーマ",
        system_id="aura_soma",
        summary=f"誕生日ボトル: #{birth_num} {birth_bottle['name']}（{birth_bottle['upper']} / {birth_bottle['lower']}）",
        details={
            "birth_bottle": {
                "number": birth_num,
                "name": birth_bottle["name"],
                "upper_color": birth_bottle["upper"],
                "lower_color": birth_bottle["lower"],
                "theme": birth_bottle["theme"],
                "message": birth_bottle["message"],
                "upper_meaning": upper_meaning,
                "lower_meaning": lower_meaning,
            },
            "soul_bottle": soul_details,
        },
        interpretation=(
            f"【誕生日ボトル】#{birth_num} {birth_bottle['name']}\n"
            f"色: {birth_bottle['upper']}（上層）/ {birth_bottle['lower']}（下層）\n\n"
            f"【テーマ】{birth_bottle['theme']}\n\n"
            f"【メッセージ】{birth_bottle['message']}\n\n"
            f"【上層の色の意味】{birth_bottle['upper']}: {upper_meaning}\n"
            f"  意識的な自分、外に見せている姿を表します。\n\n"
            f"【下層の色の意味】{birth_bottle['lower']}: {lower_meaning}\n"
            f"  無意識の自分、内に秘めた本質を表します。"
            f"{soul_info}"
        ),
    )
