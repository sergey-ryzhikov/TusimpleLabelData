#!/usr/bin/env python3
# import pytest

import json
import sys
import torch

from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from TusimpleUtils import TusimpleDataset

sample_root = (Path(__file__).parent / '../tusimple_sample_512x288/').resolve()

def test_init():
    assert len(TusimpleDataset(sample_root)) == 10, "10 items expected"


def test_test():
    img, label = TusimpleDataset(sample_root)[0]


def test_resize():
    img0, label0 = TusimpleDataset(sample_root, resize_to=(144,256), crop=False)[0]
    assert img0.shape == (3, 144, 256), f"Wrong shape 0: {img0.shape}"

    img1, label1 = TusimpleDataset(sample_root, resize_to=(288,512), crop=False)[0]
    assert img1.shape == (3, 288, 512), f"Wrong shape 1: {img1.shape}"

    img2, label2 = TusimpleDataset(sample_root, resize_to=(256,512), crop=True)[0]
    assert img2.shape == (3, 256, 512), f"Wrong shape 2: {img2.shape}"
    assert torch.all(img1[:,32] == img2[:,0]), f"32nd row should become the first after crop"

    img3, label3 = TusimpleDataset(sample_root, resize_to=(288,100), crop=True)[0]
    assert img3.shape == (3, 288, 100), f"Wrong shape 3: {img3.shape}"


def run_tests():
    from inspect import isfunction
    
    # execute all local functions which name is beginning with "test_"
    test_functions = [val for name,val in globals().items()
                         if isfunction(val) and name.startswith('test_')]
    for func in test_functions:
        func()

if __name__ == "__main__":
    run_tests()