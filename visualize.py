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


def plot_image(img, label, numbers=True, fontsize=12, **plot_args):

    prop_cycle = plt.rcParams['axes.prop_cycle']  # default colors
    colors = prop_cycle.by_key()['color']

    ax = plt.gca()

    c, height, width = img.shape
    ax.imshow(img.detach().permute(1,2,0))
    

    # Lanes in dataset are not in order, so sort them left to right
    lanes_sorted = label.lanes_sorted

    for i, lane in enumerate(lanes_sorted):
        color = colors[i % len(colors)]

        args = {'color': color, **plot_args}  # use default colormap if color is not specified
        # TODO: accept an iterable of colors

        # plot line
        plt.plot(lane, label.h_samples, **args)

        # plot number of line
        if numbers :
            idx_not_nan = ~np.isnan(lane)
            if np.count_nonzero(idx_not_nan) < 2:  # at least two points required
                continue

            present_samples = label.h_samples[idx_not_nan]
        
            xpos = np.nanmean(lane)    
            ypos = np.nanmean(present_samples)

            # plot line number
            plt.text(xpos, ypos, str(i+1), 
                        color="white", fontsize=fontsize, weight='bold', ha='center', va='center')

            # plot number background circle
            circle = plt.Circle((xpos, ypos), fontsize, 
                                color=color, fill=True, linewidth=3 
                                )
            ax.add_patch(circle)

    plt.show()
            


if __name__ == "__main__":

    current_dir = Path(__file__).parent
    sample_root = (current_dir / 'tusimple_sample_512x288/').resolve()

    dataset = TusimpleDataset(sample_root, resize_to=(256, 512))

    img, label = dataset[9]
    plot_image(img, label, linewidth=10, alpha=0.5, solid_capstyle='round' )

    plt.show()



# #TODO: 
# from torchvision.utils import draw_segmentation_masks
# img = draw_segmentation_masks(img, mask, alpha=0.8, colors="blue"))
