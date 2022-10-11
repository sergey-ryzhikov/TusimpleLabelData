import json
from collections import OrderedDict, namedtuple
import numpy as np

from dataclasses import dataclass, field

@dataclass
class LabelData:
    """ Parse and convert label data.
    Attributes
    ----------
    lanes : list[list]
        Array of x-coordinates of lanes.
    h_samples : list
        Array of y-coordinates of lanes (common for all lanes).
    raw_file : str
        Relative path to the image.
    """
    lanes: field(repr=False, default_factory=list)
    h_samples: field(repr=False, default_factory=list)
    raw_file: str

    #TODO: kw_only, __slots__ -- when moving to Python3.10

    def __post_init__(self):
        # Use float to allow nan values
        self.lanes = [np.array(lane, dtype=float) for lane in self.lanes]
        self.h_samples = np.array(self.h_samples, dtype=float)
        
        # Replace '-2' placeholders with np.nan (for unambiguous transformations)
        for lane in self.lanes:
            lane[lane == -2] = np.nan

    @classmethod
    def from_json(cls, json_string):
        info = json.loads(json_string)
        return cls(**{k: info.get(k) for k in cls.__dataclass_fields__})

    def to_dict(self):
        # Negative coordinates has to be replaced witn nans
        # since '-2' is used for missing values.
        lanes_copy = []
        for lane in self.lanes:
            l = lane.copy()
            l[l < 0] = np.nan
            lanes_copy.append(l)

        # But permit negative for h_samples

        return dict(
            lanes=[np.nan_to_num(lane, nan=-2).astype(int).tolist() for lane in lanes_copy],
            h_samples=self.h_samples.astype(int).tolist(),
            raw_file=self.raw_file,
        )
    
    def to_json(self): 
        # preserve keys order the same as in the original json files
        ordered = OrderedDict.fromkeys(self.__dataclass_fields__, None)
        ordered.update(self.to_dict())
        return json.dumps(ordered, sort_keys=False)

    def shift(self, left, top):
        """ Shift lane coordinates (for cropping the image).
        """
        for lane in self.lanes:
            lane -= left
        self.h_samples -= top

    def resize(self, height, width, to_height, to_width):
        """ Scale lane coordinates.
        """
        assert height > 0 and width > 0 and to_height > 0 and to_width > 0, \
                "All arguments should be positive numbers."

        height_ratio = to_height / height
        width_ratio = to_width / width

        for lane in self.lanes:
            lane *= width_ratio
        self.h_samples *= height_ratio


@dataclass
class LabelDataRelative(LabelData):
    """ Label data with relative values (in % instead of px)
    """
