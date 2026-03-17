"""数秘バイブレーション — ライフパスナンバーから振動特性を算出"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


MASTER_NUMBERS = {11, 22, 33}

VIBRATIONS = {
    1: {
        "level": "低振動（地上的）", "frequency": "基本", "element": "火",
        "tone": "C", "crystal": "ルビー", "trait": "実践的・行動力・自立",
        "description": "物質世界の始まりのエネルギー。自ら道を切り開く開拓者の振動を持ちます。",
        "affirmation": "私は自らの力で道を創造する",
    },
    2: {
        "level": "低振動（地上的）", "frequency": "調和", "element": "水",
        "tone": "D", "crystal": "ムーンストーン", "trait": "協調・受容・感受性",
        "description": "月のように受容するエネルギー。他者との調和を通じて力を発揮します。",
        "affirmation": "私は調和の中に真の力を見出す",
    },
    3: {
        "level": "中振動（創造的）", "frequency": "表現", "element": "火",
        "tone": "E", "crystal": "シトリン", "trait": "創造性・表現力・楽観",
        "description": "太陽のように明るく照らすエネルギー。創造的な表現を通じて世界に影響を与えます。",
        "affirmation": "私は創造の喜びを世界と分かち合う",
    },
    4: {
        "level": "低振動（地上的）", "frequency": "安定", "element": "土",
        "tone": "F", "crystal": "エメラルド", "trait": "堅実・秩序・努力",
        "description": "大地のように揺るがないエネルギー。着実な積み重ねで確かな基盤を築きます。",
        "affirmation": "私は堅固な基盤の上に未来を築く",
    },
    5: {
        "level": "中振動（創造的）", "frequency": "変化", "element": "風",
        "tone": "G", "crystal": "ターコイズ", "trait": "自由・冒険・変革",
        "description": "風のように自由なエネルギー。変化を恐れず新しい体験を求めます。",
        "affirmation": "私は変化の風に乗り自由に飛翔する",
    },
    6: {
        "level": "低振動（地上的）", "frequency": "調和", "element": "土",
        "tone": "A", "crystal": "ローズクォーツ", "trait": "愛・責任・奉仕",
        "description": "愛と責任のエネルギー。家庭やコミュニティに献身的な調和をもたらします。",
        "affirmation": "私は無条件の愛で周囲を包む",
    },
    7: {
        "level": "中振動（創造的）", "frequency": "探究", "element": "水",
        "tone": "B", "crystal": "アメジスト", "trait": "分析・神秘・内省",
        "description": "深海のように深いエネルギー。内なる真実を探求し、神秘を解き明かします。",
        "affirmation": "私は内なる叡智に耳を傾ける",
    },
    8: {
        "level": "低振動（地上的）", "frequency": "達成", "element": "土",
        "tone": "C(高)", "crystal": "タイガーアイ", "trait": "成功・権威・物質",
        "description": "物質世界を統率するエネルギー。目標を達成し、豊かさを現実化します。",
        "affirmation": "私は豊かさを引き寄せ形にする",
    },
    9: {
        "level": "高振動（霊的）", "frequency": "完成", "element": "火",
        "tone": "D(高)", "crystal": "ガーネット", "trait": "博愛・叡智・完成",
        "description": "完成と昇華のエネルギー。全てを包容する叡智で世界に奉仕します。",
        "affirmation": "私は全てとつながり叡智を分かち合う",
    },
    11: {
        "level": "高振動（霊的）", "frequency": "直感", "element": "風",
        "tone": "E(高)", "crystal": "ラブラドライト", "trait": "霊感・ビジョン・啓示",
        "description": "高次の直感を受信するエネルギー。見えない世界のメッセージを地上に伝えます。",
        "affirmation": "私は高次の導きを信頼し受け取る",
    },
    22: {
        "level": "高振動（霊的）", "frequency": "建設", "element": "土",
        "tone": "F(高)", "crystal": "モルダバイト", "trait": "マスタービルダー・大規模実現",
        "description": "霊的なビジョンを物質世界に具現化するエネルギー。壮大な計画を実現する力を持ちます。",
        "affirmation": "私はビジョンを地上に具現化する",
    },
    33: {
        "level": "高振動（霊的）", "frequency": "無条件の愛", "element": "水",
        "tone": "G(高)", "crystal": "セレスタイト", "trait": "宇宙的慈悲・癒し・奉仕",
        "description": "宇宙的な慈悲のエネルギー。無条件の愛で全ての存在を癒します。",
        "affirmation": "私は宇宙の愛そのものである",
    },
}

# 振動レベル間の相性
VIBRATION_COMPATIBILITY = {
    "低振動（地上的）": "地に足のついた現実的なエネルギーで、物質世界での成功に適しています。",
    "中振動（創造的）": "創造性と表現力に溢れるエネルギーで、芸術や革新の分野に適しています。",
    "高振動（霊的）": "霊的な高みのエネルギーで、精神世界と物質世界の橋渡しに適しています。",
}

# 五元素の特性
ELEMENT_TRAITS = {
    "火": "行動力・情熱・変革のエネルギー",
    "水": "感受性・直感・浄化のエネルギー",
    "土": "安定・堅実・具現化のエネルギー",
    "風": "知性・自由・コミュニケーションのエネルギー",
}


def _calc_life_path(year: int, month: int, day: int) -> int:
    """ライフパスナンバーを算出（マスターナンバー考慮）"""
    # 各部分をまず単独で縮約
    def reduce(n: int) -> int:
        while n > 9 and n not in MASTER_NUMBERS:
            n = sum(int(d) for d in str(n))
        return n

    y_sum = reduce(sum(int(d) for d in str(year)))
    m_sum = reduce(month)
    d_sum = reduce(day)

    total = y_sum + m_sum + d_sum
    return reduce(total)


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date
    life_path = _calc_life_path(bd.year, bd.month, bd.day)

    vib = VIBRATIONS[life_path]
    is_master = life_path in MASTER_NUMBERS
    level_desc = VIBRATION_COMPATIBILITY[vib["level"]]
    element_desc = ELEMENT_TRAITS[vib["element"]]

    # 基礎ナンバー（マスターナンバーの場合、還元した数も表示）
    base_number = None
    if is_master:
        base_number = sum(int(d) for d in str(life_path))
        if base_number > 9:
            base_number = sum(int(d) for d in str(base_number))

    details = {
        "life_path_number": life_path,
        "is_master_number": is_master,
        "base_number": base_number,
        "vibration_level": vib["level"],
        "frequency": vib["frequency"],
        "element": vib["element"],
        "musical_tone": vib["tone"],
        "crystal": vib["crystal"],
        "trait": vib["trait"],
        "affirmation": vib["affirmation"],
    }

    master_note = ""
    if is_master:
        master_note = (
            f"\n\n【マスターナンバー {life_path}】\n"
            f"マスターナンバーは高い霊的使命を示す特別な数字です。\n"
            f"基礎ナンバー{base_number}のエネルギーも内包しています。"
        )

    interpretation = (
        f"ライフパスナンバー: {life_path}\n"
        f"振動レベル: {vib['level']}\n"
        f"周波数タイプ: {vib['frequency']}\n\n"
        f"【特性】{vib['trait']}\n"
        f"{vib['description']}\n\n"
        f"【エレメント】{vib['element']} — {element_desc}\n"
        f"【音のトーン】{vib['tone']}\n"
        f"【パワーストーン】{vib['crystal']}\n\n"
        f"【振動レベルの意味】\n{level_desc}\n\n"
        f"【アファメーション】\n「{vib['affirmation']}」"
        f"{master_note}"
    )

    return DivinationResult(
        system_name="数秘バイブレーション",
        system_id="numerology_vibration",
        summary=f"ライフパス{life_path}: {vib['frequency']}の振動（{vib['level']}）",
        details=details,
        interpretation=interpretation,
    )
