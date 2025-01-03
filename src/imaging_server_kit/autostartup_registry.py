from fastapi import FastAPI
import docker

class AutoStartupRegistry:
    def __init__(self, algo_servers) -> None:
        self.algo_servers = algo_servers
        self.app = FastAPI()
        self.app.on_event("shutdown")(self.stop_all_algorithm_containers)  # This doesn't work.
        self.docker_client = docker.from_env()
        self.services = {}
        self.register_routes()
    
    def register_routes(self):
        @self.app.get("/")
        def home():
            return list_services()

        @self.app.get("/services")
        def list_services():
            return {"services": list(self.services.keys())}
            
        @self.app.get("/{algorithm}")
        def get_algorithm_url(algorithm):
            if algorithm not in self.services.keys():
                container_url = self.start_algorithm_container(algorithm)
            else:
                container_url = self.services.get(algorithm).get("url")
            return {"url": container_url}
        
    def start_algorithm_container(self, algorithm):
        algorithm_server_image = self.algo_servers[algorithm].get('image')

        port = self.algo_servers[algorithm].get('port')

        container = self.docker_client.containers.run(
            image=algorithm_server_image,
            ports={"8000/tcp": port},
            detach=True,
            remove=True,
            name=f"serverkit-server-{algorithm}"
        )

        container_url = f"http://localhost:{port}"

        self.services[algorithm] = {
            "container": container,
            "url": container_url,
        }

        return container_url

    def stop_algorithm_container(self, algorithm):
        container = self.services[algorithm].get("container")
        container.stop()
    
    def stop_all_algorithm_containers(self):
        for algorithm in self.services.keys():
            self.stop_algorithm_container(algorithm)    