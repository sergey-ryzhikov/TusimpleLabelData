#!/usr/bin/env python3
import sys
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np

if __name__ == '__main__':
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from TusimpleUtils import TusimpleDataset
else:
    from .dataset import TusimpleDataset


def plot_image(img, label, **plot_args):

    prop_cycle = plt.rcParams['axes.prop_cycle']  # default colors
    colors = prop_cycle.by_key()['color']

    plt.imshow(img.detach().permute(1,2,0))


    # Lanes in dataset are not in order, so sort them left to right
    for i, lane in enumerate(sorted(label.lanes, key=lambda lane: np.nanmean(lane))):
        color = colors[i % len(colors)]
        plt.plot(lane, label.h_samples, 
                **{'color': color, **plot_args}  # use default color if not specified
                )


if __name__ == "__main__":

    current_dir = Path(__file__).parent
    sample_root = (current_dir / 'tusimple_sample_512x288/').resolve()

    dataset = TusimpleDataset(sample_root, resize_to=(256, 512))

    img, label = dataset[7]
    plot_image(img, label, linewidth=10, alpha=0.5)

    plt.show()



# #TODO: 
# from torchvision.utils import draw_segmentation_masks
# img = draw_segmentation_masks(img, mask, alpha=0.8, colors="blue"))
