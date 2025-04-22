from pathlib import Path
import numpy as np
import uvicorn
from skimage.filters import threshold_li, threshold_otsu
from imaging_server_kit import algorithm_server, ImageUI, DropDownUI


@algorithm_server(
    algorithm_name="automatic-threshold",
    title="Automatic Threshold",
    description="Implementation of an automatic threshold algorithm.",
    used_for=["Segmentation"],
    tags=["Scikit-image", "EPFL"],
    parameters={
        "image": ImageUI(
            title="Image",
            description="Input image (2D, 3D)",
            dimensionality=[2, 3],
        ),
        "method": DropDownUI(
            default="otsu",
            title="Method",
            description="Auto-threshold method.",
            items=["Otsu", "Li"],
        ),
    },
    sample_images=[str(Path(__file__).parent / "sample_images" / "blobs.tif")],
)
def serve_auto_threshold(
    image: np.ndarray,
    method: str,
):
    if method == "Otsu":
        mask = (image > threshold_otsu(image)).astype(int)
    elif method == "Li":
        mask = (image > threshold_li(image)).astype(int)

    return [(mask, {"name": f"Threshold result ({method})"}, "mask")]


if __name__ == "__main__":
    uvicorn.run(serve_auto_threshold.app, host="0.0.0.0", port=8000)
