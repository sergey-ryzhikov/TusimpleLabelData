#!/usr/bin/env python3
# import pytest

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from label_data import LabelData

dict_ok = dict(lanes=[[-2, 1, 2], [1, 2, 3]], h_samples=[1, 2, 3], raw_file="aaa/bbb/01.jpg")
json_ok = '{"lanes": [[-2, 1, 2], [1, 2, 3]], "h_samples": [1, 2, 3], "raw_file": "aaa/bbb/01.jpg"}'
json_ok_no_lanes = '{"lanes": [], "h_samples": [1, 2, 3], "raw_file": "aaa/bbb/01.jpg"}'

def test_from_json():
    LabelData.from_json(json_ok)
    LabelData.from_json(json_ok_no_lanes)

def test_to_json():
    res = LabelData(**dict_ok).to_json()
    assert res == json_ok, f"wrong {res}"

def test_rerp():
    json_ok_repr = "LabelData(raw_file='aaa/bbb/01.jpg')"
    repr = str(LabelData(**dict_ok))
    assert repr == json_ok_repr, f"wrong __repr__: {repr}"

def test_len():
    n = len(LabelData(**dict_ok)['lanes'])
    assert n != 0, "wrong len(x['lanes'])"

def test_del():
    item = LabelData(**dict_ok)
    del item['lanes']

def test_crop_px():
    test1 = '{"lanes": [[-2, 3, 2, 1], [3, 4, 5, -2]], "h_samples": [1, 2, 3, 4]}'
    assert LabelData.from_json(test1).crop(top=2) == \
        '{"lanes": [[3, 2, 1], [4, 5, -2]], "h_samples": [1, 2, 3]}'

def test_rel():
    item = LabelData.from_json('{"lanes": [[-2, 51]], "h_samples": [1]}')
    item_rel = item.get_relative(100,100)
    assert item == item_rel.to_absolute(100,100), "wrong"
    assert item != item_rel.to_absolute(99,100), "wrong 99"
    assert item != item_rel.to_absolute(101,100), "wrong 101"
    pass


if __name__ == "__main__":
    from inspect import isfunction
    
    # execute all local functions which name is beginning with "test_"
    test_functions = [val for name,val in locals().items()
                         if isfunction(val) and name.startswith('test_')]
    
    for func in test_functions:
        func()