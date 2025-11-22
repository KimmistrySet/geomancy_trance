import json
from typing import Any, Dict, List, Union

# Import nodes from your package
from nodes.geometry import CubeNode, SphereNode, PyramidNode, CylinderNode, NoiseNode, TerrainNode
from nodes.math import Matrix4x4Node, MatrixMultiplyNode, VectorMatrixMultiplyNode

# Map JSON "type" strings to actual classes
NODE_MAP = {
    "CubeNode": CubeNode,
    "SphereNode": SphereNode,
    "PyramidNode": PyramidNode,
    "CylinderNode": CylinderNode,
    "NoiseNode": NoiseNode,
    "TerrainNode": TerrainNode,
    "Matrix4x4Node": Matrix4x4Node,
    "MatrixMultiplyNode": MatrixMultiplyNode,
    "VectorMatrixMultiplyNode": VectorMatrixMultiplyNode,
    # Add others if you want them available in JSON
}

def _to_serializable(vertices: Any) -> Any:
    """
    Ensure outputs are JSON-serializable (list of lists).
    """
    try:
        # Handles NumPy arrays
        import numpy as np
        if isinstance(vertices, np.ndarray):
            return vertices.tolist()
    except Exception:
        pass

    # Already serializable
    return vertices

def run_pipeline_from_file(filename: str) -> Union[List[List[float]], Dict[str, List[List[float]]]]:
    """
    Execute a declarative pipeline defined in a JSON file.

    Supports:
    - Single output via "output_node"
    - Multiple outputs via "output_nodes"
    """
    with open(filename, "r") as f:
        pipeline = json.load(f)

    nodes_def = pipeline.get("nodes", [])
    connections = pipeline.get("connections", [])
    output_node = pipeline.get("output_node")
    output_nodes = pipeline.get("output_nodes", [])

    # Instantiate nodes with params
    instances: Dict[str, Any] = {}
    params_by_id: Dict[str, Dict[str, Any]] = {}
    for nd in nodes_def:
        node_type = nd["type"]
        node_id = nd["id"]
        node_params = nd.get("params", {})
        node_cls = NODE_MAP.get(node_type)
        if node_cls is None:
            raise ValueError(f"Unknown node type: {node_type}")
        instances[node_id] = node_cls(node_id, **node_params)
        params_by_id[node_id] = node_params

    # Evaluate primitives (no inputs)
    results: Dict[str, Any] = {}
    for node_id, node in instances.items():
        # Heuristic: primitives evaluate with empty context; modifiers expect input via connections
        # We treat NoiseNode as a modifier and skip until connections are processed
        if isinstance(node, NoiseNode):
            continue
        out = node.evaluate({})
        results[node_id] = _to_serializable(out)

    # Apply connections (feed source vertices into destination nodes)
    # The demo_pipeline used context keyed by node id: {dst_id: {"Vertices": src_vertices}}
    for conn in connections:
        src_id = conn["from"]
        dst_id = conn["to"]
        # Retrieve destination instance and its params
        dst_node = instances[dst_id]
        dst_params = params_by_id.get(dst_id, {})
        src_vertices = results.get(src_id)

        if src_vertices is None:
            raise ValueError(f"Source vertices for '{src_id}' not found before connecting to '{dst_id}'.")

        # Build context in the style your NoiseNode expects (from demo_pipeline)
        context = {
            dst_id: {
                conn["input"]: src_vertices  # typically "Vertices"
            }
        }

        # Evaluate destination node with its context
        out = dst_node.evaluate(context)
        results[dst_id] = _to_serializable(out)

    # Return outputs
    if output_node:
        if output_node not in results:
            raise ValueError(f"Output node '{output_node}' not found in results.")
        return results[output_node]

    if output_nodes:
        missing = [nid for nid in output_nodes if nid not in results]
        if missing:
            raise ValueError(f"Missing outputs for nodes: {missing}")
        # Return a dict keyed by node id
        return {nid: results[nid] for nid in output_nodes}

    # Fallback: if no output specified, return everything (not typical for portfolio)
    return results
