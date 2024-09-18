from typing import Dict, List, Tuple
import numpy as np
import imaging_server_kit as serverkit

def serialize_result_tuple(result_data_tuple: List[Tuple]) -> List[Dict]:
    """Converts the result data tuple to dict that can be serialized as JSON (used by the server)."""
    serialized_results = []
    for (data, data_params, data_type) in result_data_tuple:
        if data_type in ['image', 'points', 'shapes', 'vectors', 'tracks']:
            serialized_results.append({
                "type": data_type,
                "data": serverkit.encode_contents(data.astype(np.float32)),
                "data_params": data_params
            })
        elif data_type == 'labels':
            serialized_results.append({
                "type": data_type,
                "data": serverkit.encode_contents(data.astype(np.uint32)),
                "data_params": data_params
            })
        else:
            print(f"Unknown data_type: {data_type}")

    return serialized_results

def deserialize_result_tuple(serialized_results: List[Dict]) -> List[Tuple]:
    """Converts serialized JSON results to a results data tuple (used by the client)."""
    result_data_tuple = []
    for result_dict in serialized_results:
        data_type = result_dict.get("type")
        data = result_dict.get("data")
        data_params = result_dict.get("data_params")
        if data_type in ["image", 'points', 'shapes', 'vectors', 'tracks']:
            data_tuple = (
                serverkit.decode_contents(data).astype(float),
                data_params,
                data_type
            )
        elif data_type == "labels":
            data_tuple = (
                serverkit.decode_contents(data).astype(int),
                data_params,
                data_type
            )
        else:
            data_tuple = (data, data_params, "none")
        result_data_tuple.append(data_tuple)

    return result_data_tuple
