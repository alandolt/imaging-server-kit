import os
import requests
from typing import Type, List, Tuple
from pydantic import BaseModel, ConfigDict
from fastapi import FastAPI, status
import imaging_server_kit as serverkit


REGISTRY_URL = os.getenv("REGISTRY_URL", "http://servers_registry:8000")


class Parameters(BaseModel):
    ...

    model_config = ConfigDict(extra="forbid")


class AlgorithmServer:
    def __init__(self, algorithm_name: str, parameters_model: Type[BaseModel]):
        self.algorithm_name = algorithm_name
        self.parameters_model = parameters_model
        self.service_url = f"http://{algorithm_name}:8000"

        self.app = FastAPI(title=algorithm_name)

        self.app.on_event("startup")(self.register_with_registry)
        self.app.on_event("shutdown")(self.deregister_from_registry)

        self.register_routes()

    def register_with_registry(self):
        try:
            response = requests.get(f"{REGISTRY_URL}/")
        except Exception:
            print("Registry unavailable.")
            return

        response = requests.post(
            f"{REGISTRY_URL}/register",
            json={"name": self.algorithm_name, "url": self.service_url},
        )
        if response.status_code == 201:
            print(f"Service {self.algorithm_name} registered successfully.")
        else:
            print(f"Failed to register {self.algorithm_name}: {response.json()}")

    def deregister_from_registry(self):
        deregister_url = f"{REGISTRY_URL}/deregister"
        response = requests.post(deregister_url, json={"name": self.algorithm_name})
        if response.status_code == 201:
            print(f"Service {self.algorithm_name} deregistered.")
        else:
            print(f"Failed to deregister {self.algorithm_name}: {response.json()}")

    def register_routes(self):
        @self.app.get("/")
        def read_status():
            return {"Status": "running"}

        # I noted that the 422 error doesn't get raised when parameters are invalid. Weird?
        @self.app.post("/", status_code=status.HTTP_201_CREATED)
        async def run_algo(algo_params: self.parameters_model):  # To check: this should automatically validate the parameters and return HTTP-422 otherwise?
            result_data_tuple = self.run_algorithm(**algo_params.dict())
            serialized_results = serverkit.serialize_result_tuple(result_data_tuple)
            return serialized_results

        @self.app.get("/parameters", response_model=dict)
        def get_algo_params():
            return self.parameters_model.model_json_schema()

        @self.app.get("/sample_images", response_model=dict)
        def get_sample_images():
            images = self.load_sample_images()
            encoded_images = [
                {"sample_image": serverkit.encode_contents(image)} for image in images
            ]
            return {"sample_images": encoded_images}

    def load_sample_images(self) -> List["np.ndarray"]:
        raise NotImplementedError("Subclasses should implement this method")

    def run_algorithm(self, **algo_params) -> List[Tuple]:
        raise NotImplementedError("Subclasses should implement this method")
