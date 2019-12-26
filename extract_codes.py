#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# extract IR/RF code from Broadlink App
# put json file and this python in same path, and run it.
# or with optional argument {json file full path}
# result will print on console, and save as codes.txt

import os
import sys
import json
import base64
import binascii

# ═══════════════════════════════════════════════


def extract_code(json_file=None):
    # check json file
    if json_file is None or not json_file.endswith('.json'):
        # find json file in same path (please put only one json in same folder)
        json_path = os.path.abspath(os.path.dirname(__file__))
        for path, dirs, files in os.walk(json_path):  # read all files
            for fn in files:
                if fn.endswith('.json'):
                    json_file = os.path.join(path, fn)  # full path
                    print(f'Found Json: {json_file}')
                    break
            break  # root only
        if not json_file:
            print('Put the json file (export from sqlite) in same path.'
                  'Or input file full path as argument.')
            return
    else:  # json file from argument
        json_path = os.path.abspath(os.path.dirname(json_file))

    # read json file
    print(f'Read Json File: {json_file}\n{"="*30}')
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # print(json.dumps(data, ensure_ascii=False, indent=4))

    # extract
    result = {}
    for index, d in enumerate(data):
        content = json.loads(d['content'])
        # print(json.dumps(content, ensure_ascii=False, indent=4))
        name = content.get(f'name', f'index_{index}')

        try:
            val = content['cmdParamList'][0]['vals'][0][0]['val']
        except Exception:
            val = None

        extend = json.loads(content['extend'])
        # print(json.dumps(extend, ensure_ascii=False, indent=4))
        try:
            did = json.loads(extend['h5Extend'])['did']
            func = json.loads(extend['h5Extend'])['func']
        except Exception:
            did = func = None

        if did and func:
            key = f'{did}_{func}'
        else:
            key = str(index)

        b64val = base64.b64encode(binascii.unhexlify(val)).decode('utf8')

        result[key] = {'name': name, 'func': func, 'base64': b64val}

    print(json.dumps(result, ensure_ascii=False, indent=4))

    # write result file
    output = os.path.join(json_path, 'codes.txt')
    with open(output, 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False, indent=2))
    print(f'{"="*30}\nAll codes saved in "{output}".')


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    json_file = sys.argv[1] if len(sys.argv) > 1 else None
    extract_code(json_file)
