# autogen.py
import os
import json
from typing import Dict, Any, List, Union, Callable, Set
import numpy as np

# --- Package-local imports (adjust these to match your repo) ---
# Base class and concrete node modules should exist under nodes/
from nodes.node_base import Node
from nodes.geometry.cube import CubeNode   # example
from nodes.geometry.sphere import SphereNode  # example
from nodes.math.noise import NoiseNode     # example
# Add or remove imports to reflect your actual nodes

# --- Node registry: map JSON "type" to constructor ---
NODE_REGISTRY: Dict[str, Callable[..., Node]] = {
    "CubeNode": CubeNode,
    "SphereNode": SphereNode,
    "NoiseNode": NoiseNode,
    # Register all supported nodes here
}

def _root_path(*parts: str) -> str:
    """Resolve file path relative to this file, not the working dir."""
    return os.path.join(os.path.dirname(__file__), *parts)

def _to_json_safe(x: Any) -> Any:
    """Convert common numeric containers to JSON-serializable structures."""
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (set, tuple)):
        return list(x)
    # Allow nested containers
    if isinstance(x, dict):
        return {k: _to_json_safe(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_to_json_safe(v) for v in x]
    # Scalars pass through
    return x

def _build_graph(nodes_def: List[Dict[str, Any]],
                 connections: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Create node instances and adjacency for execution.
    nodes_def: [{"id": "cube1", "type": "CubeNode", "params": {...}}, ...]
    connections: [{"from": "cube1", "to": "noise1"}, ...]
    """
    instances: Dict[str, Node] = {}
    indegree: Dict[str, int] = {}
    outgoing: Dict[str, List[str]] = {}

    # Instantiate all nodes
    for n in nodes_def:
        nid = n["id"]
        ntype = n["type"]
        params = n.get("params", {})
        ctor = NODE_REGISTRY.get(ntype)
        if ctor is None:
            raise ValueError(f"Unknown node type '{ntype}' for node '{nid}'")
        instances[nid] = ctor(node_id=nid, **params)
        indegree[nid] = 0
        outgoing[nid] = []

    # Wire connections
    for c in connections:
        src = c["from"]
        dst = c["to"]
        if src not in instances or dst not in instances:
            raise ValueError(f"Connection references unknown node: {src} -> {dst}")
        outgoing[src].append(dst)
        indegree[dst] += 1

    return {"instances": instances, "indegree": indegree, "outgoing": outgoing}

def _toposort(indegree: Dict[str, int],
              outgoing: Dict[str, List[str]]) -> List[str]:
    """Kahn's algorithm for topological order."""
    order: List[str] = []
    queue: List[str] = [nid for nid, deg in indegree.items() if deg == 0]
    i = 0
    while i < len(queue):
        nid = queue[i]; i += 1
        order.append(nid)
        for nxt in outgoing[nid]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    if len(order) != len(indegree):
        raise RuntimeError("Cycle detected in pipeline graph")
    return order

def _execute(instances: Dict[str, Node],
             order: List[str]) -> Dict[str, Any]:
    """
    Evaluate nodes in topological order.
    Each node receives a context dict with previous results it depends on.
    Convention: nodes read what they need from context; they must not have side effects.
    """
    results: Dict[str, Any] = {}
    for nid in order:
        node = instances[nid]
        # Provide full results as context; nodes can choose what to use
        out = node.evaluate(context=results)
        results[nid] = out
    return results

def run_pipeline_from_file(filename: str) -> Union[List[List[float]], Dict[str, List[List[float]]]]:
    """
    Execute a declarative pipeline defined in a JSON file (root-level by default).

    JSON schema:
    {
      "nodes": [
        {"id": "cube1", "type": "CubeNode", "params": {"size": 1}}
      ],
      "connections": [
        {"from": "cube1", "to": "noise1"}
      ],
      "output_node": "cube1"              # OR
      "output_nodes": ["cube1", "noise1"]
    }
    """
    path = _root_path(filename)
    try:
        with open(path, "r") as f:
            pipeline = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load pipeline file '{filename}': {e}")

    nodes_def = pipeline.get("nodes", [])
    connections = pipeline.get("connections", [])
    output_node = pipeline.get("output_node")
    output_nodes = pipeline.get("output_nodes", [])

    if not nodes_def:
        raise ValueError("Pipeline has no 'nodes'")
    if not isinstance(connections, list):
        raise ValueError("'connections' must be a list")

    graph = _build_graph(nodes_def, connections)
    order = _toposort(graph["indegree"], graph["outgoing"])
    results = _execute(graph["instances"], order)

    # Single output
    if output_node:
        if output_node not in results:
            raise ValueError(f"Requested output_node '{output_node}' not found")
        return _to_json_safe(results[output_node])

    # Multiple outputs
    if output_nodes:
        payload: Dict[str, Any] = {}
        for nid in output_nodes:
            if nid not in results:
                raise ValueError(f"Requested output node '{nid}' not found")
            payload[nid] = _to_json_safe(results[nid])
        return payload  # jsonify will handle dict

    # Fallback: return the last node's output
    last = order[-1]
    return _to_json_safe(results[last])
