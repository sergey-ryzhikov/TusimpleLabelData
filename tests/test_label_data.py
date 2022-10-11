import pytest

import json
import sys
from pathlib import Path
from copy import deepcopy


from .. import LabelData

json_ok = '{"lanes": [[-2, 1, 2], [1, 2, 3]], "h_samples": [1, 2, 3], "raw_file": "aaa/bbb/01.jpg"}'
json_ok_no_lanes = '{"lanes": [], "h_samples": [1, 2, 3], "raw_file": "aaa/bbb/01.jpg"}'
dict_ok = json.loads(json_ok)


def test_init():
    ld = LabelData(**dict_ok)


def test_from_json():
    ld = LabelData.from_json(json_ok)


def test_to_dict():
    ld = LabelData(**dict_ok).to_dict()
    assert ld == dict_ok, "wrong"


def test_to_json():
    assert LabelData(**dict_ok).to_json() == json_ok, "wrong"


def test_shift():
    ld = LabelData(lanes=[[1,2,3],[4,5,6]], h_samples=[1,2,3], raw_file='')
    ld1 = deepcopy(ld)
    ld1.shift(left=1, top=1)
    ans = ld1.to_dict()
    assert ans['lanes'] == [[0,1,2], [3,4,5]], "wrong lanes"
    assert ans['h_samples'] == [0,1,2], "wrong h_samples"

    ld2 = deepcopy(ld)
    ld2.shift(left=3, top=3)
    ans = ld2.to_dict()
    assert ans['lanes'] == [[-2,-2,0], [1,2,3]], "negative values?"
    assert ans['h_samples'] == [-2,-1,0], "wrong h_samples"

    ld2.shift(left=-1, top=-1)
    ans = ld2.to_dict()
    assert ans['lanes'] == [[-2,0,1], [2,3,4]], "wrong"  # internal representation allows negative values
    assert ans['h_samples'] == [-1,0,1], "wrong h_samples"
    

def test_resize():
    ld = LabelData(lanes=[[10,20,30],[12,12,12]], h_samples=[10,20,30], raw_file='')
    ld.resize(288, 512, 720, 1280)  # x2.5
    ans = ld.to_dict()
    assert ans['lanes'] == [[25, 50, 75], [30,30,30]], "wrong lanes"
    assert ans['h_samples'] == [25,50,75], "wrong hsamples"


