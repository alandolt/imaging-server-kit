import requests
from typing import List, Dict, Tuple
import imaging_server_kit as serverkit
import numpy as np


class Client:
    def __init__(self) -> None:
        self._server_url = ""
        self._algorithms = {}

    def connect(self, server_url: str) -> int:
        self.server_url = server_url

        try:
            response = requests.get(f"{self.server_url}/services")
        except Exception:
            self.algorithms = {}
            return (-1, "Server unavailable.")

        if response.status_code == 200:
            services = response.json().get("services")
            self.algorithms = services
            return (response.status_code, services)
        else:
            response_body = response.json()
            self.algorithms = {}
            return (response.status_code, response_body)

    @property
    def server_url(self) -> str:
        return self._server_url

    @server_url.setter
    def server_url(self, server_url: str):
        self._server_url = server_url

    @property
    def algorithms(self) -> Dict[str, str]:
        return self._algorithms

    @algorithms.setter
    def algorithms(self, algorithms: Dict[str, str]):
        self._algorithms = algorithms

    def run_algorithm(self, algorithm: str = None, **algo_params) -> List[Tuple]:
        if algorithm is None:
            if len(self.algorithms) > 0:
                algorithm = self.algorithms[0]
            else:
                print("No algorithms available.")
                return []

        if algorithm not in self.algorithms:
            print(f"Not an available algorithm: {algorithm}")
            return []

        # Encode all numpy array parameters
        for param in algo_params:
            if isinstance(algo_params[param], np.ndarray):
                algo_params[param] = serverkit.encode_contents(algo_params[param])

        response = requests.post(
            f"{self.server_url}/{algorithm}/", 
            json=algo_params,
            headers={
                'Content-Type': 'application/json',
                'accept': 'application/json',
            }
        )
        if response.status_code == 201:
            return serverkit.deserialize_result_tuple(response.json())
        elif response.status_code == 422:
            # This actually doesn't occurr when it should...
            print(f"Algorithm parameters are not valid!")
            return []
        else:
            print(
                f"Algorithm server returned an error status code: {response.status_code}"
            )
            return []

    def get_algorithm_parameters(self, algorithm: str = None) -> Dict:
        if algorithm is None:
            if len(self.algorithms) > 0:
                algorithm = self.algorithms[0]
            else:
                print("No algorithms available.")
                return []
        
        response = requests.get(f"{self.server_url}/{algorithm}/parameters")
        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Error status while attempting to get algoritm parameters: {response.status_code}"
            )
            return -1

    def get_sample_images(self, algorithm: str = None) -> "np.ndarray":
        if algorithm is None:
            if len(self.algorithms) > 0:
                algorithm = self.algorithms[0]
            else:
                print("No algorithms available.")
                return []
        
        response = requests.get(f"{self.server_url}/{algorithm}/sample_images")

        if response.status_code == 200:
            images = []
            for content in response.json().get("sample_images"):
                encoded_image = content.get("sample_image")
                image = serverkit.decode_contents(encoded_image)
                images.append(image)
            return images
        else:
            print(
                f"Error status while attempting to get algorithm sample images: {response.status_code}"
            )
            return -1
