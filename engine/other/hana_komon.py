"""花個紋（簡易版） — 誕生日に対応する花と家紋を算出"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult


# 月ごとの代表花と個紋
MONTH_FLOWERS = {
    1: {"flower": "水仙", "komon": "雪輪水仙", "keyword": "神秘・自己愛・新たな始まり",
        "season": "冬", "color": "白・黄"},
    2: {"flower": "梅", "komon": "梅鉢", "keyword": "気品・忍耐・春への希望",
        "season": "早春", "color": "紅・白"},
    3: {"flower": "桜", "komon": "桜花", "keyword": "純潔・美・精神の美しさ",
        "season": "春", "color": "淡紅"},
    4: {"flower": "チューリップ", "komon": "鬱金香", "keyword": "博愛・思いやり・魅力",
        "season": "春", "color": "赤・黄・白"},
    5: {"flower": "藤", "komon": "下り藤", "keyword": "優しさ・歓迎・佳き縁",
        "season": "晩春", "color": "紫・白"},
    6: {"flower": "紫陽花", "komon": "紫陽花", "keyword": "移り気・辛抱強さ・家族",
        "season": "梅雨", "color": "青・紫・桃"},
    7: {"flower": "百合", "komon": "百合", "keyword": "純粋・無垢・威厳",
        "season": "盛夏", "color": "白・橙"},
    8: {"flower": "向日葵", "komon": "向日葵", "keyword": "憧れ・情熱・太陽のような明るさ",
        "season": "夏", "color": "黄"},
    9: {"flower": "秋桜", "komon": "秋桜", "keyword": "調和・謙虚・乙女の真心",
        "season": "初秋", "color": "桃・白"},
    10: {"flower": "菊", "komon": "菊花", "keyword": "高貴・長寿・真実",
         "season": "秋", "color": "黄・白・紫"},
    11: {"flower": "山茶花", "komon": "山茶花", "keyword": "困難に打ち勝つ・ひたむきさ",
         "season": "晩秋", "color": "紅・桃・白"},
    12: {"flower": "椿", "komon": "椿", "keyword": "控えめな優しさ・誇り・完璧な美",
         "season": "冬", "color": "紅・白"},
}

# 日ごとの副花（31日分）
DAY_FLOWERS = [
    {"flower": "松", "keyword": "長寿・不変", "element": "木"},
    {"flower": "竹", "keyword": "節操・成長", "element": "木"},
    {"flower": "蘭", "keyword": "優雅・気品", "element": "水"},
    {"flower": "菊", "keyword": "高潔・真実", "element": "土"},
    {"flower": "牡丹", "keyword": "富貴・王者", "element": "火"},
    {"flower": "撫子", "keyword": "純愛・可憐", "element": "水"},
    {"flower": "萩", "keyword": "柔軟・思案", "element": "木"},
    {"flower": "桔梗", "keyword": "誠実・変わらぬ愛", "element": "水"},
    {"flower": "鈴蘭", "keyword": "幸福の再来", "element": "水"},
    {"flower": "薔薇", "keyword": "愛・美・情熱", "element": "火"},
    {"flower": "蓮", "keyword": "清浄・悟り", "element": "水"},
    {"flower": "楓", "keyword": "美しい変化", "element": "木"},
    {"flower": "柊", "keyword": "先見の明・用心", "element": "木"},
    {"flower": "南天", "keyword": "難を転ずる", "element": "火"},
    {"flower": "万両", "keyword": "財運・繁栄", "element": "土"},
    {"flower": "千両", "keyword": "富・裕福", "element": "土"},
    {"flower": "福寿草", "keyword": "幸福・長寿", "element": "土"},
    {"flower": "雪柳", "keyword": "殊勝・愛嬌", "element": "水"},
    {"flower": "沈丁花", "keyword": "栄光・不滅", "element": "水"},
    {"flower": "木蓮", "keyword": "崇高・持続力", "element": "木"},
    {"flower": "藤", "keyword": "優しさ・歓迎", "element": "木"},
    {"flower": "山吹", "keyword": "気品・金運", "element": "土"},
    {"flower": "杜若", "keyword": "幸運の使者", "element": "水"},
    {"flower": "菖蒲", "keyword": "勝負・勇気", "element": "水"},
    {"flower": "紫苑", "keyword": "追憶・君を忘れない", "element": "水"},
    {"flower": "芙蓉", "keyword": "繊細な美", "element": "水"},
    {"flower": "桃", "keyword": "長寿・魔除け", "element": "木"},
    {"flower": "柿", "keyword": "自然の恵み", "element": "土"},
    {"flower": "栗", "keyword": "豊穣・忍耐", "element": "土"},
    {"flower": "柚子", "keyword": "健康・浄化", "element": "木"},
    {"flower": "林檎", "keyword": "誘惑・知恵", "element": "木"},
]

# 月+日の組み合わせで個紋スタイルを決定
KOMON_STYLES = [
    "丸に", "三つ", "花菱", "抱き", "結び", "重ね", "五つ", "捻じ",
    "枝", "葉", "蕾", "実",
]

# 五行相生の関係性
ELEMENT_HARMONY = {
    ("木", "火"): "木は火を生む — 創造力が燃え上がる",
    ("火", "土"): "火は土を生む — 情熱が実りをもたらす",
    ("土", "木"): "土は木を育む — 安定が成長を支える",
    ("水", "木"): "水は木を養う — 感性が成長を促す",
    ("水", "水"): "水と水の調和 — 深い感受性の共鳴",
    ("木", "木"): "木と木の調和 — 伸びやかな成長の力",
    ("火", "火"): "火と火の調和 — 燃え盛る情熱",
    ("土", "土"): "土と土の調和 — 揺るぎない安定",
}


def _get_element_message(month_el: str, day_el: str) -> str:
    """月花と日花の五行の関係性メッセージを返す"""
    key = (month_el, day_el)
    if key in ELEMENT_HARMONY:
        return ELEMENT_HARMONY[key]
    rev_key = (day_el, month_el)
    if rev_key in ELEMENT_HARMONY:
        return ELEMENT_HARMONY[rev_key]
    return f"{month_el}と{day_el}の組み合わせ — 異なるエネルギーが互いを補い合う"


def _get_month_element(month: int) -> str:
    """月の花から五行を簡易推定"""
    season_to_element = {
        "冬": "水", "早春": "木", "春": "木", "晩春": "木",
        "梅雨": "水", "盛夏": "火", "夏": "火",
        "初秋": "土", "秋": "土", "晩秋": "土",
    }
    season = MONTH_FLOWERS[month]["season"]
    return season_to_element.get(season, "土")


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date
    month = bd.month
    day = bd.day

    month_data = MONTH_FLOWERS[month]
    day_index = (day - 1) % len(DAY_FLOWERS)
    day_data = DAY_FLOWERS[day_index]

    # 個紋スタイル（月+日で決定）
    style_index = (month + day) % len(KOMON_STYLES)
    komon_style = KOMON_STYLES[style_index]
    personal_komon = f"{komon_style}{month_data['flower']}に{day_data['flower']}"

    # 五行の相性
    month_element = _get_month_element(month)
    day_element = day_data["element"]
    harmony_msg = _get_element_message(month_element, day_element)

    details = {
        "month_flower": {
            "flower": month_data["flower"],
            "komon": month_data["komon"],
            "keyword": month_data["keyword"],
            "season": month_data["season"],
            "color": month_data["color"],
        },
        "day_flower": {
            "flower": day_data["flower"],
            "keyword": day_data["keyword"],
            "element": day_data["element"],
            "day_index": day_index + 1,
        },
        "personal_komon": personal_komon,
        "element_harmony": harmony_msg,
        "birth_month": month,
        "birth_day": day,
    }

    interpretation = (
        f"【月の花】{month_data['flower']}（{month_data['komon']}）\n"
        f"  花言葉: {month_data['keyword']}\n"
        f"  季節: {month_data['season']} / 色: {month_data['color']}\n\n"
        f"【日の花】{day_data['flower']}\n"
        f"  花言葉: {day_data['keyword']}\n"
        f"  五行: {day_data['element']}\n\n"
        f"【あなたの花個紋】{personal_komon}\n"
        f"  {month}月{day}日生まれのあなただけの紋様です。\n\n"
        f"【五行の調和】\n"
        f"  {harmony_msg}\n\n"
        f"花個紋は、あなたの誕生日に宿る花のエネルギーを家紋のように象徴化したものです。\n"
        f"月の花が全体的な性質を、日の花が個人的な才能や使命を表しています。"
    )

    return DivinationResult(
        system_name="花個紋",
        system_id="hana_komon",
        summary=f"{month_data['flower']}と{day_data['flower']}の紋 — {personal_komon}",
        details=details,
        interpretation=interpretation,
    )
