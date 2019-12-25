#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# extract IR/RF code from Broadlink App
# put json file and this python in same path, and run it.

import os
import json
import base64
import binascii

# ═══════════════════════════════════════════════


def main():
    # find json file (please put only one json in same folder)
    json_file = None
    here = os.path.abspath(os.path.dirname(__file__))
    for path, dirs, files in os.walk(here):  # read all files
        for fn in files:
            if fn.endswith('.json'):
                json_file = os.path.join(path, fn)  # full path
                print(f'Found Json: {json_file}')
                break  # root only
    if not json_file:
        print('Put the json file (export from sqlite) in same path.')

    # read json file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(json.dumps(data, ensure_ascii=False, indent=4))

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
    with open(os.path.join(here, 'codes.txt'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False, indent=2))
    print('All codes saved in "codes.txt".')


# ═══════════════════════════════════════════════

if __name__ == '__main__':

    main()
