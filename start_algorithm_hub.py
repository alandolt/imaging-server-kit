import uvicorn
import imaging_server_kit as serverkit

server = serverkit.AlgorithmHub()
app = server.app

if __name__ == "__main__":
    uvicorn.run("start_algorithm_hub:app", host="0.0.0.0", port=8000)
