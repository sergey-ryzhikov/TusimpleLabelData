
# How to shrink the dataset (11 GB → ~170 MB)

### 1. Download the TUSimple dataset

``` bash
wget -q --show-progress -- "https://s3.us-east-2.amazonaws.com/benchmark-frontend/datasets/1/train_set.zip" 
```

### 2. Extract only files with no groud truth

.json files with labels contain ground truth about the lanes only for the last file in each 20-file sequence (20.jpg). If need only files with ground truth, we can extract only them:

```
 !time 7z x -aos -bso0 ./data/train_set.zip -o./tusimple/ "clips/*/*/20.jpg" "*.json" 
```

Or just unpack all and delete all the other images:
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

#  +profile "*" - removes any ICM, EXIF, IPTC, or other profiles that might be present in the input and aren't needed (uncomment if needed)
```

### 4. Adjust ground truth files
```python 
json_files = list(Path('./tusimple/').glob('*.json'))

DIM_FROM = 1280, 720
DIM_TO = 512, 288

for file in json_files:
  stem = file.with_suffix("")  # path/file.json -> path/file
  new_file = str(stem) + f"_{DIM_TO[0]}x{DIM_TO[1]}.json"

  with Path(file).open() as input, Path(out_file).open() as output:
    for line in input:
      ld = LabelData.from_json(line)
      res = ld.to_relative(1280, 720).to_absolute(512, 288).to_json()
      print(res, file=output)
```

If everything is ok, replace the old files:
``` bash 
cd tusimple; rename -v --force 's/_512x288.json/.json/' *.json
```

### 5. Compress modified files
``` bash
find tusimple_shrinked -type f | sort -V | xargs zip train_set_512x288_gt.zip  

# zip -0 to add files without compression
```
