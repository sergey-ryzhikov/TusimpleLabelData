# Tusimple Utils

Some utility functions for [TUSimple dataset](https://github.com/TuSimple/tusimple-benchmark).


## Usage example

``` python
# Convert json_data to relative coordinates

from TusimpleUtils import LabelData

DIM = 1280, 720

json_files = list(Path('./tusimple/').glob('*.json'))

for file in json_files:
  stem = file.with_suffix("")  # path/file.json -> path/file
  out_file = str(stem) + "relative.json"

  with Path(file).open() as input, Path(out_file).open() as output:
    for line in input:
      ld = LabelData.from_json(line)
      res = ld.to_relative(*DIM).to_json()
      print(res, file=output)

```

## How To

* [How to shrink the dataset (11 GB → ~170 MB)](ShrinkTheDataset.md)