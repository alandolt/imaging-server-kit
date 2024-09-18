import requests
from typing import List, Dict, Tuple
import imaging_server_kit as serverkit
import numpy as np

class ServerKitAPIClient:
    def __init__(self) -> None:
        self._server_ip = ""
        self._algorithms = {}

    def connect(self, server_ip: str) -> int:
        self.server_ip = server_ip

        try:
            response = requests.get(f"{self.server_ip}/services")
        except Exception:
            self.algorithms = {}
            return -1

        if response.status_code == 200:
            services = response.json().get("services")
            self.algorithms = services
        else:
            self.algorithms = {}

        return response.status_code

    @property
    def server_ip(self) -> str:
        return self._server_ip

    @server_ip.setter
    def server_ip(self, server_ip: str):
        self._server_ip = server_ip

    @property
    def algorithms(self) -> Dict[str, str]:
        return self._algorithms

    @algorithms.setter
    def algorithms(self, algorithms: Dict[str, str]):
        self._algorithms = algorithms

    def run_algorithm(self, algorithm: str = "rembg", **algo_params) -> List[Tuple]:
        if algorithm not in self.algorithms:
            print(f"Not an available algorithm: {algorithm}")
            return []

        # Encode all the numpy array parameters
        for param in algo_params:
            if isinstance(algo_params[param], np.ndarray):
                algo_params[param] = serverkit.encode_contents(algo_params[param])

        response = requests.post(f"{self.server_ip}/{algorithm}/", json=algo_params, timeout=300)
        if response.status_code == 422:
            print("Error: Unprocessable Entity.")
            return []

        return serverkit.deserialize_result_tuple(response.json())

    def get_algorithm_parameters(self, algorithm: str) -> Dict:
        parameters = requests.get(f"{self.server_ip}/{algorithm}/algorithm_parameters").json()
        return parameters

    def get_sample_images(self, algorithm: str) -> "np.ndarray":
        response = requests.get(f"{self.server_ip}/{algorithm}/sample_images")

        images = []
        for content in response.json().get("sample_images"):
            encoded_image = content.get("sample_image")
            image = serverkit.decode_contents(encoded_image)
            images.append(image)
        return images
