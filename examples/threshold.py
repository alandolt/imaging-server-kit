from pathlib import Path
import numpy as np
import uvicorn
from skimage.exposure import rescale_intensity
from imaging_server_kit import algorithm_server, ImageUI, FloatSpinBoxUI

@algorithm_server(
    algorithm_name="intensity-threshold",
    title="Binary Threshold",
    description="Implementation of a binary threshold algorithm.",
    used_for=["Segmentation"],
    tags=["EPFL"],
    parameters={
        "image": ImageUI(
            title="Image",
            description="Input image (2D, 3D)",
            dimensionality=[2, 3],
        ),
        "threshold": FloatSpinBoxUI(
            default=0.5,
            title="Threshold",
            description="Intensity threshold.",
            min=0.0,
            max=1.0,
            step=0.1,
        ),
    },
    sample_images=[str(Path(__file__).parent / "sample_images" / "blobs.tif")],
)
def serve_threshold(
    image: np.ndarray,
    threshold: float,
):
    """Implements a simple intensity threshold algorithm."""
    mask = (rescale_intensity(image, out_range=(0, 1)) > threshold).astype(int)
    return [(mask, {"name": "Threshold result"}, "mask")]


if __name__ == "__main__":
    uvicorn.run(serve_threshold.app, host="0.0.0.0", port=8000)
