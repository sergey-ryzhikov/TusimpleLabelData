
# How to shrink the dataset (11 GB → ~170 MB)

<!-- markdownlint-disable no-trailing-punctuation -->
## Steps:  

### 1. Download the TUSimple dataset

``` bash
wget -q --show-progress -- "https://s3.us-east-2.amazonaws.com/benchmark-frontend/datasets/1/train_set.zip" 
```

### 2. Extract only files with groud truth

.json files with labels contain ground truth about lanes coordinates only for the last file in each sequence of 20 frames (20.jpg). If we need only files with ground truth, we can extract only them:

``` bash
 !time 7z x -aos -bso0 ./data/train_set.zip -o./tusimple/ "clips/*/*/20.jpg" "*.json" 
```

Or just extract all of them and delete all images except \*/20.jpg:

``` bash
find tusimple/ -name "*.jpg" -not -name "20.jpg" -delete   # keep only 20.jpg
```

### 3. Resize the files

To save some CPU, we can preliminary compress the files from 1280x720 to 512x288.

First, install the Image Magic toolset:

``` bash
# install ImageMagic tools
!(sudo apt -y update && apt -y install pv imagemagick)&> /dev/null && echo done || echo error
```

Then resize the files:

``` bash
find tusimple/clips/ -name "*.jpg" -print0 | pv -0 | xargs -0 -P 8 -n 10 mogrify -size 512x288 -resize 512x288! # +profile "*"

# -size gives a hint to the JPEG decoder that the images are going to be downscaled,
# allowing it to run faster by avoiding returning full-resolution images to ImageMagick
# for the subsequent operation.

#  +profile "*" - remove any ICM, EXIF, IPTC, or other profiles that might be present in the input (uncomment if needed)
```

### 4. Adjust the lane coordinates in .json-files

```python
from TusimpleUtils import LabelData

json_files = list(Path('./tusimple/').glob('*.json'))

DIM_FROM = 720, 1280
DIM_TO = 288, 512

for file in json_files:
  stem = file.with_suffix("")  # path/file.json -> path/file
  new_file = str(stem) + f"_{DIM_TO[1]}x{DIM_TO[0]}.json"

  with Path(file).open() as input, Path(out_file).open() as output:
    for line in input:
      ld = LabelData.from_json(line)
      ld.resize(*DIM_FROM, *DIM_TO)
      res = ld.to_json()
      print(res, file=output)
```

If everything is ok, replace the old files with adjusted ones:

``` bash
cd tusimple; rename -v --force 's/_512x288.json/.json/' *.json
```

### 5. Put all what you get in a new .zip archive

``` bash
find tusimple -type f | sort -V | xargs zip train_set_512x288_gt.zip  

# zip -0 to add files without compression
```
