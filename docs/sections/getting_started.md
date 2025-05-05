# Getting started

This page explains how to run an existing algorithm server and connect to it from Napari and QuPath.

If you are interested in implementing your own server, jump to the next [section]().

## Run your first algo server (locally)

With the `imaging-server-kit` package installed, run:

```
serverkit demo
```

This will start a demo web server for a simple intensity threshold algorithm.

The server will be running on http://localhost:8000. Open your web browser and navigate to this page to check that the server is running. You should see a web page displaying information about the running threshold algorithm server.

[Web page screenshot]()

## Usage from Napari

Now that the server is running, you can interact with it from different client apps. For usage in [Napari](), you need to install napari and the `napari-serverkit` plugin.

You can install the `napari-serverkit` plugin with `pip`:

```sh
pip install napari-serverkit
```

Then, start Napari with the plugin:

```
napari -w napari-serverkit
```

or open the plugin from `Plugins > Server Kit (Napari Server Kit)` in Napari.

With your server still running on http://localhost:8000, you should be able to connect to it, load a sample image, run the threshold algorithm on it, and have the results displayed in the viewer.

[Napari threshold screenshot]()

## Usage from QuPath

You can also interact with the algorithm server via QuPath. To try it out, you need to install the [qupath-extension-serverkit]().

## Usage from Python

It is also possible to connect to an algorithm server and run computation from Python directly:

```python
from imaging_server_kit import Client

# Connect to the server
client = Client("http://localhost:8000")

# run_algorithm returns a list of data tuples
results = client.run_algorithm(
    algorithm="threshold", 
    image=image, 
    threshold=0.5,
)

# Unpack the first result data tuple
mask, result_metadata, result_type = results[0]

# Segmentaiton mask
print(mask.shape)
```
