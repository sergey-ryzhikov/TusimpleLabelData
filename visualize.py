#!/usr/bin/env python3
import sys
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
from functools import cmp_to_key

if __name__ == '__main__':
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from TusimpleUtils import TusimpleDataset
else:
    from .dataset import TusimpleDataset


def plot_image(img, label, numbers=True, fontsize=12, **plot_args):

    prop_cycle = plt.rcParams['axes.prop_cycle']  # default colors
    colors = prop_cycle.by_key()['color']

    ax = plt.gca()

    c, height, width = img.shape
    ax.imshow(img.detach().permute(1,2,0))
    

    # Lanes in dataset are not in order, so sort them left to right
    lanes_sorted = sorted(label.lanes, 
                        key=cmp_to_key(lambda a,b: np.nansum(a-b)))  # compares only non-nan values

    for i, lane in enumerate(lanes_sorted):
        color = colors[i % len(colors)]

        # plot line
        plt.plot(lane, label.h_samples, 
                **{'color': color, **plot_args}  # use default color if not specified
                )

        # plot line number
        if numbers:
            x = np.nanmean(lane)
            present_samples = label.h_samples[~np.isnan(lane)]
            y = np.nanmean(present_samples)
            plt.text(x, y, str(i+1), 
                        color="red", fontsize=fontsize, weight='bold', ha='center', va='center')

            # plot number background
            # circle = plt.Circle((x/width, y/height), fontsize/width, color=color, fill=True, zorder=2)
            # ax.add_patch(circle)

    plt.show()
            



if __name__ == "__main__":

    current_dir = Path(__file__).parent
    sample_root = (current_dir / 'tusimple_sample_512x288/').resolve()

    dataset = TusimpleDataset(sample_root, resize_to=(256, 512))

    img, label = dataset[7]
    plot_image(img, label, linewidth=10, alpha=0.5, )

    plt.show()



# #TODO: 
# from torchvision.utils import draw_segmentation_masks
# img = draw_segmentation_masks(img, mask, alpha=0.8, colors="blue"))
