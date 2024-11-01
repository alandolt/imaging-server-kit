---
title: Imaging Server Kit
emoji: 🦀
colorFrom: yellow
colorTo: pink
sdk: docker
pinned: false
license: mit
short_description: Base image for the Imaging Server Kit project.
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# 🪐 Imaging Server Kit

Run seamlessly interoperable algorithms on images using FastAPI.

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

**Run an algorithm server**

The server will be running on `http://localhost:8000`.

```bash
docker build -t serverkit/rembg .
docker run -it --rm -p 8000:8000 serverkit/rembg
```

**Run an algorithm server with multiple algorithms**

See [deployment](./reference_deployment/README.md). The server will be running on `http://localhost:7000`.

## Usage

**Python client**

Install the `imaging-server-kit` package with `pip`:

```
pip install git+https://gitlab.com/epfl-center-for-imaging/imaging-server-kit.git
```

Connect to an algorithm server and run algorithms from Python:

```python
from imaging_server_kit import Client

client = Client()

client.connect("http://localhost:7000")

print(client.algorithms)
# [`rembg`, `stardist`, `sam2`]

data_tuple = client.run_algorithm(
    algorithm="rembg",
    image=(...),
    rembg_model_name="silueta",
)
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
