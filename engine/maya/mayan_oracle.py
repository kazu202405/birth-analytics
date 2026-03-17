"""マヤンオラクル（マヤ暦オラクルカード的解釈）

マヤ暦ツォルキンの計算結果をもとに、各紋章の関係性（オラクル）を
より深い意味と詳細な解釈で読み解く。maya_calendar モジュールのラッパー。
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult
from utils.constants import MAYA_SOLAR_SEALS
from maya.maya_calendar import (
    _calc_kin, _wavespell_seal, _guide_seal,
    _antipodal_seal, _occult_seal, _analog_seal,
    TONE_MEANINGS, SEAL_COLORS,
)

# ── 20の太陽の紋章の詳細解釈 ──
SEAL_ORACLE = {
    "赤い竜": {
        "keyword": "誕生・生命力・育む",
        "essence": "根源的な生命エネルギーの象徴。母なる大地の力を持ち、"
                   "すべての始まりと創造の源泉。無条件の愛と保護の力。",
        "gift": "新しいものを生み出す創造力と、人を育てる包容力",
        "challenge": "過保護や支配的になりやすい面。手放すことを学ぶ必要がある",
        "question": "あなたは何を生み出し、何を育てたいですか？",
    },
    "白い風": {
        "keyword": "スピリット・コミュニケーション・呼吸",
        "essence": "精神世界と物質世界をつなぐメッセンジャー。目に見えない"
                   "ものを感じ取り、言葉や表現を通じて伝える力。",
        "gift": "繊細な感受性と、見えない世界を感じ取るスピリチュアルな力",
        "challenge": "感受性の高さゆえに傷つきやすい。地に足をつけることが課題",
        "question": "あなたのスピリットは何を伝えようとしていますか？",
    },
    "青い夜": {
        "keyword": "夢・豊かさ・直感",
        "essence": "夢と潜在意識の世界を司る。内なるビジョンを現実に"
                   "変換する力を持ち、豊かさの源泉にアクセスできる。",
        "gift": "壮大な夢を描き、それを現実化するビジョンの力",
        "challenge": "夢想に溺れて現実から離れがち。地に足のついた行動が必要",
        "question": "あなたの深層にある本当の夢は何ですか？",
    },
    "黄色い種": {
        "keyword": "開花・目覚め・可能性",
        "essence": "無限の可能性の種。知的探究心と気づきの力を持ち、"
                   "物事の本質を見抜いて花開かせる力がある。",
        "gift": "知的好奇心と、物事の本質を見抜く洞察力",
        "challenge": "可能性を追いすぎて一つに絞れない。集中力が課題",
        "question": "あなたの中のどの種を開花させたいですか？",
    },
    "赤い蛇": {
        "keyword": "本能・情熱・生存力",
        "essence": "生命の根源的なエネルギー。本能と情熱の力を持ち、"
                   "サバイバル能力と変容（脱皮）の力に満ちている。",
        "gift": "強い生命力と、状況を生き抜く本能的な力",
        "challenge": "欲望や執着に振り回されやすい。感情のコントロールが課題",
        "question": "あなたの本能は何を求めていますか？",
    },
    "白い世界の橋渡し": {
        "keyword": "死と再生・橋渡し・手放し",
        "essence": "異なる世界をつなぐ架け橋。古いものを手放し、"
                   "新しいステージへと導く変容の力を持つ。",
        "gift": "人と人、世界と世界をつなぐコーディネート力",
        "challenge": "手放すことへの恐れ。変化を受け入れる勇気が必要",
        "question": "今、手放すべきものは何ですか？",
    },
    "青い手": {
        "keyword": "遂行・癒し・把握",
        "essence": "実際に手を動かして物事を成し遂げる力。癒しの手を持ち、"
                   "触れるものに変化をもたらす。体験を通じて理解する。",
        "gift": "ヒーリング能力と、物事を完成させる実行力",
        "challenge": "やりすぎて疲弊しやすい。自分自身の癒しも忘れずに",
        "question": "あなたの手で何を成し遂げたいですか？",
    },
    "黄色い星": {
        "keyword": "美・調和・芸術",
        "essence": "美と調和の象徴。芸術的な感性を持ち、周囲に美しさと"
                   "エレガンスをもたらす。完成形を見据える力。",
        "gift": "美的センスと、物事を調和させるバランス感覚",
        "challenge": "完璧主義に陥りやすい。不完全さも受け入れる寛容さが必要",
        "question": "あなたにとっての美しさとは何ですか？",
    },
    "赤い月": {
        "keyword": "浄化・流れ・普遍的な水",
        "essence": "浄化と新しい流れの象徴。感情の水を浄化し、"
                   "新しいエネルギーの流れを生み出す力を持つ。",
        "gift": "浄化力と、物事に新しい流れを作る開拓精神",
        "challenge": "感情の波に翻弄されやすい。安定した軸を持つことが大切",
        "question": "何を浄化し、どんな新しい流れを作りたいですか？",
    },
    "白い犬": {
        "keyword": "愛・忠誠・ハート",
        "essence": "無条件の愛と忠誠心の象徴。ハートの知性を持ち、"
                   "誠実さと信頼で人との絆を深める力がある。",
        "gift": "深い愛情と忠誠心、人を信じる純粋な心",
        "challenge": "依存や盲目的な忠誠に注意。自立した愛を学ぶ必要がある",
        "question": "あなたのハートは何に忠実でありたいですか？",
    },
    "青い猿": {
        "keyword": "遊び・魔術・幻想",
        "essence": "遊び心と創造的なトリックスターのエネルギー。"
                   "マジカルな力で現実を変容させ、笑いとユーモアをもたらす。",
        "gift": "ユーモアのセンスと、遊び心から生まれる創造力",
        "challenge": "ふざけすぎて信頼を失いがち。真剣さとのバランスが大切",
        "question": "人生をもっと遊び心を持って楽しめていますか？",
    },
    "黄色い人": {
        "keyword": "自由意志・知恵・影響力",
        "essence": "自由意志と選択の力の象徴。高い知恵と影響力を持ち、"
                   "自分の人生を自らの意志で切り拓く力がある。",
        "gift": "自由な精神と、人に影響を与える知恵の力",
        "challenge": "自由を求めすぎて孤立しがち。協調性も大切にする",
        "question": "あなたの自由意志は何を選択していますか？",
    },
    "赤い空歩く者": {
        "keyword": "探究・空間・目覚め",
        "essence": "天と地の間を歩く探究者。未知の領域を探索し、"
                   "社会に奉仕する力と、人々を目覚めさせる使命を持つ。",
        "gift": "社会貢献への情熱と、人の可能性を引き出す力",
        "challenge": "現実離れしやすい。足元を固めながら進むことが大切",
        "question": "あなたはどんな新しい世界を探究したいですか？",
    },
    "白い魔法使い": {
        "keyword": "魅惑・受容・永遠",
        "essence": "時間を超越した魔法の力。すべてを受け入れる許しの力と、"
                   "目に見えない世界の知恵を現実に活かす力がある。",
        "gift": "許しと受容の力、スピリチュアルな知恵",
        "challenge": "受容しすぎて自分を見失いがち。健全な境界線が必要",
        "question": "あなたが許し、受け入れるべきことは何ですか？",
    },
    "青い鷲": {
        "keyword": "ビジョン・創造・心眼",
        "essence": "高い視点から全体像を見渡す鷲の目。先見の明があり、"
                   "ビジョンを具現化する創造力に満ちている。",
        "gift": "全体を俯瞰する視野と、未来を見通すビジョン",
        "challenge": "批判的になりやすい。高所からの視点を愛をもって活かす",
        "question": "あなたのビジョンが見せる未来はどんな姿ですか？",
    },
    "黄色い戦士": {
        "keyword": "知性・大胆さ・問い",
        "essence": "恐れを知らない精神の戦士。知性と勇気で困難に"
                   "立ち向かい、常に深い問いを探究し続ける力がある。",
        "gift": "困難を恐れない勇気と、深い問いを立てる知性",
        "challenge": "戦いに明け暮れて疲弊しがち。平和な時間も大切に",
        "question": "あなたが恐れずに問いかけたいことは何ですか？",
    },
    "赤い地球": {
        "keyword": "シンクロニシティ・ナビゲーション・地球",
        "essence": "地球と共鳴する力。シンクロニシティを通じて"
                   "導きを受け取り、正しい方向へナビゲートされる。",
        "gift": "シンクロニシティを感じ取る力と、地に足のついた安定感",
        "challenge": "サインを読み過ぎて行動が遅れがち。直感と行動の一致が大切",
        "question": "今、地球はあなたにどんなサインを送っていますか？",
    },
    "白い鏡": {
        "keyword": "果てしなさ・映し出す・秩序",
        "essence": "真実を映し出す鏡のエネルギー。あらゆる幻想を取り払い、"
                   "物事の本質と秩序を明らかにする力がある。",
        "gift": "真実を見抜く力と、秩序をもたらす明晰さ",
        "challenge": "真実の刃で人を傷つけやすい。優しさとのバランスが必要",
        "question": "鏡に映るあなたの本当の姿はどのようなものですか？",
    },
    "青い嵐": {
        "keyword": "変容・エネルギー・自己発生",
        "essence": "圧倒的な変容のエネルギー。嵐のように周囲を一変させ、"
                   "新しい世界を創り出す自己生成的な力を持つ。",
        "gift": "強大な変容の力と、触媒としてのエネルギー",
        "challenge": "破壊的になりすぎる危険。建設的な変容を心がける",
        "question": "あなたはどんな変容を起こしたいですか？",
    },
    "黄色い太陽": {
        "keyword": "普遍的な火・悟り・生命",
        "essence": "すべてを照らす太陽の光。悟りと無条件の愛の象徴で、"
                   "存在そのものが周囲に光をもたらす力がある。",
        "gift": "存在感と、周囲を照らす無条件の愛の力",
        "challenge": "自己中心的になりがち。謙虚さと感謝を忘れずに",
        "question": "あなたの光は何を照らしていますか？",
    },
}

# ── オラクルの5つの力の解説 ──
ORACLE_ROLES = {
    "main": ("顕在意識", "あなたが意識的に表現している力。太陽の紋章として、社会的に発揮される資質。"),
    "wavespell": ("潜在意識", "あなたの内面に眠る力。ウェイブスペルとして、無意識に影響する根源的なエネルギー。"),
    "guide": ("導きの力", "あなたを正しい方向へ導く力。迷った時に立ち返るべき指針となるエネルギー。"),
    "antipodal": ("挑戦と広がりの力", "あなたの成長を促す対極の力。困難に見えて、実は視野を広げてくれるエネルギー。"),
    "occult": ("神秘の力", "あなたの隠された才能。予想外の形で現れる突然変異的な力。深いレベルでの気づきをもたらす。"),
    "analog": ("類似の力", "あなたを支え、共鳴する力。最も自然に協力し合えるエネルギーで、居心地の良さをもたらす。"),
}


def _get_seal_info(seal_name: str) -> dict:
    """紋章の詳細情報を取得する。"""
    info = SEAL_ORACLE.get(seal_name, {})
    return {
        "name": seal_name,
        "keyword": info.get("keyword", ""),
        "essence": info.get("essence", ""),
        "gift": info.get("gift", ""),
        "challenge": info.get("challenge", ""),
        "question": info.get("question", ""),
    }


def _build_interpretation(
    kin: int,
    tone: int,
    main_seal: str,
    ws_seal: str,
    guide_seal_name: str,
    anti_seal: str,
    occult_seal_name: str,
    analog_seal_name: str,
    color: str,
) -> str:
    """マヤンオラクルの総合解釈テキストを生成する。"""
    lines = []

    lines.append(f"【KIN {kin} / 銀河の音 {tone}】")
    lines.append(f"{TONE_MEANINGS.get(tone, '')}")
    lines.append("")

    # メイン紋章
    main_info = SEAL_ORACLE.get(main_seal, {})
    lines.append(f"【太陽の紋章（顕在意識）: {main_seal}】")
    lines.append(f"  キーワード: {main_info.get('keyword', '')}")
    lines.append(f"  {main_info.get('essence', '')}")
    lines.append(f"  ギフト: {main_info.get('gift', '')}")
    lines.append(f"  チャレンジ: {main_info.get('challenge', '')}")
    lines.append(f"  問いかけ: {main_info.get('question', '')}")
    lines.append("")

    # ウェイブスペル
    ws_info = SEAL_ORACLE.get(ws_seal, {})
    lines.append(f"【ウェイブスペル（潜在意識）: {ws_seal}】")
    lines.append(f"  キーワード: {ws_info.get('keyword', '')}")
    lines.append(f"  {ws_info.get('essence', '')}")
    lines.append("")

    # ガイド
    guide_info = SEAL_ORACLE.get(guide_seal_name, {})
    lines.append(f"【ガイドキン（導き）: {guide_seal_name}】")
    lines.append(f"  キーワード: {guide_info.get('keyword', '')}")
    lines.append(f"  {guide_info.get('essence', '')}")
    lines.append("")

    # 反対キン
    anti_info = SEAL_ORACLE.get(anti_seal, {})
    lines.append(f"【反対キン（挑戦と広がり）: {anti_seal}】")
    lines.append(f"  キーワード: {anti_info.get('keyword', '')}")
    lines.append(f"  {anti_info.get('challenge', '')}")
    lines.append("")

    # 神秘キン
    occult_info = SEAL_ORACLE.get(occult_seal_name, {})
    lines.append(f"【神秘キン（隠された力）: {occult_seal_name}】")
    lines.append(f"  キーワード: {occult_info.get('keyword', '')}")
    lines.append(f"  {occult_info.get('gift', '')}")
    lines.append("")

    # 類似キン
    analog_info = SEAL_ORACLE.get(analog_seal_name, {})
    lines.append(f"【類似キン（支え合う力）: {analog_seal_name}】")
    lines.append(f"  キーワード: {analog_info.get('keyword', '')}")
    lines.append(f"  {analog_info.get('essence', '')}")
    lines.append("")

    # 色の意味
    color_meanings = {
        "赤": "赤は「起承転結」の「起」。新しいエネルギーを生み出す始まりの力です。",
        "白": "白は「起承転結」の「承」。物事を洗練し、磨き上げる力です。",
        "青": "青は「起承転結」の「転」。変容と深化をもたらす力です。",
        "黄": "黄は「起承転結」の「結」。物事を完成させ、次の段階へと導く力です。",
    }
    lines.append(f"【色: {color}】")
    lines.append(f"  {color_meanings.get(color, '')}")

    return "\n".join(lines)


def calculate(birth_data: BirthData) -> DivinationResult:
    """マヤンオラクルを算出する。"""
    bd = birth_data.birth_date
    kin = _calc_kin(bd)

    seal_index = (kin - 1) % 20
    tone = (kin - 1) % 13 + 1
    main_seal = MAYA_SOLAR_SEALS[seal_index]
    color_index = seal_index % 4
    color = SEAL_COLORS[color_index]

    ws_index = _wavespell_seal(kin)
    guide_index = _guide_seal(kin, seal_index, tone)
    anti_index = _antipodal_seal(seal_index)
    occult_index = _occult_seal(seal_index)
    analog_index = _analog_seal(seal_index)

    ws_seal = MAYA_SOLAR_SEALS[ws_index]
    guide_seal_name = MAYA_SOLAR_SEALS[guide_index]
    anti_seal = MAYA_SOLAR_SEALS[anti_index]
    occult_seal_name = MAYA_SOLAR_SEALS[occult_index]
    analog_seal_name = MAYA_SOLAR_SEALS[analog_index]

    interpretation = _build_interpretation(
        kin, tone, main_seal, ws_seal, guide_seal_name,
        anti_seal, occult_seal_name, analog_seal_name, color,
    )

    oracle = {
        "main": _get_seal_info(main_seal),
        "wavespell": _get_seal_info(ws_seal),
        "guide": _get_seal_info(guide_seal_name),
        "antipodal": _get_seal_info(anti_seal),
        "occult": _get_seal_info(occult_seal_name),
        "analog": _get_seal_info(analog_seal_name),
    }

    return DivinationResult(
        system_name="マヤンオラクル",
        system_id="mayan_oracle",
        summary=f"KIN {kin} {main_seal} 音{tone} ─ {SEAL_ORACLE.get(main_seal, {}).get('keyword', '')}",
        details={
            "kin": kin,
            "tone": tone,
            "tone_meaning": TONE_MEANINGS.get(tone, ""),
            "color": color,
            "oracle": oracle,
        },
        interpretation=interpretation,
    )
