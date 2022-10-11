import numpy as np
import json

from pathlib import Path
from copy import deepcopy
from functools import lru_cache

import torch.nn.functional as F
from torch.autograd import Variable
from torch.utils.data import Dataset

from torchvision.io import read_image
from torchvision.transforms.functional import resize, resized_crop, crop
from torchvision.transforms import InterpolationMode

from .label_data import LabelData

class TusimpleDataset(Dataset):
    """ Dataset with road lanes.
        Returns image and a list of lane coordinates.
    """
    def __init__(self, root, train=True, # download=False,
                        transform=None, target_transform=None,
                        resize_to=(256, 512), crop=True,
                        interpolation_mode=InterpolationMode.BICUBIC):
        """ 
            resize_to - images will be resized to (height, width)
            crop - keep aspect ratio by cropping images before resize
                   (from the top of from both sides equally, if needed)
        """
        self.root = Path(root)
        self.is_training = train
        self.transform = transform
        self.target_transform = target_transform
        self.resize_to = resize_to
        self.crop = crop
        self.interpolation_mode = interpolation_mode

        self.img_labels = self._load_items(root)

    def _load_items(self, root):
        """ Parse json files in the dataset directory
        """
        raw_files_labels = {}

        json_files = list(Path(root).glob('*.json'))
        assert len(json_files) != 0, \
                f"No *.json files found in dataset directory '{root}'."
 
        for file in json_files:
            with file.open('r') as f:
                for line_no, line in enumerate(f):
                    label = json.loads(line)
                    assert label['raw_file'], \
                            "Item with empty 'raw_file' attribute: " \
                                    f"{file}:{line_no}"
                    if self.is_training:
                        if len(label['lanes']) == 0:  # skip if 'lanes' is empty
                            continue

                    raw_file = label['raw_file']
                    raw_files_labels[raw_file] = label

        labels = dict(sorted(raw_files_labels.items())).values()
        return list(labels)

    def __len__(self):  
        return len(self.img_labels)

    @lru_cache(maxsize=100)
    def get_crop_params(self, h, w):
        """ Find optimal crop to keep aspect ratio.
        """
        new_h, new_w = self.resize_to
        new_ratio = new_h / new_w
        ideal_h = round(new_ratio * w)

        if ideal_h == h:
            top, left, height, width = 0, 0, h, w
        elif ideal_h < h: 
            # Crop top
            top, left, height, width = (h - ideal_h), 0, ideal_h, w
        else: 
            # Crop sides equally
            ideal_w = round(h / new_ratio)
            top, left, height, width = 0, (w - ideal_w) >> 1, h, ideal_w

        return top, left, height, width

    def __getitem__(self, idx):

        # Avoid shared memory copy-on-update issues by using deepcopy
        # https://github.com/pytorch/pytorch/issues/13246#issuecomment-905703662

        lanes = deepcopy(self.img_labels[idx]['lanes'])
        h_samples = deepcopy(self.img_labels[idx]['h_samples'])
        raw_file = deepcopy(self.img_labels[idx]['raw_file'])

        img_path = str(self.root / raw_file)
        image = read_image(img_path)

        label = LabelData(lanes=lanes, h_samples=h_samples, raw_file=raw_file)
        
        c, h, w = image.shape

        if self.resize_to != (h, w):
            if not self.crop:
                image = resize(image, self.resize_to, self.interpolation_mode)
            else:  # keep aspect ratio, but crop the top or the sides
                top, left, crop_h, crop_w = self.get_crop_params(h, w)
                image = resized_crop(image, top, left, crop_h, crop_w,
                                      self.resize_to, self.interpolation_mode)
                label.shift(top, left)
            label.resize(h, w, *self.resize_to)

        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)

        return image, label
