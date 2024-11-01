![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# 🪐 Imaging Server Kit

Run algorithms on images using a FastAPI server.

## Setup

Build the `imaging-server-kit` image with `docker`:

```
docker build -t imaging-server-kit:3.9 .
```

or build specific images:

```
docker build -t imaging-server-kit:3.10 --file Dockerfile-3.10 .
docker build -t imaging-server-kit:gpu --file Dockerfile-GPU .
```

**Run an algorithm registry server (with multiple algorithms to choose from)**

See [deployment](./deployment/README.md). The server will be running on `http://localhost:7000`.

**Run a single algorithm server**

The server will be running on `http://localhost:8000`.

```bash
docker build -t serverkit/rembg .
docker run -it --rm -p 8000:8000 serverkit/rembg
```

## Usage

**Python client**

Install the `imaging-server-kit` package with `pip`:

```
pip install git+https://gitlab.com/epfl-center-for-imaging/imaging-server-kit.git
```

Connect to a server **registry** and run algorithms from Python:

```python
from imaging_server_kit import RegistryClient

client = RegistryClient()

client.connect("http://localhost:7000")

print(client.algorithms)
# [`rembg`, `stardist`, `sam2`]

<<<<<<< HEAD
import skimage.data
image = skimage.data.astronaut()

data_tuple = client.run_algorithm(
=======
algo_output = client.run_algorithm(
>>>>>>> 5fdd1ad (Progress)
    algorithm="rembg",
    image=(...),
    rembg_model_name="silueta",
)
```

Connect to an algorithm **server** and run the algorithm:

```python
from imaging_server_kit import Client

client = Client()

client.connect("http://localhost:8000")

algo_output = client.run_algorithm(
    image=(...),
    rembg_model_name="silueta",
)
for (data, data_params, data_type) in data_tuple:
    print(f"Algo returned: {data_type=} ({data.shape=})")
```

More [examples](./examples/).

**Napari client**

Coming soon.

**Web client**

Coming soon.

**QuPath client**

Coming soon.

**Fiji plugin**

Coming soon.

## Contributing

Contributions are very welcome.

## License

This software is distributed under the terms of the [BSD-3](http://opensource.org/licenses/BSD-3-Clause) license.

## Issues

If you encounter any problems, please file an issue along with a detailed description.
