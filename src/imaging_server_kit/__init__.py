from ._version import version as __version__

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from imaging_server_kit.client import Client
from imaging_server_kit.server import AlgorithmServer, Parameters
from imaging_server_kit.authenticated_server import AuthenticatedAlgorithmServer
from imaging_server_kit.algorithm_hub import AlgorithmHub
from imaging_server_kit.encoding import encode_contents, decode_contents
from imaging_server_kit.serialization import (
    serialize_result_tuple,
    deserialize_result_tuple,
)
from imaging_server_kit.geometry import (
    mask2features,
    instance_mask2features,
    features2mask,
    features2instance_mask,
    features2mask_3d,
    mask2features_3d,
    instance_mask2features_3d,
    features2instance_mask_3d,
    boxes2features,
    features2boxes,
    points2features,
    features2points,
    vectors2features,
    features2vectors,
)

from imaging_server_kit.decorator import algorithm_server
from imaging_server_kit.multialgo_server import MultiAlgorithmServer
