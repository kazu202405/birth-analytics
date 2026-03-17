"""守護天使ナンバー（72天使 - カバラの天使学）"""
from datetime import date
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


GUARDIAN_ANGELS = [
    # 1-8: 春分から (3/21 - 5/20)
    {"number": 1, "name": "ヴェフエル (Vehuiah)", "period": (3, 21, 3, 25), "quality": "意志力・新しい始まり", "psalm": "詩篇3:4"},
    {"number": 2, "name": "イェリエル (Jeliel)", "period": (3, 26, 3, 30), "quality": "愛・知恵・忠誠", "psalm": "詩篇22:20"},
    {"number": 3, "name": "シタエル (Sitael)", "period": (3, 31, 4, 4), "quality": "建設・保護・逆境の克服", "psalm": "詩篇91:2"},
    {"number": 4, "name": "エレミヤ (Elemiah)", "period": (4, 5, 4, 9), "quality": "神の力・旅の守護", "psalm": "詩篇6:5"},
    {"number": 5, "name": "マハシヤ (Mahasiah)", "period": (4, 10, 4, 14), "quality": "調和・平和・学習", "psalm": "詩篇34:5"},
    {"number": 6, "name": "レラヘル (Lelahel)", "period": (4, 15, 4, 20), "quality": "光・癒し・理解", "psalm": "詩篇9:12"},
    {"number": 7, "name": "アカイア (Achaiah)", "period": (4, 21, 4, 25), "quality": "忍耐・知識の発見", "psalm": "詩篇103:8"},
    {"number": 8, "name": "カヘテル (Cahetel)", "period": (4, 26, 4, 30), "quality": "豊穣・神の祝福", "psalm": "詩篇95:6"},
    # 9-16: (5/1 - 6/20)
    {"number": 9, "name": "ハジエル (Haziel)", "period": (5, 1, 5, 5), "quality": "慈悲・赦し・友情", "psalm": "詩篇25:6"},
    {"number": 10, "name": "アラディア (Aladiah)", "period": (5, 6, 5, 10), "quality": "恩寵・罪の清め・再生", "psalm": "詩篇33:22"},
    {"number": 11, "name": "ラウヴィア (Lauviah)", "period": (5, 11, 5, 15), "quality": "啓示・直感・勝利", "psalm": "詩篇18:47"},
    {"number": 12, "name": "ハハイア (Hahaiah)", "period": (5, 16, 5, 20), "quality": "避難所・夢の解釈", "psalm": "詩篇10:1"},
    {"number": 13, "name": "イェザレル (Iezalel)", "period": (5, 21, 5, 25), "quality": "忠誠・調和・和解", "psalm": "詩篇98:4"},
    {"number": 14, "name": "メバヘル (Mebahel)", "period": (5, 26, 5, 31), "quality": "真実・正義・解放", "psalm": "詩篇9:10"},
    {"number": 15, "name": "ハリエル (Hariel)", "period": (6, 1, 6, 5), "quality": "浄化・信仰・科学的発見", "psalm": "詩篇94:22"},
    {"number": 16, "name": "ハカミア (Hekamiah)", "period": (6, 6, 6, 10), "quality": "忠誠・指導力・国家の守護", "psalm": "詩篇88:2"},
    # 17-24: (6/11 - 8/10)
    {"number": 17, "name": "ラウヴィア2 (Lauviah II)", "period": (6, 11, 6, 15), "quality": "啓示・夢の理解・知恵", "psalm": "詩篇8:2"},
    {"number": 18, "name": "カリエル (Caliel)", "period": (6, 16, 6, 21), "quality": "正義・真実の勝利", "psalm": "詩篇35:24"},
    {"number": 19, "name": "レウヴィア (Leuviah)", "period": (6, 22, 6, 26), "quality": "記憶力・恩寵・忍耐", "psalm": "詩篇40:2"},
    {"number": 20, "name": "パハリア (Pahaliah)", "period": (6, 27, 7, 1), "quality": "道徳・精神性・贖い", "psalm": "詩篇120:2"},
    {"number": 21, "name": "ネルカエル (Nelchael)", "period": (7, 2, 7, 6), "quality": "学問・知識・忍耐", "psalm": "詩篇31:15"},
    {"number": 22, "name": "イェイアエル (Yeiayel)", "period": (7, 7, 7, 11), "quality": "名声・外交・尊敬", "psalm": "詩篇121:5"},
    {"number": 23, "name": "メラヘル (Melahel)", "period": (7, 12, 7, 16), "quality": "癒し・自然の力・健康", "psalm": "詩篇121:8"},
    {"number": 24, "name": "ハフユヤ (Haheuiah)", "period": (7, 17, 7, 22), "quality": "保護・亡命者の守護", "psalm": "詩篇33:18"},
    # 25-32: (7/23 - 9/12)
    {"number": 25, "name": "ニトハイア (Nith-Haiah)", "period": (7, 23, 7, 27), "quality": "知恵・魔術・霊的理解", "psalm": "詩篇9:2"},
    {"number": 26, "name": "ハアイア (Haaiah)", "period": (7, 28, 8, 1), "quality": "政治的知恵・外交・裁量", "psalm": "詩篇119:145"},
    {"number": 27, "name": "イェラテル (Yerathel)", "period": (8, 2, 8, 6), "quality": "光の伝播・文明・正義", "psalm": "詩篇140:2"},
    {"number": 28, "name": "シェアヒア (Seheiah)", "period": (8, 7, 8, 12), "quality": "長寿・健康・災害からの保護", "psalm": "詩篇71:12"},
    {"number": 29, "name": "レイイエル (Reiyel)", "period": (8, 13, 8, 17), "quality": "解放・啓蒙・真実の探求", "psalm": "詩篇54:6"},
    {"number": 30, "name": "オマエル (Omael)", "period": (8, 18, 8, 22), "quality": "忍耐・豊穣・種の繁栄", "psalm": "詩篇71:5"},
    {"number": 31, "name": "レカベル (Lecabel)", "period": (8, 23, 8, 28), "quality": "知性・才能・成功", "psalm": "詩篇71:16"},
    {"number": 32, "name": "ヴァサリア (Vasariah)", "period": (8, 29, 9, 2), "quality": "正義・寛大・高潔", "psalm": "詩篇33:4"},
    # 33-40: (9/3 - 11/2)
    {"number": 33, "name": "イェフヤ (Yehuiah)", "period": (9, 3, 9, 7), "quality": "従順・階級の維持・知恵", "psalm": "詩篇94:11"},
    {"number": 34, "name": "レハヒア (Lehahiah)", "period": (9, 8, 9, 12), "quality": "服従・統治・安定", "psalm": "詩篇131:3"},
    {"number": 35, "name": "カヴァキア (Chavaquiah)", "period": (9, 13, 9, 17), "quality": "和解・調和・家族の絆", "psalm": "詩篇116:1"},
    {"number": 36, "name": "メナデル (Menadel)", "period": (9, 18, 9, 23), "quality": "労働・職業の守護・解放", "psalm": "詩篇26:8"},
    {"number": 37, "name": "アニエル (Aniel)", "period": (9, 24, 9, 28), "quality": "勇気・神の息吹・啓示", "psalm": "詩篇80:20"},
    {"number": 38, "name": "ハアミア (Haamiah)", "period": (9, 29, 10, 3), "quality": "儀式・真実・礼拝の守護", "psalm": "詩篇91:9"},
    {"number": 39, "name": "レハエル (Rehael)", "period": (10, 4, 10, 8), "quality": "親子の絆・従順・治癒", "psalm": "詩篇30:11"},
    {"number": 40, "name": "イェイアゼル (Ieiazel)", "period": (10, 9, 10, 13), "quality": "慰め・解放・芸術の才能", "psalm": "詩篇88:15"},
    # 41-48: (10/14 - 12/13)
    {"number": 41, "name": "ハハヘル (Hahahel)", "period": (10, 14, 10, 18), "quality": "聖職・信仰・霊的使命", "psalm": "詩篇120:2"},
    {"number": 42, "name": "ミカエル (Mikael)", "period": (10, 19, 10, 23), "quality": "政治的権威・忠誠・安全", "psalm": "詩篇121:7"},
    {"number": 43, "name": "ヴェウリア (Veuliah)", "period": (10, 24, 10, 28), "quality": "繁栄・勝利・解放", "psalm": "詩篇88:14"},
    {"number": 44, "name": "イェラヒア (Yelahiah)", "period": (10, 29, 11, 2), "quality": "戦いの勝利・正義の力", "psalm": "詩篇119:108"},
    {"number": 45, "name": "セアリア (Sealiah)", "period": (11, 3, 11, 7), "quality": "動機・意志・堕落者の再生", "psalm": "詩篇94:18"},
    {"number": 46, "name": "アリエル (Ariel)", "period": (11, 8, 11, 12), "quality": "自然の秘密・発見・啓示", "psalm": "詩篇145:9"},
    {"number": 47, "name": "アサリア (Asaliah)", "period": (11, 13, 11, 17), "quality": "真理の観照・高次の知恵", "psalm": "詩篇104:24"},
    {"number": 48, "name": "ミハエル (Mihael)", "period": (11, 18, 11, 22), "quality": "豊穣・夫婦の調和・預言", "psalm": "詩篇98:2"},
    # 49-56: (11/23 - 1/20)
    {"number": 49, "name": "ヴェフエル2 (Vehuel)", "period": (11, 23, 11, 27), "quality": "高揚・名声・寛大な精神", "psalm": "詩篇145:3"},
    {"number": 50, "name": "ダニエル (Daniel)", "period": (11, 28, 12, 2), "quality": "雄弁・慈悲・決断", "psalm": "詩篇103:8"},
    {"number": 51, "name": "ハハシア (Hahasiah)", "period": (12, 3, 12, 7), "quality": "医学・秘儀・高次の科学", "psalm": "詩篇104:31"},
    {"number": 52, "name": "イマミア (Imamiah)", "period": (12, 8, 12, 12), "quality": "旅の守護・償い・忍耐", "psalm": "詩篇7:18"},
    {"number": 53, "name": "ナナエル (Nanael)", "period": (12, 13, 12, 16), "quality": "霊的コミュニケーション・瞑想", "psalm": "詩篇119:75"},
    {"number": 54, "name": "ニタエル (Nithael)", "period": (12, 17, 12, 21), "quality": "永遠の若さ・王族の守護", "psalm": "詩篇103:19"},
    {"number": 55, "name": "メバヒア (Mebahiah)", "period": (12, 22, 12, 26), "quality": "知的明晰・道徳・子供の守護", "psalm": "詩篇102:13"},
    {"number": 56, "name": "ポイエル (Poyel)", "period": (12, 27, 12, 31), "quality": "豊穣・才能・謙虚", "psalm": "詩篇145:14"},
    {"number": 57, "name": "ネマミア (Nemamiah)", "period": (1, 1, 1, 5), "quality": "正義の戦い・高潔・将軍の守護", "psalm": "詩篇115:11"},
    {"number": 58, "name": "イェイアレル (Yeialel)", "period": (1, 6, 1, 10), "quality": "精神力・悲しみからの回復", "psalm": "詩篇6:4"},
    {"number": 59, "name": "ハラヘル (Harahel)", "period": (1, 11, 1, 15), "quality": "知識・出版・学問の守護", "psalm": "詩篇113:3"},
    {"number": 60, "name": "ミツラエル (Mitzrael)", "period": (1, 16, 1, 20), "quality": "内なる治癒・精神疾患の癒し", "psalm": "詩篇145:17"},
    # 61-68: (1/21 - 3/10)
    {"number": 61, "name": "ウマベル (Umabel)", "period": (1, 21, 1, 25), "quality": "友情・類似性・物理学", "psalm": "詩篇113:2"},
    {"number": 62, "name": "イアヘル (Iah-Hel)", "period": (1, 26, 1, 30), "quality": "知恵の追求・哲学・隠遁", "psalm": "詩篇119:159"},
    {"number": 63, "name": "アナウエル (Anauel)", "period": (1, 31, 2, 4), "quality": "統一・知覚・商業の守護", "psalm": "詩篇100:2"},
    {"number": 64, "name": "メヒエル (Mehiel)", "period": (2, 5, 2, 9), "quality": "活性化・執筆・教育", "psalm": "詩篇33:18"},
    {"number": 65, "name": "ダマビア (Damabiah)", "period": (2, 10, 2, 14), "quality": "知恵の泉・海の守護・呪術解除", "psalm": "詩篇90:13"},
    {"number": 66, "name": "マナケル (Manakel)", "period": (2, 15, 2, 19), "quality": "夢の知識・水の力・穏やかさ", "psalm": "詩篇38:22"},
    {"number": 67, "name": "エヤエル (Eyael)", "period": (2, 20, 2, 24), "quality": "変容・昇華・長寿", "psalm": "詩篇37:4"},
    {"number": 68, "name": "ハブヒア (Habuhiah)", "period": (2, 25, 2, 29), "quality": "治癒・農業の守護・豊穣", "psalm": "詩篇106:1"},
    # 69-72: (3/1 - 3/20)
    {"number": 69, "name": "ロカヘル (Rochel)", "period": (3, 1, 3, 5), "quality": "復元・遺失物の発見・名声", "psalm": "詩篇16:5"},
    {"number": 70, "name": "ジャバミア (Jabamiah)", "period": (3, 6, 3, 10), "quality": "錬金術・変容・再生", "psalm": "詩篇1:1"},
    {"number": 71, "name": "ハイアイエル (Haiaiel)", "period": (3, 11, 3, 15), "quality": "武器・勇気・神の守護", "psalm": "詩篇109:30"},
    {"number": 72, "name": "ムミア (Mumiah)", "period": (3, 16, 3, 20), "quality": "再生・終わりと始まり・長寿", "psalm": "詩篇116:7"},
]


def _is_in_period(month: int, day: int, period: tuple[int, int, int, int]) -> bool:
    """誕生日が天使の守護期間内にあるか判定する。"""
    start_m, start_d, end_m, end_d = period
    target = (month, day)
    start = (start_m, start_d)
    end = (end_m, end_d)

    if start <= end:
        return start <= target <= end
    else:
        # 年をまたぐ期間への対応（本データでは発生しないが安全策）
        return target >= start or target <= end


def _find_guardian_angel(month: int, day: int) -> dict:
    """誕生日に対応する守護天使を見つける。"""
    for angel in GUARDIAN_ANGELS:
        if _is_in_period(month, day, angel["period"]):
            return angel
    # フォールバック: 見つからない場合（うるう年2/29など境界ケース）
    # 2/29は68番ハブヒアの期間に含まれる設計
    return GUARDIAN_ANGELS[0]


def _find_opposing_angel(angel_number: int) -> dict:
    """対極天使: 36番先の天使（72天使の円環上の対角）。"""
    opposing_num = ((angel_number - 1 + 36) % 72) + 1
    for angel in GUARDIAN_ANGELS:
        if angel["number"] == opposing_num:
            return angel
    return GUARDIAN_ANGELS[0]


def _get_choir(angel_number: int) -> dict:
    """天使の属する天使階級（9つの聖歌隊）を返す。"""
    choirs = [
        {"name": "セラフィム（熾天使）", "archangel": "メタトロン", "quality": "神への愛と献身"},
        {"name": "ケルビム（智天使）", "archangel": "ラジエル", "quality": "神の知恵と啓示"},
        {"name": "スローンズ（座天使）", "archangel": "ザフキエル", "quality": "神の正義と裁き"},
        {"name": "ドミニオンズ（主天使）", "archangel": "ザドキエル", "quality": "神の慈悲と恩寵"},
        {"name": "パワーズ（力天使）", "archangel": "カマエル", "quality": "神の力と勇気"},
        {"name": "ヴァーチューズ（能天使）", "archangel": "ミカエル", "quality": "神の美と奇跡"},
        {"name": "プリンシパリティーズ（権天使）", "archangel": "ハニエル", "quality": "神の勝利と栄光"},
        {"name": "アークエンジェルズ（大天使）", "archangel": "ラファエル", "quality": "神の癒しと導き"},
        {"name": "エンジェルズ（天使）", "archangel": "ガブリエル", "quality": "神のメッセージと啓示"},
    ]
    # 各聖歌隊に8天使ずつ
    choir_index = (angel_number - 1) // 8
    if choir_index >= len(choirs):
        choir_index = len(choirs) - 1
    return choirs[choir_index]


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date
    month, day = bd.month, bd.day

    guardian = _find_guardian_angel(month, day)
    opposing = _find_opposing_angel(guardian["number"])
    choir = _get_choir(guardian["number"])

    start_m, start_d, end_m, end_d = guardian["period"]
    period_str = f"{start_m}/{start_d} - {end_m}/{end_d}"

    return DivinationResult(
        system_name="守護天使ナンバー（72天使）",
        system_id="guardian_angel",
        summary=f"守護天使: 第{guardian['number']}天使 {guardian['name']}",
        details={
            "guardian_angel": {
                "number": guardian["number"],
                "name": guardian["name"],
                "period": period_str,
                "quality": guardian["quality"],
                "psalm": guardian["psalm"],
            },
            "choir": {
                "name": choir["name"],
                "archangel": choir["archangel"],
                "quality": choir["quality"],
            },
            "opposing_angel": {
                "number": opposing["number"],
                "name": opposing["name"],
                "quality": opposing["quality"],
            },
        },
        interpretation=(
            f"守護天使【第{guardian['number']}天使 {guardian['name']}】: {guardian['quality']}\n"
            f"関連聖句: {guardian['psalm']}\n"
            f"所属天使階級【{choir['name']}】: {choir['quality']}（大天使{choir['archangel']}の管轄）\n"
            f"対極天使【第{opposing['number']}天使 {opposing['name']}】: {opposing['quality']}"
        ),
    )
