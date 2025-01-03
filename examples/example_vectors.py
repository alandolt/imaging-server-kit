"""
Demo: Running an algorithm.
"""

import imaging_server_kit as serverkit


def main():
    client = serverkit.Client()
    status_code = client.connect("http://localhost:8000")
    print(f"{status_code=}")
    print(f"{client.algorithms=}")

    algo = "orientationpy"

    # Get the algo params
    params = client.get_algorithm_parameters(algo)
    print(f"{params=}")

    # Get the algo sample image
    sample_images = client.get_sample_images(algo)
    for image in sample_images:
        print(f"{image.shape=}")
    sample_image = sample_images[0]
    sample_image = sample_image[200:300, 200:300]


    # Run the algo (return type is a `LayerDataTuple`)
    algo_output = client.run_algorithm(
        algorithm=algo, 
        image=sample_image,
        mode="fiber",
        scale=1.0,
        with_colors=False,
        vector_spacing=3,
    )
    for data, data_params, data_type in algo_output:
        print(f"Algo returned: {data_type=}")


if __name__ == "__main__":
    main()
