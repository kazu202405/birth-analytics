"""九星気学（きゅうせいきがく）"""
from datetime import date
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import BirthData, DivinationResult
from utils.kanshi import get_setsu_year, get_setsu_month
from utils.constants import KYUSEI


KYUSEI_ATTRIBUTES = {
    "一白水星": {"五行": "水", "方位": "北", "色": "白・黒", "性格": "柔軟・知的・適応力が高い"},
    "二黒土星": {"五行": "土", "方位": "南西", "色": "黒・黄", "性格": "堅実・忍耐・母性的"},
    "三碧木星": {"五行": "木", "方位": "東", "色": "青・碧", "性格": "活動的・若々しい・行動力"},
    "四緑木星": {"五行": "木", "方位": "南東", "色": "緑", "性格": "社交的・調和・信用"},
    "五黄土星": {"五行": "土", "方位": "中央", "色": "黄", "性格": "帝王・支配力・強運"},
    "六白金星": {"五行": "金", "方位": "北西", "色": "白・銀", "性格": "リーダー・品格・天の気"},
    "七赤金星": {"五行": "金", "方位": "西", "色": "赤・ピンク", "性格": "社交的・楽しみ・悦び"},
    "八白土星": {"五行": "土", "方位": "北東", "色": "白・茶", "性格": "変革・蓄積・山のような安定"},
    "九紫火星": {"五行": "火", "方位": "南", "色": "紫・赤", "性格": "知性・美・華やか"},
}

# 月命星テーブル: 本命星グループ × 節月
# グループ: 一四七(A), 二五八(B), 三六九(C)
GETSU_TABLE = {
    "A": [8, 7, 6, 5, 4, 3, 2, 1, 9, 8, 7, 6],  # 2月節〜1月節
    "B": [2, 1, 9, 8, 7, 6, 5, 4, 3, 2, 1, 9],
    "C": [5, 4, 3, 2, 1, 9, 8, 7, 6, 5, 4, 3],
}


def _honmeisei(year: int, month: int, day: int) -> int:
    """本命星を算出。戻り値: 1-9 (1=一白水星, ..., 9=九紫火星)"""
    y = get_setsu_year(year, month, day)
    # 各桁の合計を1桁にする
    digit_sum = sum(int(d) for d in str(y))
    while digit_sum > 9:
        digit_sum = sum(int(d) for d in str(digit_sum))
    # 11から引いて9で割った余り（0なら9）
    result = (11 - digit_sum) % 9
    return result if result != 0 else 9


def _getsu_group(honmei: int) -> str:
    """本命星のグループを返す"""
    if honmei in (1, 4, 7):
        return "A"
    elif honmei in (2, 5, 8):
        return "B"
    else:
        return "C"


def _getsumeisei(honmei: int, month: int, day: int) -> int:
    """月命星を算出"""
    setsu_m = get_setsu_month(month, day)
    group = _getsu_group(honmei)
    # setsu_m: 1-12, テーブルは2月節(index 0)〜1月節(index 11)
    table_index = (setsu_m - 2) % 12
    return GETSU_TABLE[group][table_index]


def _keisha_kyu(honmei: int, getsumei: int) -> str:
    """傾斜宮を算出（簡易版）"""
    # 傾斜宮は月命星の後天定位盤での位置
    kyusei_to_kyu = {
        1: "坎宮", 2: "坤宮", 3: "震宮", 4: "巽宮", 5: "中宮",
        6: "乾宮", 7: "兌宮", 8: "艮宮", 9: "離宮",
    }
    return kyusei_to_kyu.get(getsumei, "不明")


def calculate(birth_data: BirthData) -> DivinationResult:
    bd = birth_data.birth_date
    honmei = _honmeisei(bd.year, bd.month, bd.day)
    getsumei = _getsumeisei(honmei, bd.month, bd.day)
    keisha = _keisha_kyu(honmei, getsumei)

    honmei_name = KYUSEI[honmei - 1]
    getsumei_name = KYUSEI[getsumei - 1]
    attrs = KYUSEI_ATTRIBUTES[honmei_name]

    return DivinationResult(
        system_name="九星気学",
        system_id="kyusei_kigaku",
        summary=f"本命星: {honmei_name}",
        details={
            "honmeisei": honmei_name,
            "getsumeisei": getsumei_name,
            "keisha_kyu": keisha,
            "gogyo": attrs["五行"],
            "houi": attrs["方位"],
            "color": attrs["色"],
        },
        interpretation=f"本命星: {honmei_name} — {attrs['性格']}\n"
                       f"月命星: {getsumei_name}\n"
                       f"傾斜宮: {keisha}\n"
                       f"五行: {attrs['五行']} / 方位: {attrs['方位']} / ラッキーカラー: {attrs['色']}",
    )
