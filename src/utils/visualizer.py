import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from skimage.transform import rotate


def result_visualize(image1, image2, merged_image, cand):
    fig, ax = plt.subplots(1, 2, figsize=(6, 3))
    h1, w1, _ = image1.shape
    h2, w2, _ = image2.shape
    hm, wm, _ = merged_image.shape

    revised_image1 = np.zeros_like(merged_image)
    revised_image1[:, :, :] = 255
    revised_image1[(hm - h1) // 2 : (hm + h1) // 2, (wm - w1) // 2 : (wm + w1) // 2] = image1
    revised_image2 = np.zeros_like(merged_image)
    revised_image2[:, :, :] = 255
    revised_image2[(hm - h2) // 2 : (hm + h2) // 2, (wm - w2) // 2 : (wm + w2) // 2] = image2

    ax[0].imshow(revised_image1)
    ax[0].set_title("Image1")

    ax[1].imshow(revised_image2)
    ax[1].set_title("Image2")

    fig.suptitle("Input Images")
    fig.align_labels()
    fig.tight_layout()

    fig, ax = plt.subplots(1, 2, figsize=(6, 3))

    rotated_image2 = rotate(image2, cand["best_rotation"], resize=True, preserve_range=True).astype(np.uint8)
    h2, w2, _ = rotated_image2.shape
    revised_image2 = np.zeros_like(merged_image)
    revised_image2[:, :, :] = 255
    revised_image2[(hm - h2) // 2 : (hm + h2) // 2, (wm - w2) // 2 : (wm + w2) // 2] = rotated_image2

    hc = min(cand["height"], h1, h2)
    wc = min(cand["width"], w1, w2)
    rect1 = Rectangle(
        (cand["topleft1"].x + (wm - w1) // 2, cand["topleft1"].y + (hm - h1) // 2),
        wc - 1,
        hc - 1,
        linewidth=7,
        edgecolor="g",
        facecolor="none",
    )
    rect2 = Rectangle(
        (cand["topleft2"].x + (wm - w2) // 2, cand["topleft2"].y + (hm - h2) // 2),
        wc - 1,
        hc - 1,
        linewidth=7,
        edgecolor="g",
        facecolor="none",
    )

    ax[0].add_patch(rect1)
    ax[1].add_patch(rect2)

    ax[0].imshow(revised_image1)
    ax[0].set_title("Image1")

    ax[1].imshow(revised_image2)
    ax[1].set_title("Image2")

    fig.suptitle(f"Rotated Input Images ({cand['best_rotation']}°)")
    fig.align_labels()
    fig.tight_layout()

    fig, ax = plt.subplots(1, 1, figsize=(3, 3))

    ax.imshow(merged_image)
    ax.set_title("Merged Image")

    fig.align_labels()
    fig.tight_layout()

    plt.show()
