import os
import json
from typing import Dict, Any, List, Union
import numpy as np

# --- 1. CONFIGURATION & IMPORTS ---
# Adjust these imports if your folder structure is slightly different
from nodes.node_base import Node
# Geometry
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
# Math / Modifiers
from nodes.math.Matrix4x4Node import Matrix4x4Node
from nodes.math.MatrixMultiplyNode import MatrixMultiplyNode
from nodes.math.VectorMatrixNode import VectorMatrixMultiplyNode
from nodes.math.TransformNode import TransformNode
from nodes.math.ScaleNode import ScaleNode
from nodes.math.RotateNode import RotateNode
from nodes.math.TranslaterNode import TranslaterNode
from nodes.math.MirrorNode import MirrorNode

NODE_REGISTRY = {
    "CubeNode": CubeNode, "CylinderNode": CylinderNode, "SphereNode": SphereNode,
    "NoiseNode": NoiseNode, "PyramidNode": PyramidNode, "TerrainNode": TerrainNode,
    "ConeNode": ConeNode, "TorusNode": TorusNode, "PlaneNode": PlaneNode,
    "ScatterNode": ScatterNode, "GridNode": GridNode, "Matrix4x4Node": Matrix4x4Node,
    "MatrixMultiplyNode": MatrixMultiplyNode, "VectorMatrixMultiplyNode": VectorMatrixMultiplyNode,
    "TransformNode": TransformNode, "ScaleNode": ScaleNode, "RotateNode": RotateNode,
    "TranslaterNode": TranslaterNode, "MirrorNode": MirrorNode,
}

def _root_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)

def _to_json_safe(x: Any) -> Any:
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, (set, tuple)): return list(x)
    if isinstance(x, dict): return {k: _to_json_safe(v) for k, v in x.items()}
    if isinstance(x, list): return [_to_json_safe(v) for v in x]
    return x

def run_pipeline_from_file(filename: str):
    path = _root_path(filename)
    with open(path, "r") as f:
        pipeline = json.load(f)

    nodes_def = pipeline.get("nodes", [])
    connections = pipeline.get("connections", [])

    # --- 2. INSTANTIATE NODES ---
    instances = {}
    for n in nodes_def:
        nid, ntype = n["id"], n["type"]
        params = n.get("params", {})
        ctor = NODE_REGISTRY.get(ntype)
        if ctor: 
            instances[nid] = ctor(node_id=nid, **params)
        else:
            print(f"Warning: Unknown node type {ntype}")

    # --- 3. BUILD DEPENDENCY GRAPH ---
    dependencies = {n["id"]: set() for n in nodes_def}
    input_map = {n["id"]: {} for n in nodes_def}

    for conn in connections:
        # SUPPORT BOTH formats: "from/to" (JSON) and "source/target" (Old Code)
        source_id = conn.get("from") or conn.get("source")
        target_id = conn.get("to") or conn.get("target")
        
        # Default input name if missing
        target_input = conn.get("input") or conn.get("target_input") or "geometry"
        
        if source_id and target_id:
            dependencies[target_id].add(source_id)
            input_map[target_id][target_input] = source_id

    # --- 4. TOPOLOGICAL SORT (Execution Order) ---
    execution_order = []
    visited, temp_mark = set(), set()
    
    def visit(nid):
        if nid in temp_mark: raise ValueError(f"Cycle detected in {nid}")
        if nid not in visited:
            temp_mark.add(nid)
            for dep in dependencies[nid]: visit(dep)
            temp_mark.remove(nid)
            visited.add(nid)
            execution_order.append(nid)
            
    for nid in instances: visit(nid)
    
    # --- 5. EXECUTION LOOP ---
    results = {}
    for nid in execution_order:
        node = instances[nid]
        
        # Gather inputs from finished parents
        node_inputs = {}
        for input_name, source_nid in input_map[nid].items():
            if source_nid in results:
                node_inputs[input_name] = results[source_nid]
        
        # RUN THE NODE
        # We pass as positional arg so it works with both 'context' and 'inputs' signatures
        try:
            results[nid] = node.evaluate(node_inputs)
        except Exception as e:
            print(f"Error executing {nid}: {e}")
            results[nid] = []

    # --- 6. RETURN OUTPUTS (The Critical Fix) ---
    
    # Check for PLURAL outputs first (e.g. ["translate1", "mirror1"])
    output_nodes = pipeline.get("output_nodes")
    if output_nodes:
        combined_list = []
        for nid in output_nodes:
            data = results.get(nid, [])
            # Flatten lists if necessary to merge geometry
            if isinstance(data, list):
                combined_list.extend(data)
            else:
                combined_list.append(data)
        return _to_json_safe(combined_list)

    # Check for SINGULAR output
    output_node = pipeline.get("output_node")
    if output_node: 
        return _to_json_safe(results.get(output_node, []))
        
    # Fallback: Return the last calculated node
    if results:
        return _to_json_safe(results[list(results.keys())[-1]])
        
    return []
