from nodes.node_base import Node
import numpy as np
from typing import Dict, List, Any

class TransformNode(Node):
    """
    Apply a custom 3x3 transformation matrix to the vertex set.
    """
    def __init__(self, node_id: str, matrix: List[List[float]] = None):
        super().__init__(node_id)
        # Default to Identity Matrix if none provided
        self.matrix = np.array(matrix, dtype=np.float32) if matrix is not None else np.eye(3, dtype=np.float32)
        self.outputs["Matrix"] = self.matrix.tolist()

    def evaluate(self, inputs: Dict[str, Any]) -> List[List[float]]:
        # 1. Input Validation
        if not inputs:
            return []

        # 2. Collect ALL incoming geometry from connected nodes
        all_vertices = []
        for input_data in inputs.values():
            if isinstance(input_data, list):
                all_vertices.extend(input_data)
        
        if not all_vertices:
            return []

        # 3. Convert to Numpy
        vertices = np.array(all_vertices, dtype=np.float32)

        # 4. Apply Matrix Multiplication
        # vertices (N,3) @ matrix.T (3,3) -> (N,3)
        return (vertices @ self.matrix.T).tolist()
