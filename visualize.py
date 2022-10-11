#!/usr/bin/env python3
import sys
from pathlib import Path
from matplotlib import pyplot as plt

if __name__ == '__main__':
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from TusimpleUtils import TusimpleDataset
else:
    from .dataset import TusimpleDataset


def plot_image(img, label):

    prop_cycle = plt.rcParams['axes.prop_cycle']  # default colors
    colors = prop_cycle.by_key()['color']

    plt.imshow(img.detach().permute(1,2,0))

    n = len(label.lanes)
    for i, lane in enumerate(label.lanes):
        color = colors[i % n]
        plt.plot(lane, label.h_samples, color=color)

if __name__ == "__main__":

    current_dir = Path(__file__).parent
    sample_root = (current_dir / 'tusimple_sample_512x288/').resolve()

    dataset = TusimpleDataset(sample_root, resize_to=(256, 512))

    img, label = dataset[0]
    plot_image(img, label)
    plt.show()