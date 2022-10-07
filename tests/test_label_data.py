#!/usr/bin/env python3

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from label_data import LabelData

json_ok = '{"lanes": [[-2, 1, 2], [1, 2, 3]], "h_samples": [1, 2, 3], "raw_file": "aaa/bbb/01.jpg"}'
json_ok_empty_lanes = '{"lanes": [], "h_samples": [1, 2, 3], "raw_file": "aaa/bbb/01.jpg"}'

def test_parsing():
    LabelData.from_json(json_ok)
    LabelData.from_json(json_ok_empty_lanes)

def test_rerp():
    json_ok_repr = "LabelData(raw_file='aaa/bbb/01.jpg')"
    repr = str(LabelData.from_json(json_ok))
    assert repr == json_ok_repr, f"wrong __repr__: {repr}"

def test_dict():
    n = len(LabelData.from_json(json_ok)['lanes'])
    assert n != 0, "wrong len(x['lanes'])"

def test_del():
    item = LabelData.from_json(json_ok)
    del item['lanes']

def test_rel():
    LabelData.from_json(json_ok).to_relative(100,100)

if __name__ == "__main__":
    test_parsing()
    test_rerp()
    test_dict()
    test_del()
    test_rel()