#!/usr/bin/env python3
"""誕生日総合占術エンジン — CLI エントリーポイント"""
import argparse
import json
import sys
import os
import io
from datetime import date, time, datetime

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add engine directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import BirthData, DivinationResult


def _import_module(category: str, module_name: str):
    """占術モジュールを動的にインポート"""
    try:
        mod = __import__(f"{category}.{module_name}", fromlist=[module_name])
        return mod
    except ImportError:
        return None
    except Exception as e:
        return None


# 登録された占術モジュール (category, module_name)
DIVINATION_MODULES = [
    # 東洋系
    ("eastern", "inyo_gogyo"),
    ("eastern", "kyusei_kigaku"),
    ("eastern", "rokusei"),
    ("eastern", "zero_gaku"),
    ("eastern", "fusui_meika"),
    ("eastern", "ekikyo_birthday"),
    ("eastern", "shichuu_suimei"),
    ("eastern", "sanmei_gaku"),
    ("eastern", "shukuyou"),
    ("eastern", "junichoku"),
    # 西洋系
    ("western", "numerology"),
    # マヤ系
    ("maya", "maya_calendar"),
    ("maya", "mayan_oracle"),
    # 動物・キャラクター系
    ("animal", "doubutsu_uranai"),
    ("animal", "kosei_shinrigaku"),
    # 古代文明系
    ("ancient", "egyptian"),
    ("ancient", "celtic_tree"),
    ("ancient", "aztec"),
    ("ancient", "arabian"),
    # シンボル系
    ("symbol", "tarot_birthday"),
    ("symbol", "rune_birthday"),
    ("symbol", "guardian_angel"),
    # エネルギー系
    ("energy", "biorhythm"),
    ("energy", "aura_soma"),
    ("energy", "chakra"),
    ("energy", "birthday_color"),
    ("energy", "numerology_vibration"),
    # その他
    ("other", "youbi_uranai"),
    ("other", "birthday_number"),
    ("other", "hana_komon"),
]


def run_all(birth_data: BirthData) -> dict:
    """全占術を実行して結果を返す"""
    results = {}
    warnings = []

    for category, module_name in DIVINATION_MODULES:
        mod = _import_module(category, module_name)
        if mod is None:
            continue
        try:
            result = mod.calculate(birth_data)
            if category not in results:
                results[category] = {}
            results[category][result.system_id] = result.to_dict()
        except Exception as e:
            warnings.append(f"{module_name}: {str(e)}")

    return {
        "input": {
            "birth_date": birth_data.birth_date.isoformat(),
            "birth_time": birth_data.birth_time.isoformat() if birth_data.birth_time else None,
            "birth_place": birth_data.birth_place,
            "name": birth_data.name,
            "gender": birth_data.gender,
        },
        "results": results,
        "meta": {
            "calculated_at": datetime.now().isoformat(),
            "engine_version": "1.0.0",
            "total_systems": sum(len(v) for v in results.values()),
            "warnings": warnings,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="誕生日総合占術エンジン")
    parser.add_argument("--date", required=True, help="生年月日 (YYYY-MM-DD)")
    parser.add_argument("--time", default=None, help="出生時刻 (HH:MM)")
    parser.add_argument("--place", default=None, help="出生地")
    parser.add_argument("--name", default=None, help="氏名")
    parser.add_argument("--gender", default=None, choices=["M", "F"], help="性別")

    args = parser.parse_args()

    try:
        birth_date = date.fromisoformat(args.date)
    except ValueError:
        print(json.dumps({"error": f"Invalid date format: {args.date}. Use YYYY-MM-DD"}, ensure_ascii=False))
        sys.exit(1)

    birth_time = None
    if args.time:
        try:
            birth_time = time.fromisoformat(args.time)
        except ValueError:
            print(json.dumps({"error": f"Invalid time format: {args.time}. Use HH:MM"}, ensure_ascii=False))
            sys.exit(1)

    birth_data = BirthData(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_place=args.place,
        name=args.name,
        gender=args.gender,
    )

    result = run_all(birth_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
