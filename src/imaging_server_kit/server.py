import importlib.resources
import os
from typing import List, Tuple, Type

import imaging_server_kit as serverkit
import requests
import yaml
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from imaging_server_kit.web_demo import generate_dash_app
from pydantic import BaseModel, ConfigDict
from starlette.middleware.wsgi import WSGIMiddleware

templates_dir = importlib.resources.files("imaging_server_kit").joinpath("templates")
static_dir = importlib.resources.files("imaging_server_kit").joinpath("static")

templates = Jinja2Templates(directory=str(templates_dir))


def load_from_yaml(file_path: str):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def parse_algo_params_schema(algo_params_schema):
    algo_params = algo_params_schema.get("properties")
    required_params = algo_params_schema.get("required")
    for param in algo_params.keys():
        algo_params[param]["required"] = param in required_params
    return algo_params


REGISTRY_URL = os.getenv("REGISTRY_URL", "http://servers_registry:8000")


class Parameters(BaseModel):
    ...

    model_config = ConfigDict(extra="forbid")


class Server:
    def __init__(self, algorithm_name: str, parameters_model: Type[BaseModel]):
        self.algorithm_name = algorithm_name
        self.parameters_model = parameters_model

        self.app = FastAPI(title=algorithm_name)
        self.app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

        # Set up the web demo app
        algo_params = parameters_model.model_json_schema().get("properties")

        dash_app = generate_dash_app(
            algorithm_name,
            algo_params,
            run_fnct=self.run_algorithm,
            sample_image_fnct=self.load_sample_images,
            prefix="/demo/",
        )

        self.app.mount("/demo", WSGIMiddleware(dash_app.server))

        self.app.on_event("startup")(self.register_with_registry)
        self.app.on_event("shutdown")(self.deregister_from_registry)

        self.register_routes()

        self.services = [self.algorithm_name]

    def register_with_registry(self):
        try:
            response = requests.get(f"{REGISTRY_URL}/")
        except Exception:
            print("Registry unavailable.")
            return

        response = requests.post(
            f"{REGISTRY_URL}/register",
            json={
                "name": self.algorithm_name,
                "url": f"http://{self.algorithm_name}:8000",
            },
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
        def home():
            return list_services()

        @self.app.get("/services")
        def list_services():
            return {"services": self.services}

        @self.app.get("/version")
        def get_version():
            return serverkit.__version__

        @self.app.get(f"/{self.algorithm_name}/info", response_class=HTMLResponse)
        def info(request: Request):
            algo_info = load_from_yaml("metadata.yaml")
            algo_params_schema = get_algo_params()
            algo_params = parse_algo_params_schema(algo_params_schema)
            return templates.TemplateResponse(
                "info.html",
                {
                    "request": request,
                    "algo_info": algo_info,
                    "algo_params": algo_params,
                },
            )

        @self.app.post(f"/{self.algorithm_name}/", status_code=status.HTTP_201_CREATED)
        async def run_algo(algo_params: self.parameters_model):
            result_data_tuple = self.run_algorithm(**algo_params.dict())
            serialized_results = serverkit.serialize_result_tuple(result_data_tuple)
            return serialized_results

        @self.app.get(f"/{self.algorithm_name}/parameters", response_model=dict)
        def get_algo_params():
            return self.parameters_model.model_json_schema()

        @self.app.get(f"/{self.algorithm_name}/sample_images", response_model=dict)
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
