#!/usr/bin/env python3
# import pytest

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from label_data import LabelData

json_ok = '{"lanes": [[-2, 1, 2], [1, 2, 3]], "h_samples": [1, 2, 3], "raw_file": "aaa/bbb/01.jpg"}'
json_ok_no_lanes = '{"lanes": [], "h_samples": [1, 2, 3], "raw_file": "aaa/bbb/01.jpg"}'

dict_ok = json.loads(json_ok)


def test_from_json():
    assert LabelData(**dict_ok) == LabelData.from_json(json_ok), "wrong"
    LabelData.from_json(json_ok_no_lanes)

def test_to_json():
    res = LabelData(**dict_ok).to_json()
    assert res == json_ok, f"wrong"

def test_rerp():
    json_ok_repr = "LabelData(raw_file='aaa/bbb/01.jpg')"
    repr = LabelData(**dict_ok).__repr__()
    assert repr == json_ok_repr, f"wrong __repr__: {repr}"

def test_str():
    json_ = LabelData(**dict_ok).to_json()
    str_ =  str(LabelData(**dict_ok))
    assert str_ == json_, f"wrong __str__: {str_}"

def test_len():
    n = len(LabelData(**dict_ok)['lanes'])
    assert n != 0, "wrong len(x['lanes'])"

def test_del():
    item = LabelData(**dict_ok)
    del item['lanes']

def test_rel():
    item = LabelData(**{'lanes': [[-2, 51]], 'h_samples': [1]})
    item_rel = item.to_relative(100, 100)

    assert item == item_rel.to_absolute(100, 100), "wrong 100"
    assert item != item_rel.to_absolute(99, 100), f"wrong 99"
    assert item != item_rel.to_absolute(101, 100), f"wrong 101"


def run_tests():
    from inspect import isfunction
    
    # execute all local functions which name is beginning with "test_"
    test_functions = [val for name,val in globals().items()
                         if isfunction(val) and name.startswith('test_')]
    for func in test_functions:
        func()

if __name__ == "__main__":
    run_tests()
