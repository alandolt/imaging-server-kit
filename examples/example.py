"""
Demo: Running an algorithm.
"""

import imaging_server_kit as serverkit


def main():
    client = serverkit.Client()
    status_code = client.connect("http://localhost:7000")
    print(f"{status_code=}")
    print(f"{client.algorithms=}")

    algo = client.algorithms[0]  # e.g. `rembg`

    # Get the algo params
    rembg_params = client.get_algorithm_parameters(algo)
    print(f"{rembg_params=}")

    # Get the algo sample image
    rembg_sample_images = client.get_sample_images(algo)
    for image in rembg_sample_images:
        print(f"{image.shape=}")
    sample_image = rembg_sample_images[0]

    # Run the algo (return type is a `LayerDataTuple`)
    algo_output = client.run_algorithm(
        algorithm=algo, image=sample_image, rembg_model_name="silueta"
    )
    for data, data_params, data_type in algo_output:
        print(f"Algo returned: {data_type=} ({data.shape=})")


if __name__ == "__main__":
    main()
