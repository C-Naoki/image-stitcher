import dataclasses

import numpy as np
from skimage.metrics import mean_squared_error
from skimage.transform import rotate


@dataclasses.dataclass
class Coordinate:
    x: int
    y: int


def run(image1, image2, min_overlap=(5, 5), verbose=False):
    h1, w1, _ = image1.shape
    h2, w2, _ = image2.shape
    min_h, min_w = min_overlap
    core_x1 = [0, w1]
    core_y1 = [0, h1]

    cand = init_candparam()
    for angle in [0, 90, 180, 270]:
        # 画像を回転
        _image2 = rotate(image2, angle, resize=True, preserve_range=True).astype(np.uint8)
        h2, w2, _ = _image2.shape
        core_x2 = [0, w2]
        core_y2 = [0, h2]
        for hc in range(min_h, max(h1, h2) + 1):
            for wc in range(min_w, max(w1, w2) + 1):
                for ix in range(2):
                    for iy in range(2):
                        topleft1 = Coordinate(
                            min(core_x1[ix] + (-1) ** ix * max(wc - w2, 0), core_x1[ix] + (-1) ** ix * min(wc, w1)),
                            min(core_y1[iy] + (-1) ** iy * max(hc - h2, 0), core_y1[iy] + (-1) ** iy * min(hc, h1)),
                        )
                        bottomright1 = Coordinate(
                            max(core_x1[ix] + (-1) ** ix * max(wc - w2, 0), core_x1[ix] + (-1) ** ix * min(wc, w1)),
                            max(core_y1[iy] + (-1) ** iy * max(hc - h2, 0), core_y1[iy] + (-1) ** iy * min(hc, h1)),
                        )
                        overlap1 = image1[topleft1.y : bottomright1.y, topleft1.x : bottomright1.x, :]
                        if verbose:
                            print(f"image1's top-left: {topleft1}")
                            print(f"image1's bottom-right: {bottomright1}")
                        topleft2 = Coordinate(
                            min(
                                core_x2[ix ^ 1] + (-1) ** (ix ^ 1) * max(wc - w1, 0),
                                core_x2[ix ^ 1] + (-1) ** (ix ^ 1) * min(wc, w2),
                            ),
                            min(
                                core_y2[iy ^ 1] + (-1) ** (iy ^ 1) * max(hc - h1, 0),
                                core_y2[iy ^ 1] + (-1) ** (iy ^ 1) * min(hc, h2),
                            ),
                        )
                        bottomright2 = Coordinate(
                            max(
                                core_x2[ix ^ 1] + (-1) ** (ix ^ 1) * max(wc - w1, 0),
                                core_x2[ix ^ 1] + (-1) ** (ix ^ 1) * min(wc, w2),
                            ),
                            max(
                                core_y2[iy ^ 1] + (-1) ** (iy ^ 1) * max(hc - h1, 0),
                                core_y2[iy ^ 1] + (-1) ** (iy ^ 1) * min(hc, h2),
                            ),
                        )
                        overlap2 = _image2[topleft2.y : bottomright2.y, topleft2.x : bottomright2.x, :]
                        if verbose:
                            print(f"image2's top-left: {topleft2}")
                            print(f"image2's bottom-right: {bottomright2}")
                        mse = mean_squared_error(overlap1, overlap2)
                        if mse < cand["best_mse"]:
                            cand["best_mse"] = mse
                            cand["best_rotation"] = angle
                            cand["topleft1"] = topleft1
                            cand["topleft2"] = topleft2
                            cand["bottomright1"] = bottomright1
                            cand["bottomright2"] = bottomright2
                            cand["height"] = hc
                            cand["width"] = wc
    print("\n==== BEST RESULT ====")
    print(f'Best MSE: {cand["best_mse"]}')
    print(f'Best rotation: {cand["best_rotation"]}')
    print(f"image1\'s shape: ({w1}, {h1})")
    print(f"image2\'s shape: ({w2}, {h2})")
    print(f'shared image\'s top-left in image1: {cand["topleft1"]}')
    print(f'shared image\'s bottom-right in image1: {cand["bottomright1"]}')
    print(f'shared image\'s top-left in (rotated) image2: {cand["topleft2"]}')
    print(f'shared image\'s bottom-right in (rotated) image2: {cand["bottomright2"]}')
    print(f'shared image\'s height: {cand["height"]}')
    print(f'shared image\'s width: {cand["width"]}')

    revised_image2 = rotate(image2, cand["best_rotation"], resize=True, preserve_range=True).astype(np.uint8)
    h2, w2, _ = revised_image2.shape
    hc, wc = cand["height"], cand["width"]
    merged_image = np.zeros((h1 + h2 - cand["height"], w1 + w2 - cand["width"], 3), dtype=np.uint8)
    merged_image[:, :, 0] = 255
    hm, wm, _ = merged_image.shape
    if hc <= min(h1, h2) and wc <= min(w1, w2):
        left1 = 1 if cand["topleft1"].x == 0 else 0
        left2 = 1 if cand["topleft2"].x == 0 else 0
        top1 = 1 if cand["topleft1"].y == 0 else 0
        top2 = 1 if cand["topleft2"].y == 0 else 0
        merged_image[(h2 - hc) * top1 : h1 + (h2 - hc) * top1, (w2 - wc) * left1 : w1 + (w2 - wc) * left1, :] = image1
        merged_image[(h1 - hc) * top2 : h2 + (h1 - hc) * top2, (w1 - wc) * left2 : w2 + (w1 - wc) * left2, :] = (
            revised_image2
        )
    elif hc > min(h1, h2) or wc > min(w1, w2):
        raise NotImplementedError
    else:
        small_image = image1 if h1 < h2 else revised_image2
        large_image = image1 if h1 >= h2 else revised_image2
        merged_image = large_image.copy()
        merged_image[: small_image.shape[0], : small_image.shape[1]] = small_image

        raise NotImplementedError

    return merged_image, cand


def init_candparam():
    return {
        "best_mse": float("inf"),
        "best_rotation": None,
        "topleft1": None,
        "topleft2": None,
        "bottomright1": None,
        "bottomright2": None,
        "height": None,
        "width": None,
    }
