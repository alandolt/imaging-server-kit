![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# 🪐 Imaging Server Kit

Run algorithms on images via a FastAPI server.

## Installation

```
pip install -e .
```

## Usage

**Server**

The server is [...].

```python
from imaging_server_kit import AlgorithmServer
```

**Client**

The client is [...].

```python
from imaging_server_kit import ServerKitAPIClient

client = ServerKitAPIClient("http://localhost:7000")
client.connect()

print(client.algorithms)

import skimage.data
image = skimage.data.astronaut()

segmentation = client.run_segmentation(
    image,
    algorithm="rembg",
    rembg_model_name="silueta",
)
```

## Contributing

Contributions are very welcome.

## License

This software is distributed under the terms of the [BSD-3](http://opensource.org/licenses/BSD-3-Clause) license.

## Issues

If you encounter any problems, please file an issue along with a detailed description.
