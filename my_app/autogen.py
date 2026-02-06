import os
import json
from typing import Dict, Any, List, Union
import numpy as np
# (Keep your node imports here...)

# (Keep your NODE_REGISTRY and helper functions here...)

def run_pipeline_from_file(filename: str) -> Union[List[List[float]], Dict[str, List[List[float]]]]:
    path = _root_path(filename)
    with open(path, "r") as f:
        pipeline = json.load(f)

    nodes_def = pipeline.get("nodes", [])
    connections = pipeline.get("connections", []) # List of {source_node, source_socket, target_node, target_socket}
    
    # 1. Instantiate Nodes
    instances: Dict[str, Node] = {}
    for n in nodes_def:
        nid = n["id"]
        ntype = n["type"]
        params = n.get("params", {})
        ctor = NODE_REGISTRY.get(ntype)
        if ctor is None:
            raise ValueError(f"Unknown node type '{ntype}'")
        instances[nid] = ctor(node_id=nid, **params)

    # 2. Build Dependency Graph (Who waits for whom?)
    # adjacency = { "target_node_id": ["source_node_id", "source_node_id"] }
    dependencies = {n["id"]: set() for n in nodes_def}
    
    # Map connections to node inputs
    # input_map = { "target_node_id": { "target_input_name": "source_node_id" } }
    input_map = {n["id"]: {} for n in nodes_def}

    for conn in connections:
        source_id = conn["source"]
        target_id = conn["target"]
        target_input = conn["target_input"] # e.g., "geometry" or "mask"
        
        dependencies[target_id].add(source_id)
        input_map[target_id][target_input] = source_id

    # 3. Topological Sort (The "Garden Logic")
    execution_order = []
    visited = set()
    temp_mark = set()

    def visit(nid):
        if nid in temp_mark:
            raise ValueError("Cycle detected! Nodes point to each other in a loop.")
        if nid not in visited:
            temp_mark.add(nid)
            for dependency in dependencies[nid]:
                visit(dependency)
            temp_mark.remove(nid)
            visited.add(nid)
            execution_order.append(nid)

    for nid in instances:
        visit(nid)
    
    # 4. Execute in Correct Order
    results: Dict[str, Any] = {}
    
    for nid in execution_order:
        node = instances[nid]
        
        # Inject inputs from previous nodes
        node_inputs = {}
        for input_name, source_nid in input_map[nid].items():
            # Pass the OUTPUT of the source node as the INPUT for this node
            node_inputs[input_name] = results[source_nid]
            
        # Update node params with dynamic inputs
        # (Assuming your Node class has a method to update inputs, or you pass them to evaluate)
       results[nid] = node.evaluate(node_inputs) 

    # (Return logic remains the same)
    output_node = pipeline.get("output_node")
    if output_node:
        return _to_json_safe(results[output_node])
    return _to_json_safe(results[list(results.keys())[-1]])

