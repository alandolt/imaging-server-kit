import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import Server

def test_run_algorithm():
    server = Server()
    # images = server.load_sample_images()
    # print(images)
    result = server.run_algorithm(
        server.load_sample_images()[1],
        min_sigma=2,
        max_sigma=3,
        num_sigma=3,
        threshold=0.4,
        invert_image=False,
        time_dim=True,
    )
    assert isinstance(result[0][0], np.ndarray), \
    "Segmentation failed or did not output an array."

if __name__ == "__main__":
    test_run_algorithm()
