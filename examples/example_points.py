"""
Demo: Running an algorithm.
"""

import imaging_server_kit as serverkit


def main():
    client = serverkit.Client()
    status_code = client.connect("http://localhost:8000")
    print(f"{status_code=}")
    print(f"{client.algorithms=}")

    algo = "skimage"

    # Get the algo params
    params = client.get_algorithm_parameters(algo)
    print(f"{params=}")

    # Get the algo sample image
    sample_images = client.get_sample_images(algo)
    for image in sample_images:
        print(f"{image.shape=}")
    sample_image = sample_images[0]

    # Run the algo (return type is a `LayerDataTuple`)
    algo_output = client.run_algorithm(
        algorithm=algo, 
        image=sample_image,
        min_sigma=1,
        max_sigma=2,
        num_sigma=4,
        threshold=0.04,
        invert_image=False,
        time_dim=False,
    )
    for data, data_params, data_type in algo_output:
        import pdb; pdb.set_trace()
        print(f"Algo returned: {data_type=}")
        


if __name__ == "__main__":
    main()
