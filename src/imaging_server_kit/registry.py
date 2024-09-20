import requests
from fastapi import FastAPI, Request

class RegistryServer:
    def __init__(self) -> None:
        self.app = FastAPI()
        self.services = {}
        self.register_routes()

    def register_routes(self):
        @self.app.get("/")
        def home():
            return list_services()

        @self.app.get("/services")
        def list_services():
            return {"services": list(self.services.keys())}

        @self.app.post("/register")
        async def register_service(request: Request):
            data = await request.json()
            service_name = data.get('name')
            service_url = data.get('url')
            self.services[service_name] = service_url
            return {"message": "Service registered"}

        @self.app.post("/deregister")
        async def deregister_service(request: Request):
            data = await request.json()
            service_name = data.get('name')
            if service_name in self.services:
                del self.services[service_name]
                return {"message": "Service deregistered"}
            return {"error": "Service not found"}

        @self.app.get("/{algorithm}")
        def get_algorithm_status(algorithm):
            url = f"{self.services.get(algorithm)}/"
            response = requests.get(url)
            return response.json()

        @self.app.post("/{algorithm}")
        async def run_algorithm(algorithm, request: Request):
            data = await request.json()
            url = f"{self.services.get(algorithm)}/"
            response = requests.post(url, json=data)
            return response.json()

        @self.app.get("/{algorithm}/parameters")
        def get_algorithm_parameters(algorithm):
            url = f"{self.services.get(algorithm)}/parameters"
            response = requests.get(url)
            return response.json()

        @self.app.get("/{algorithm}/sample_images")
        def get_algorithm_sample_images(algorithm):
            url = f"{self.services.get(algorithm)}/sample_images"
            response = requests.get(url)
            return response.json()
