"""易経バースデー卦（64卦） — 生年月日から易経の卦を算出"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


# 八卦（先天八卦の順序: 乾兌離震巽坎艮坤）
BAGUA_NAMES = ["乾", "兌", "離", "震", "巽", "坎", "艮", "坤"]

BAGUA_ATTRIBUTES = {
    "乾": {"象意": "天", "性質": "剛健", "方位": "南"},
    "兌": {"象意": "沢", "性質": "悦び", "方位": "南東"},
    "離": {"象意": "火", "性質": "明晰", "方位": "東"},
    "震": {"象意": "雷", "性質": "動き", "方位": "北東"},
    "巽": {"象意": "風", "性質": "浸透", "方位": "南西"},
    "坎": {"象意": "水", "性質": "険難", "方位": "西"},
    "艮": {"象意": "山", "性質": "静止", "方位": "北西"},
    "坤": {"象意": "地", "性質": "柔順", "方位": "北"},
}

# 64卦: (上卦index, 下卦index) -> {number, name, meaning}
# 上卦・下卦はBAGUA_NAMESのインデックス(0-7)
HEXAGRAMS = {
    (0, 0): {"number": 1, "name": "乾為天", "meaning": "創造・天の力・積極的な前進"},
    (0, 1): {"number": 10, "name": "天沢履", "meaning": "慎重な行動・礼節を守る"},
    (0, 2): {"number": 13, "name": "天火同人", "meaning": "協力・同志との結束"},
    (0, 3): {"number": 25, "name": "天雷无妄", "meaning": "無心・自然体で臨む"},
    (0, 4): {"number": 44, "name": "天風姤", "meaning": "出会い・偶然の巡り合わせ"},
    (0, 5): {"number": 6, "name": "天水訟", "meaning": "争い・慎重な判断が必要"},
    (0, 6): {"number": 33, "name": "天山遯", "meaning": "退却・戦略的な撤退"},
    (0, 7): {"number": 12, "name": "天地否", "meaning": "閉塞・忍耐の時期"},
    (1, 0): {"number": 43, "name": "沢天夬", "meaning": "決断・思い切った行動"},
    (1, 1): {"number": 58, "name": "兌為沢", "meaning": "喜び・和やかな交流"},
    (1, 2): {"number": 49, "name": "沢火革", "meaning": "変革・古きを改める"},
    (1, 3): {"number": 17, "name": "沢雷随", "meaning": "追従・流れに従う"},
    (1, 4): {"number": 28, "name": "沢風大過", "meaning": "過剰・重荷を背負う"},
    (1, 5): {"number": 47, "name": "沢水困", "meaning": "困窮・苦境を耐える"},
    (1, 6): {"number": 31, "name": "沢山咸", "meaning": "感応・心が通じ合う"},
    (1, 7): {"number": 45, "name": "沢地萃", "meaning": "集合・人が集まる"},
    (2, 0): {"number": 14, "name": "火天大有", "meaning": "大いなる所有・豊かさ"},
    (2, 1): {"number": 38, "name": "火沢睽", "meaning": "対立・視点の違い"},
    (2, 2): {"number": 30, "name": "離為火", "meaning": "文明・知性・美の追求"},
    (2, 3): {"number": 21, "name": "火雷噬嗑", "meaning": "障害を噛み砕く・決着"},
    (2, 4): {"number": 50, "name": "火風鼎", "meaning": "革新・新しい体制の確立"},
    (2, 5): {"number": 64, "name": "火水未済", "meaning": "未完成・まだ渡り切らない"},
    (2, 6): {"number": 56, "name": "火山旅", "meaning": "旅・一時的な滞在"},
    (2, 7): {"number": 35, "name": "火地晋", "meaning": "進歩・昇進・前進"},
    (3, 0): {"number": 34, "name": "雷天大壮", "meaning": "大いなる力・勢いに乗る"},
    (3, 1): {"number": 54, "name": "雷沢帰妹", "meaning": "従属・未熟さを自覚する"},
    (3, 2): {"number": 55, "name": "雷火豊", "meaning": "豊穣・盛大な時期"},
    (3, 3): {"number": 51, "name": "震為雷", "meaning": "衝撃・奮起・覚醒"},
    (3, 4): {"number": 32, "name": "雷風恒", "meaning": "恒常・持続する力"},
    (3, 5): {"number": 40, "name": "雷水解", "meaning": "解放・困難からの脱出"},
    (3, 6): {"number": 62, "name": "雷山小過", "meaning": "小さな超過・謙虚に進む"},
    (3, 7): {"number": 16, "name": "雷地予", "meaning": "喜び・準備・前向きな期待"},
    (4, 0): {"number": 9, "name": "風天小畜", "meaning": "小さな蓄え・少しずつ進む"},
    (4, 1): {"number": 61, "name": "風沢中孚", "meaning": "誠実・真心が通じる"},
    (4, 2): {"number": 37, "name": "風火家人", "meaning": "家庭・秩序ある暮らし"},
    (4, 3): {"number": 42, "name": "風雷益", "meaning": "利益・増加・恩恵"},
    (4, 4): {"number": 57, "name": "巽為風", "meaning": "浸透・穏やかな影響力"},
    (4, 5): {"number": 59, "name": "風水渙", "meaning": "散らす・執着を手放す"},
    (4, 6): {"number": 53, "name": "風山漸", "meaning": "漸進・段階的な発展"},
    (4, 7): {"number": 20, "name": "風地観", "meaning": "観察・広い視野で見る"},
    (5, 0): {"number": 5, "name": "水天需", "meaning": "待つ・忍耐強く時を待つ"},
    (5, 1): {"number": 60, "name": "水沢節", "meaning": "節度・適度な制限"},
    (5, 2): {"number": 63, "name": "水火既済", "meaning": "完成・物事の成就"},
    (5, 3): {"number": 3, "name": "水雷屯", "meaning": "困難な始まり・産みの苦しみ"},
    (5, 4): {"number": 48, "name": "水風井", "meaning": "井戸・変わらぬ恵み"},
    (5, 5): {"number": 29, "name": "坎為水", "meaning": "険難・困難を乗り越える"},
    (5, 6): {"number": 39, "name": "水山蹇", "meaning": "行き詰まり・迂回が必要"},
    (5, 7): {"number": 8, "name": "水地比", "meaning": "親和・助け合い・団結"},
    (6, 0): {"number": 26, "name": "山天大畜", "meaning": "大いなる蓄積・実力を養う"},
    (6, 1): {"number": 41, "name": "山沢損", "meaning": "減らす・損して得取れ"},
    (6, 2): {"number": 22, "name": "山火賁", "meaning": "装飾・美しく飾る"},
    (6, 3): {"number": 27, "name": "山雷頤", "meaning": "養い・自己の滋養"},
    (6, 4): {"number": 18, "name": "山風蠱", "meaning": "腐敗を正す・立て直し"},
    (6, 5): {"number": 4, "name": "山水蒙", "meaning": "蒙昧・学びの始まり"},
    (6, 6): {"number": 52, "name": "艮為山", "meaning": "静止・止まって観る"},
    (6, 7): {"number": 23, "name": "山地剥", "meaning": "剥落・衰退の時期"},
    (7, 0): {"number": 11, "name": "地天泰", "meaning": "安泰・天地の調和"},
    (7, 1): {"number": 19, "name": "地沢臨", "meaning": "臨む・積極的な関与"},
    (7, 2): {"number": 36, "name": "地火明夷", "meaning": "明を傷つける・隠忍"},
    (7, 3): {"number": 24, "name": "地雷復", "meaning": "回復・再出発"},
    (7, 4): {"number": 46, "name": "地風升", "meaning": "上昇・着実な向上"},
    (7, 5): {"number": 7, "name": "地水師", "meaning": "軍団・統率力"},
    (7, 6): {"number": 15, "name": "地山謙", "meaning": "謙虚・控えめな姿勢"},
    (7, 7): {"number": 2, "name": "坤為地", "meaning": "受容・大地の包容力"},
}

# 卦の追加解説（上卦・下卦の組み合わせによるアドバイス）
RELATIONSHIP_ADVICE = {
    "same": "上下同卦は、その性質が純粋に表れます。長所が強まる反面、偏りに注意が必要です。",
    "complement": "上下の卦が補い合う関係です。バランスの取れた運勢を示しています。",
    "tension": "上下の卦に緊張関係があります。内面と外面の調和を意識することが大切です。",
}


def _calc_trigram_indices(birth_data: BirthData) -> tuple[int, int]:
    """生年月日から上卦・下卦のインデックスを算出"""
    bd = birth_data.birth_date
    year = bd.year
    month = bd.month
    day = bd.day

    base_sum = year + month + day
    upper = base_sum % 8

    # 時刻がある場合はそれを使う、なければデフォルト6
    if birth_data.birth_time is not None:
        hour_offset = birth_data.birth_time.hour
    else:
        hour_offset = 6

    lower = (base_sum + hour_offset) % 8

    return upper, lower


def _get_relationship_type(upper: int, lower: int) -> str:
    """上卦・下卦の関係性タイプを判定"""
    if upper == lower:
        return "same"
    # 対卦（乾坤、兌艮、離坎、震巽）
    opposites = {(0, 7), (7, 0), (1, 6), (6, 1), (2, 5), (5, 2), (3, 4), (4, 3)}
    if (upper, lower) in opposites:
        return "complement"
    return "tension"


def calculate(birth_data: BirthData) -> DivinationResult:
    upper, lower = _calc_trigram_indices(birth_data)
    hexagram = HEXAGRAMS[(upper, lower)]
    upper_name = BAGUA_NAMES[upper]
    lower_name = BAGUA_NAMES[lower]
    upper_attr = BAGUA_ATTRIBUTES[upper_name]
    lower_attr = BAGUA_ATTRIBUTES[lower_name]
    rel_type = _get_relationship_type(upper, lower)

    details = {
        "hexagram_number": hexagram["number"],
        "hexagram_name": hexagram["name"],
        "upper_trigram": {
            "name": upper_name,
            "index": upper,
            "象意": upper_attr["象意"],
            "性質": upper_attr["性質"],
        },
        "lower_trigram": {
            "name": lower_name,
            "index": lower,
            "象意": lower_attr["象意"],
            "性質": lower_attr["性質"],
        },
        "relationship": rel_type,
        "has_birth_time": birth_data.birth_time is not None,
    }

    warnings = []
    if birth_data.birth_time is None:
        warnings.append("出生時刻が未指定のため、下卦の算出にデフォルト値（6）を使用しています。")

    interpretation = (
        f"第{hexagram['number']}卦 {hexagram['name']}\n"
        f"意味: {hexagram['meaning']}\n\n"
        f"上卦: {upper_name}（{upper_attr['象意']}・{upper_attr['性質']}）\n"
        f"下卦: {lower_name}（{lower_attr['象意']}・{lower_attr['性質']}）\n\n"
        f"上卦は外面的・社会的な性質を、下卦は内面的・個人的な性質を表します。\n"
        f"{RELATIONSHIP_ADVICE[rel_type]}"
    )

    return DivinationResult(
        system_name="易経バースデー卦",
        system_id="ekikyo_birthday",
        summary=f"第{hexagram['number']}卦 {hexagram['name']}",
        details=details,
        interpretation=interpretation,
        warnings=warnings,
    )
