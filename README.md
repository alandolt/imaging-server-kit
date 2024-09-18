![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# 🪐 Imaging Server Kit

Run algorithms on images via a FastAPI server.

## Setup

First, install the `imaging-server-kit` image with `docker`:

```
docker build -t imaging-server-kit .
```

Then, deploy the server; see [deployment](./deployment/README.md). It'll be running on `http://localhost:7000`.

## Usage

**Python client**

Install the `imaging-server-kit` package with `pip`:

```
pip install git+https://gitlab.com/epfl-center-for-imaging/imaging-server-kit.git
```

Connect to the server and run algorithms from Python:

```python
from imaging_server_kit import ServerKitAPIClient

server_url = "http://localhost:7000"

client = ServerKitAPIClient()
client.connect(server_url)

print(client.algorithms)

import skimage.data
image = skimage.data.astronaut()

data_tuple = client.run_algorithm(
    algorithm="rembg",
    image=image,
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
