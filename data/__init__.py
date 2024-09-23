from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from skimage.transform import rotate
from sklearn.datasets import fetch_openml


def load_data(idx: int = 0) -> Union[np.ndarray, pd.Series]:
    cifar10 = fetch_openml("CIFAR_10")

    data = cifar10["data"]
    target = cifar10["target"]
    X = np.array(data).reshape(-1, 3, 32, 32).astype(np.uint8)

    return np.transpose(X[idx], (1, 2, 0)), target


def split_data(
    image: np.ndarray, slicex: tuple, slicey: tuple, angle: int = 0, plot: bool = False
) -> Union[np.ndarray, np.ndarray]:
    if plot:
        viz_image1 = np.zeros_like(image)
        viz_image1[:, :, 0] = 255
        viz_image1[slicey[0], slicex[0], :] = image[slicey[0], slicex[0], :]
        viz_image2 = np.zeros_like(image)
        viz_image2[:, :, 0] = 255
        viz_image2[slicey[1], slicex[1], :] = image[slicey[1], slicex[1], :]

        fig, ax = plt.subplots(1, 3, figsize=(7, 3))

        ax[0].imshow(image)
        ax[0].set_title(f"Original {image.shape[1]}x{image.shape[0]}")
        ax[0].axis("off")

        ax[1].imshow(viz_image1)
        ax[1].set_title(f"First {slicey[0].stop - slicey[0].start}x{slicex[0].stop - slicex[0].start}")
        ax[1].axis("off")

        ax[2].imshow(viz_image2)
        ax[2].set_title(f"Second {slicey[1].stop - slicey[1].start}x{slicex[1].stop - slicex[1].start}")
        ax[2].axis("off")

        rect1 = Rectangle(
            (max(slicex[0].start, slicex[1].start), max(slicey[0].start, slicey[1].start)),
            min(slicex[0].stop, slicex[1].stop) - max(slicex[0].start, slicex[1].start) - 1,
            min(slicey[0].stop, slicey[1].stop) - max(slicey[0].start, slicey[1].start) - 1,
            linewidth=7,
            edgecolor="g",
            facecolor="none",
        )
        rect2 = Rectangle(
            (max(slicex[0].start, slicex[1].start), max(slicey[0].start, slicey[1].start)),
            min(slicex[0].stop, slicex[1].stop) - max(slicex[0].start, slicex[1].start) - 1,
            min(slicey[0].stop, slicey[1].stop) - max(slicey[0].start, slicey[1].start) - 1,
            linewidth=7,
            edgecolor="g",
            facecolor="none",
        )

        ax[1].add_patch(rect1)
        ax[2].add_patch(rect2)

    image1 = image[slicey[0], slicex[0], :]
    image2 = image[slicey[1], slicex[1], :]

    rotated_image2 = rotate(image2, angle, resize=True, preserve_range=True).astype(np.uint8)

    return image1, rotated_image2
