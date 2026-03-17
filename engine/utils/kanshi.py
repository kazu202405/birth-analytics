"""干支計算ユーティリティ（六十干支）"""
from datetime import date
from .constants import JIKKAN, JUNISHI, ROKUJU_KANSHI, KAN_TO_GOGYO, KAN_TO_INYO

# 節入り日（各月の節気の開始日）- 簡易版
# 正確には年によって1-2日ずれるが、多くの場合この日付で正しい
SETSU_DAYS = {
    1: 6,   # 小寒 (1/5-6)
    2: 4,   # 立春 (2/3-4) ★年の始まり
    3: 6,   # 啓蟄 (3/5-6)
    4: 5,   # 清明 (4/4-5)
    5: 6,   # 立夏 (5/5-6)
    6: 6,   # 芒種 (6/5-6)
    7: 7,   # 小暑 (7/7-8)
    8: 8,   # 立秋 (8/7-8)
    9: 8,   # 白露 (9/7-8)
    10: 8,  # 寒露 (10/8-9)
    11: 7,  # 立冬 (11/7-8)
    12: 7,  # 大雪 (12/7-8)
}


def get_setsu_month(month: int, day: int) -> int:
    """節入り日を考慮した月を返す（節月）。
    節入り日前なら前月扱い。"""
    setsu_day = SETSU_DAYS.get(month, 6)
    if day < setsu_day:
        return month - 1 if month > 1 else 12
    return month


def get_setsu_year(year: int, month: int, day: int) -> int:
    """節入り日を考慮した年を返す。
    立春（2月の節入り）前なら前年扱い。"""
    if month < 2 or (month == 2 and day < SETSU_DAYS[2]):
        return year - 1
    return year


def get_year_kanshi(year: int, month: int, day: int) -> tuple[str, str]:
    """年干支を返す（節入り日考慮）。戻り値: (天干, 地支)"""
    y = get_setsu_year(year, month, day)
    kan_index = (y - 4) % 10
    shi_index = (y - 4) % 12
    return JIKKAN[kan_index], JUNISHI[shi_index]


def get_month_kanshi(year: int, month: int, day: int, year_kan: str) -> tuple[str, str]:
    """月干支を返す（節入り日で月を判定）。"""
    setsu_month = get_setsu_month(month, day)
    # 月支: 寅月(1月/旧暦)=2月節から始まる
    shi_index = (setsu_month + 1) % 12  # 1月→寅(2), 2月→卯(3), ...
    # 月干: 年干から算出（甲己→丙寅始まり、乙庚→戊寅始まり、...）
    year_kan_index = JIKKAN.index(year_kan)
    base_kan = (year_kan_index % 5) * 2 + 2
    kan_index = (base_kan + setsu_month - 1) % 10
    return JIKKAN[kan_index], JUNISHI[shi_index]


def get_day_kanshi(year: int, month: int, day: int) -> tuple[str, str]:
    """日干支を返す（基準日からの経過日数で算出）。"""
    # 基準日: 1900年1月1日 = 甲子(index 0)... 実際は庚子
    # 1900-01-01のJulian Day Number = 2415021
    # 1900-01-01 の干支は「庚子」= index 36
    base_date = date(1900, 1, 1)
    target_date = date(year, month, day)
    diff_days = (target_date - base_date).days
    kanshi_index = (diff_days + 36) % 60  # 36 = 庚子のindex
    kan_index = kanshi_index % 10
    shi_index = kanshi_index % 12
    return JIKKAN[kan_index], JUNISHI[shi_index]


def get_hour_kanshi(hour: int, day_kan: str) -> tuple[str, str]:
    """時干支を返す。hour: 0-23。"""
    # 時支: 23-1→子, 1-3→丑, ... (2時間ごと)
    shi_index = ((hour + 1) // 2) % 12
    # 時干: 日干から算出
    day_kan_index = JIKKAN.index(day_kan)
    base_kan = (day_kan_index % 5) * 2
    kan_index = (base_kan + shi_index) % 10
    return JIKKAN[kan_index], JUNISHI[shi_index]


def kanshi_to_gogyo(kan: str) -> str:
    """天干から五行を返す"""
    return KAN_TO_GOGYO[kan]


def kanshi_to_inyo(kan: str) -> str:
    """天干から陰陽を返す"""
    return KAN_TO_INYO[kan]


def get_kanshi_index(kan: str, shi: str) -> int:
    """天干と地支から六十干支のインデックス(0-59)を返す"""
    kan_i = JIKKAN.index(kan)
    shi_i = JUNISHI.index(shi)
    # 干と支の偶奇が一致する組み合わせのみ有効
    for i in range(60):
        if i % 10 == kan_i and i % 12 == shi_i:
            return i
    raise ValueError(f"Invalid kanshi combination: {kan}{shi}")


def get_kuubou(day_kan: str, day_shi: str) -> tuple[str, str]:
    """空亡（天中殺）を返す。日柱の干支から算出。"""
    idx = get_kanshi_index(day_kan, day_shi)
    group_start = (idx // 10) * 10
    # 空亡は、そのグループ(10干支)に含まれない2つの地支
    used_shi = set()
    for i in range(group_start, group_start + 10):
        used_shi.add(JUNISHI[i % 12])
    empty = [s for s in JUNISHI if s not in used_shi]
    return tuple(empty)
