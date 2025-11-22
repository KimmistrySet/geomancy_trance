from nodes.node_base import Node
import numpy as np
from typing import Dict, List

class TransformNode(Node):
    """
    Apply a custom 3x3 transformation matrix to the last vertex set.
    """
    def __init__(self, node_id: str, matrix: List[List[float]] = None):
        super().__init__(node_id)
        self.matrix = np.array(matrix, dtype=np.float32) if matrix is not None else np.eye(3, dtype=np.float32)
        self.outputs["Matrix"] = self.matrix.tolist()

    def evaluate(self, graph_data: Dict) -> List[List[float]]:
        if not graph_data:
            return []
        last = list(graph_data.values())[-1]
        return np.dot(last, self.matrix.T).tolist()
