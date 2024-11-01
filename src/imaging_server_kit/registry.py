import requests
from fastapi import FastAPI, Request, status, HTTPException


class Registry:
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

        @self.app.post("/register", status_code=status.HTTP_201_CREATED)
        async def register_service(request: Request):
            data = await request.json()
            service_name = data.get("name")
            service_url = data.get("url")
            if service_name in self.services:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Service {service_name} is already registered.",
                )

            self.services[service_name] = service_url
            return {"message": "Service registered"}

        @self.app.post("/deregister", status_code=status.HTTP_201_CREATED)
        async def deregister_service(request: Request):
            data = await request.json()
            service_name = data.get("name")
            if service_name in self.services:
                del self.services[service_name]
                return {"message": "Service deregistered"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Service {service_name} could not be deregistered because it is not in the list of services.",
                )

        @self.app.get("/{algorithm}")
        def get_algorithm_status(algorithm):
            response = requests.get(f"{self.services.get(algorithm)}/")
            return response.json()

        @self.app.post("/{algorithm}", status_code=status.HTTP_201_CREATED)
        async def run_algorithm(algorithm, request: Request):
            data = await request.json()
            response = requests.post(
                f"{self.services.get(algorithm)}/{algorithm}/", json=data
            )
            return response.json()

        @self.app.get("/{algorithm}/parameters")
        def get_algorithm_parameters(algorithm):
            response = requests.get(
                f"{self.services.get(algorithm)}/{algorithm}/parameters"
            )
            return response.json()

        @self.app.get("/{algorithm}/sample_images")
        def get_algorithm_sample_images(algorithm):
            response = requests.get(
                f"{self.services.get(algorithm)}/{algorithm}/sample_images"
            )
            return response.json()
