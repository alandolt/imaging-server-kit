from functools import partial
from typing import Callable, List

import skimage.io
from imaging_server_kit import AlgorithmServer, decode_contents
from pydantic import BaseModel, Field, create_model, field_validator


def decode_image_array(cls, v, dimensionality) -> "np.ndarray":
    image_array = decode_contents(v)

    if image_array.ndim not in dimensionality:
        raise ValueError("Array has the wrong dimensionality.")

    return image_array


def parse_params(parameters: dict) -> BaseModel:
    fields = {}
    validators = {}
    for param_name, param_details in parameters.items():
        field_constraints = {"json_schema_extra": {}}

        if hasattr(param_details, "min"):
            field_constraints["ge"] = param_details.min
        if hasattr(param_details, "max"):
            field_constraints["le"] = param_details.max
        if hasattr(param_details, "default"):
            field_constraints["default"] = param_details.default
        if hasattr(param_details, "title"):
            field_constraints["title"] = param_details.title
        if hasattr(param_details, "description"):
            field_constraints["description"] = param_details.description
        if hasattr(param_details, "step"):
            field_constraints["json_schema_extra"]["step"] = param_details.step

        field_constraints["json_schema_extra"][
            "widget_type"
        ] = param_details.widget_type

        if param_details.widget_type == "image":
            validated_func = partial(
                decode_image_array, dimensionality=param_details.dimensionality
            )
            validators["image_validator"] = field_validator("image", mode="after")(
                validated_func
            )

        fields[param_name] = (param_details.type, Field(**field_constraints))

    return create_model("Parameters", **fields, __validators__=validators)


class CustomAlgorithmServer(AlgorithmServer):
    def __init__(
        self,
        algorithm_name,
        parameters_model,
        metadata_file,
        func: Callable,
        sample_images: List,
    ):
        super().__init__(algorithm_name, parameters_model, metadata_file)
        self.func = func
        self.sample_images = sample_images

    def run_algorithm(self, **algo_params):
        return self.func(**algo_params)

    def load_sample_images(self) -> List["np.ndarray"]:
        return [skimage.io.imread(image_path) for image_path in self.sample_images]


def algorithm_server(
    algorithm_name="algorithm",
    parameters=None,
    sample_images=[],
    metadata_file: str = None,
):
    def wrapper(func: Callable):
        algo_server = CustomAlgorithmServer(
            algorithm_name=algorithm_name,
            parameters_model=parse_params(parameters),
            metadata_file=metadata_file,
            func=func,
            sample_images=sample_images,
        )

        return algo_server

    return wrapper
