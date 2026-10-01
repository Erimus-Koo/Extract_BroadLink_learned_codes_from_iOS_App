#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Erimus"
# extract IR/RF code from Broadlink App
# put sqlite (or json) file and this python in same path, and run it.
# or with optional argument: full path to .sqlite or .json file
# result will print on console, and save as codes.txt

import base64
import binascii
import json
import os
import sqlite3
import sys

# ═══════════════════════════════════════════════


def load_data_from_sqlite(sqlite_file):
    print(f"Read SQLite File: {sqlite_file}")
    conn = sqlite3.connect(sqlite_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute("SELECT content FROM BL_SceneDevInfo_List")
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data


def load_data_from_json(json_file):
    print(f"Read Json File: {json_file}")
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def find_input_file(search_path):
    """在指定目录下查找 .sqlite 或 .json 文件，优先 sqlite。"""
    sqlite_file = None
    json_file = None
    for fn in os.listdir(search_path):
        if fn.endswith(".sqlite") and sqlite_file is None:
            sqlite_file = os.path.join(search_path, fn)
        elif fn.endswith(".json") and json_file is None:
            json_file = os.path.join(search_path, fn)
    return sqlite_file or json_file


def extract_code(input_file=None):
    script_path = os.path.abspath(os.path.dirname(__file__))

    # 确定输入文件
    if input_file and os.path.isfile(input_file):
        pass  # 直接用传入的路径
    else:
        input_file = find_input_file(script_path)
        if not input_file:
            print("请把 .sqlite 或 .json 文件放在同一目录，或作为参数传入文件路径。")
            return
        print(f"Found: {input_file}")

    # 根据文件类型读取数据
    if input_file.endswith(".sqlite"):
        data = load_data_from_sqlite(input_file)
        output_dir = os.path.dirname(input_file)
    elif input_file.endswith(".json"):
        data = load_data_from_json(input_file)
        output_dir = os.path.dirname(input_file)
    else:
        print("不支持的文件类型，请传入 .sqlite 或 .json 文件。")
        return

    print("=" * 30)

    # extract
    result = {}
    for index, d in enumerate(data):
        content = json.loads(d["content"])
        name = content.get("name", f"index_{index}")

        try:
            val = content["cmdParamList"][0]["vals"][0][0]["val"]
            b64val = base64.b64encode(binascii.unhexlify(val)).decode("utf8")
        except Exception:
            b64val = None

        extend = json.loads(content["extend"])
        try:
            did = json.loads(extend["h5Extend"])["did"]
            func = json.loads(extend["h5Extend"])["func"]
        except Exception:
            did = func = None

        did = did if did else "Others"
        func = func if func else str(index)
        result.setdefault(did, {})

        result[did][func] = {"name": name, "base64": b64val}

    result_json = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
    print(result_json)

    # write result file
    output = os.path.join(output_dir, "codes.txt")
    with open(output, "w", encoding="utf-8") as f:
        f.write(result_json)
    print(f'{"=" * 30}\nAll codes saved in "{output}".')


# ═══════════════════════════════════════════════

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    extract_code(input_file)
