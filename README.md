# image-stitcher
This is a python implementation for stitching images based on overlap region.
- [🛠️ Usage](#️-usage)
- [🎯 Preview of results](#-preview-of-results)
- [🙋‍♂️ Support](#️-support)
- [✉️ Contact](#️-contact)

## 🛠️ Usage
```python
from src.models.run import run
from src.utils.visualizer import result_visualize

merged_image, cand = run(
    image1=image1,       # The first image to be combined
    image2=image2,       # The second image to be combined
    min_overlap=(5, 5),  # The minimum overlap region
    verbose=False,       # Whether to print the log
)
result_visualize(
    image1=image1,              # The first image to be combined
    image2=image2,              # The second image to be combined
    merged_image=merged_image,  # The output image
    cand=cand,                  # The parameters
)
```


## 🎯 Preview of results
The results using [`CIFAR-10`](https://www.cs.toronto.edu/~kriz/cifar.html) are shown below. I would refer you to [`tutorial.ipynb`](https://github.com/C-Naoki/image-stitcher/blob/main/tutorial.ipynb) for detailed results.

<p align="center">
<img src="./docs/assets/input.png" alt="" align=center />
<br><br>
<b>Figure 1.</b> The example of input images. The red area represents an empty region. This application can combine these images while considering their rotation.
</p>

<p align="center">
<img src="./docs/assets/rotated.png" alt="" align=center />
<br><br>
<b>Figure 2.</b> The preprocessed input images. This rotation process is necessary to accurately combine the images. The green frame represents the overlap region between the input images.
</p>

<p align="center">
<img src="./docs/assets/result.png" alt="" align=center />
<br><br>
<b>Figure 3.</b> The output image.
</p>

## 🙋‍♂️ Support
💙 If you like this app, give it a ⭐ and share it with friends!

## ✉️ Contact
💥 For questions or issues, feel free to open an [issue](https://github.com/C-Naoki/image-stitcher/issues). I appreciate your feedback and look forward to hearing from you!
