import json


class LabelData(dict):
    """ Parse and convert label data.
    """
    __slots__ = 'lanes', 'h_samples', 'raw_file', 'relative'

    def __init__(self, lanes=[], h_samples=[], raw_file='', relative=False):
        kwargs = dict(lanes=lanes,
                      h_samples=h_samples,
                      raw_file=raw_file,
                      )
        if relative:
            kwargs['relative'] = relative
            
        super().__init__(**kwargs)
        # self.__dict__ = self
   
    @classmethod
    def from_json(cls, json_string):
      info = json.loads(json_string)
      return cls(**{k: info[k] if k in info else None for k in cls.__slots__})

    def __repr__(self):
      return f"LabelData(raw_file='{self['raw_file']}')"

    def to_json(self): 
      attrs = self.__slots__
      if self['relative'] != True:
        attrs = [x for x in attrs if x != 'relative']
      return json.dumps({k: getattr(self, k, None) for k in attrs})

    def to_relative(self, dim_lanes, dim_h_samples, round_=2):
      """ Convert absolute coordinates to the relative ones. 
      """
      assert self['relative'] != True, "Coordinates are relative already."
      assert dim_lanes >= self.max_lanes, "The 'dim_lanes' is less than the current maximum."
      assert dim_h_samples >= self.max_h_samples, "The 'dim_h_samples' is less than the current maximum."
      
      return self.__class__(
          h_samples=[round(x / dim_h_samples * 100, round_) for x in self['h_samples']],
          lanes=[[round(x / dim_lanes * 100, round_) if x > 0 else x
                          for x in lane]
                          for lane in self['lanes']],
          raw_file=self['raw_file'],
          relative=True
        )

    def to_absolute(self, dim_lanes, dim_h_samples):
      """ Convert relative coordinates to absolute ones. """
      assert self['relative'] == True, "Coordinates are absolute."
      assert self.max_lanes <= 100, f"Relative value for max_lanes is invalid:{self.max_lanes}"
      assert self.max_h_samples <= 100, f"Relative value for h_samples is invalid:{self.max_h_samples}"

      return self.__class__(
          h_samples=[round(x / 100 * dim_h_samples) for x in self['h_samples']],
          lanes=[[round(x / 100 * dim_lanes) if x > 0 else x
                          for x in lane]
                          for lane in self['lanes']],
          raw_file=self['raw_file'],
          relative=None
        )

    @property
    def max_lanes(self):
      if self['lanes']:
        return max(next((x for x in reversed(lane) if x > 0), 0)  # last from the end != -2
                        for lane in self['lanes'])
      else:
        return 0

    @property
    def max_h_samples(self):
      if self.h_samples:
        return self['h_samples'][-1]  # return the last one
      else:
        return 0