from typing import List, Literal, Tuple, Type, Union
from pathlib import Path
import skimage.io
import numpy as np
from pydantic import BaseModel, Field, validator
import imaging_server_kit as serverkit
import skimage.feature
from skimage.exposure import rescale_intensity


class Parameters(BaseModel):
    """Defines the algorithm parameters"""

    image: str = Field(
        ...,
        title="Image",
        description="Base64-encoded numpy array. Should be decoded to a numpy array.",
        json_schema_extra={"widget_type": "image"},
    )
    min_sigma: float = Field(
        title="Min sigma",
        description="",
        default=5.0,
        ge=0.1,
        le=100.0,
        json_schema_extra={"widget_type": "float"},
    )
    max_sigma: float = Field(
        title="Max sigma",
        description="",
        default=10.0,
        ge=0.1,
        le=100.0,
        json_schema_extra={"widget_type": "float"},
    )
    num_sigma: int = Field(
        title="Num sigma",
        description="",
        default=10,
        ge=1,
        le=100,
        json_schema_extra={"widget_type": "int"},
    )
    threshold: float = Field(
        title="Threshold",
        description="",
        default=0.1,
        ge=0.01,
        le=1.0,
        json_schema_extra={"widget_type": "float"},
    )
    invert_image: bool = Field(
        default=False,
        title="Dark blobs",
        description="",
        json_schema_extra={"widget_type": "bool"},
    )
    time_dim: bool = Field(
        default=True,
        title="Frame by frame",
        description="",
        json_schema_extra={"widget_type": "bool"},
    )

    @validator("image", pre=False, always=True)
    def decode_image_array(cls, v) -> np.ndarray:
        image_array = serverkit.decode_contents(v)
        if image_array.ndim not in [2, 3]:
            raise ValueError("Array has the wrong dimensionality.")
        return image_array


# Define the run_algorithm() method for your algorithm
class Server(serverkit.Server):
    def __init__(
        self,
        algorithm_name: str = "skimage",
        parameters_model: Type[BaseModel] = Parameters,
    ):
        super().__init__(algorithm_name, parameters_model)

    def run_algorithm(
        self,
        image: np.ndarray,
        min_sigma: float,
        max_sigma: float,
        num_sigma: int,
        threshold: float,
        invert_image: bool,
        time_dim: bool,
        **kwargs,
    ) -> List[tuple]:
        """Runs the skimage algorithm."""

        if invert_image:
            image = -image

        image = rescale_intensity(image, out_range=(0, 1))

        if (image.ndim == 3) & time_dim:
            # Handle a time-series
            points = np.empty((0, 3))
            for frame_id, frame in enumerate(image):
                frame_results = skimage.feature.blob_log(
                    frame,
                    min_sigma=min_sigma,
                    max_sigma=max_sigma,
                    num_sigma=num_sigma,
                    threshold=threshold,
                )
                frame_points = frame_results[:, :2]  # Shape (N, 2)
                frame_points = np.hstack(
                    (np.array([frame_id] * len(frame_points))[..., None], frame_points)
                )  # Shape (N, 3)
                points = np.vstack((points, frame_points))
        else:
            results = skimage.feature.blob_log(
                image,
                min_sigma=min_sigma,
                max_sigma=max_sigma,
                num_sigma=num_sigma,
                threshold=threshold,
            )
            points = results[:, :2]

        points_params = {
            "name": "Detections",
            "opacity": 0.7,
        }

        return [(points, points_params, "points")]

    def load_sample_images(self) -> List["np.ndarray"]:
        """Load one or multiple sample images."""
        image_dir = Path(__file__).parent / "sample_images"
        images = [skimage.io.imread(image_path) for image_path in image_dir.glob("*")]
        return images


server = Server()
app = server.app
