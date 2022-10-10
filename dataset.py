from pathlib import Path
from copy import deepcopy

import numpy as np
import json

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torch.utils.data import Dataset

from torchvision.io import read_image
from torchvision.transforms.functional import resize, resized_crop
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
            resize_to - images will be resized to (width, height)
            crop - keep aspect ratio by cropping images before resize
                   (from the top of from both sides equally, if needed)
        """
        self.root = Path(root)
        self.is_training = train
        self.transform = transform
        self.target_transform = target_transform

        self.img_size = resize_to
        self.img_crop = crop
        self.img_labels = self.load_items()
        self.img_interpolation_mode = interpolation_mode

    def load_items(self):
        """ Parse json files in the dataset directory
        """
        root = self.root

        raw_files_labels = {}

        json_files = list(Path(root).glob('*.json'))
        assert len(json_files) != 0, \
                f"No *.json files found in dataset directory '{root}'."
 
        for file in json_files:
            with file.open('r') as f:
                for line_no, line in enumerate(f):
                    label = json.loads(line)
                    assert label['raw_file'], "Item with empty 'raw_file' attribute: " \
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
    
    @classmethod
    def find_crop(cls, w, h, new_w, new_h):
        pass

        return top, left, height, width

    def __getitem__(self, idx):

        # Avoid shared memory copy-on-update issues by using deepcopy
        # https://github.com/pytorch/pytorch/issues/13246#issuecomment-905703662

        lanes = deepcopy(self.img_labels[idx]['lanes'])
        h_samples = deepcopy(self.img_labels[idx]['h_samples'])
        raw_file = deepcopy(self.img_labels[idx]['raw_file'])

        img_path = str(self.root / raw_file)
        image = read_image(img_path)
        label = dict(
            lanes = [np.array(lane, dtype=float) for lane in lanes],  # float to allow nan values
            h_samples = np.array(h_samples, dtype=float),
            )
        
        # Replace '-2' placeholders with np.nan (for unambiguous transformations)
        for lane in label['lanes']:
            lane[lane == -2] = np.nan  

        # TODO: Resize image and labels
        c, h, w = image.shape
        new_h, new_w = self.img_size

        if (h, w) != (new_h, new_w):
            if not self.img_crop:
                image = resize(image, self.img_size, self.img_interpolation_mode)
        

        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)

        return image, label
