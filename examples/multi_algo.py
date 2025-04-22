import uvicorn
from imaging_server_kit import MultiAlgorithmServer

from auto_threshold import serve_auto_threshold
from threshold import serve_threshold

server = MultiAlgorithmServer(
    server_name="multi-algo",
    algorithm_servers=[serve_auto_threshold, serve_threshold],
)

if __name__ == "__main__":
    uvicorn.run(server.app, host="0.0.0.0", port=8000)
