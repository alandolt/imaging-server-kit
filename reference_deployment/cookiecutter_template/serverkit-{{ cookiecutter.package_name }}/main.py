from typing import List, Literal, Type
from pathlib import Path
import numpy as np
from pydantic import BaseModel, Field, validator
import skimage.io
import imaging_server_kit as serverkit

# Import your library
import {{ cookiecutter.package }}

# Define a Pydantic BaseModel to validate your algorithm parameters
class Parameters(BaseModel):
    """Defines the algorithm parameters"""
    image: str = Field(
        ...,
        title="Image",
        description="Base64-encoded numpy array. Should be decoded to a numpy array.",
        json_schema_extra={"widget_type": "image"},
    )
    model_name: Literal['model1', 'model2'] = Field(
        ...,
        title="Model",
        description="Model description.",
        json_schema_extra={"widget_type": "dropdown"},
    )
    threshold: float = Field(
        title="Threshold",
        description="",
        default=0.5,
        ge=0.0,
        le=1.0,
        json_schema_extra={"widget_type": "float"},
    )
    # Numpy arrays should be validated:
    @validator('image', pre=False, always=True)
    def decode_image_array(cls, v) -> np.ndarray:
        image_array = serverkit.decode_contents(v)
        if image_array.ndim not in [2, 3]:
            raise ValueError("Array has the wrong dimensionality.")
        return image_array

# Define the run_algorithm() method for your algorithm
class Server(serverkit.Server):
    def __init__(
        self,
        algorithm_name: str="{{ cookiecutter.package }}",
        parameters_model: Type[BaseModel]=Parameters
    ):
        super().__init__(algorithm_name, parameters_model)

    def run_algorithm(
        self,
        image: np.ndarray,
        model_name: str,
        threshold: float,
        **kwargs
    ) -> List[tuple]:
        """ Runs the algorithm. """
        segmentation = np.zeros_like(image)  # Adjust as necessary

        segmentation_params = {}

        return [(segmentation, segmentation_params, 'labels')]

    def load_sample_images(self) -> List["np.ndarray"]:
        """Load one or multiple sample images."""
        image_dir = Path(__file__).parent / "sample_images"
        images = [skimage.io.imread(image_path) for image_path in image_dir.glob("*")]
        return images

server = Server()
app = server.app
