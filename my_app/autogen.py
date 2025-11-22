# autogen.py
import os
import json
from typing import Dict, Any, List, Union
import numpy as np

# --- Node imports based on your folder structure ---
from nodes.node_base import Node

# Geometry nodes
from nodes.geometry.CubeNode import CubeNode
from nodes.geometry.CylinderNode import CylinderNode
from nodes.geometry.SphereNode import SphereNode
from nodes.geometry.PyramidNode import PyramidNode
from nodes.geometry.NoiseNode import NoiseNode
from nodes.geometry.TerrainNode import TerrainNode
from nodes.geometry.ConeNode import ConeNode
from nodes.geometry.TorusNode import TorusNode
from nodes.geometry.PlaneNode import PlaneNode
from nodes.geometry.ScatterNode import ScatterNode
from nodes.geometry.GridNode import GridNode

# Math nodes
from nodes.math.Matrix4x4Node import Matrix4x4Node
from nodes.math.MatrixMultiplyNode import MatrixMultiplyNode
from nodes.math.VectorMatrixNode import VectorMatrixMultiplyNode
from nodes.math.TransformNode import TransformNode
from nodes.math.ScaleNode import ScaleNode
from nodes.math.RotateNode import RotateNode
from nodes.math.TranslateNode import TranslateNode
from nodes.math.MirrorNode import MirrorNode
# Add more math nodes here as needed

# --- Registry mapping JSON "type" strings to actual classes ---
NODE_REGISTRY: Dict[str, Any] = {
    "CubeNode": CubeNode,
    "CylinderNode": CylinderNode,
    "SphereNode": SphereNode,
    "NoiseNode": NoiseNode,
    "PyramidNode": PyramidNode,
    "TerrainNode": TerrainNode,
    "ConeNode": ConeNode,
    "TorusNode": TorusNode,
    "PlaneNode": PlaneNode,
    "ScatterNode": ScatterNode,
    "GridNode": GridNode,
    "Matrix4x4Node": Matrix4x4Node,
    "MatrixMultiplyNode": MatrixMultiplyNode,
    "VectorMatrixMultiplyNode": VectorMatrixMultiplyNode,
    "TransformNode": TransformNode,
    "ScaleNode": ScaleNode,
    "RotateNode": RotateNode,
    "TranslateNode": TranslateNode,
    "MirrorNode": MirrorNode,
    # Add other node types here
}

def _root_path(filename: str) -> str:
    """Resolve file path relative to this file."""
    return os.path.join(os.path.dirname(__file__), filename)

def _to_json_safe(x: Any) -> Any:
    """Convert outputs to JSON-serializable structures."""
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (set, tuple)):
        return list(x)
    if isinstance(x, dict):
        return {k: _to_json_safe(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_to_json_safe(v) for v in x]
    return x

def run_pipeline_from_file(filename: str) -> Union[List[List[float]], Dict[str, List[List[float]]]]:
    """
    Execute a declarative pipeline defined in a JSON file.
    Supports single output via "output_node" or multiple via "output_nodes".
    """
    path = _root_path(filename)
    with open(path, "r") as f:
        pipeline = json.load(f)

    nodes_def = pipeline.get("nodes", [])
    connections = pipeline.get("connections", [])
    output_node = pipeline.get("output_node")
    output_nodes = pipeline.get("output_nodes", [])

    # Build node instances
    instances: Dict[str, Node] = {}
    for n in nodes_def:
        nid = n["id"]
        ntype = n["type"]
        params = n.get("params", {})
        ctor = NODE_REGISTRY.get(ntype)
        if ctor is None:
            raise ValueError(f"Unknown node type '{ntype}' for node '{nid}'")
        instances[nid] = ctor(node_id=nid, **params)

    # Execute nodes in declared order (simplified)
    results: Dict[str, Any] = {}
    for nid, node in instances.items():
        results[nid] = node.evaluate(context=results)

    # Return outputs
    if output_node:
        return _to_json_safe(results[output_node])
    if output_nodes:
        return {nid: _to_json_safe(results[nid]) for nid in output_nodes}
    last = list(results.keys())[-1]
    return _to_json_safe(results[last])