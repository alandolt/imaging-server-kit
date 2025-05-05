## Using Docker

The Imaging Server Kit provides an **algorithm hub** to serve multiple algorithms in separate docker containers.

To set up an algorithm hub, the easiest is to use a `docker-compose.yml` file.

Here is the [example from the respository]():

```
services:
  algorithm_hub:
    build: ../..
    ports:
      - "8000:8000"
    command: python3 start_algorithm_hub.py
  cellpose:
    build: ./serverkit-cellpose
    depends_on:
      - algorithm_hub
  stardist:
    build: ./serverkit-stardist
    depends_on:
      - algorithm_hub
```

Build the algorithm hub server with

```sh
docker compose build
```

Start the algorithm hub server with

```sh
docker compose up
```

The server will be listening on http://localhost:8000. It behaves exactly like a [Multi-algorithm server](), however each algorithm runs in a separate docker container.