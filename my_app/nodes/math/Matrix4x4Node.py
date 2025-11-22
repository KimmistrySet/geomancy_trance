from nodes.node_base import Node
import numpy as np
from typing import Optional, List, Dict

class Matrix4x4Node(Node):
    """
    Represents a 4x4 Homogeneous Transformation Matrix.
    """
    def __init__(self, node_id: str, values: Optional[List[float]] = None):
        super().__init__(node_id)
        if values is None or len(values) != 16:
            self.matrix = np.identity(4, dtype=np.float32)
        else:
            self.matrix = np.array(values, dtype=np.float32).reshape((4, 4))
        self.outputs["Matrix"] = self.matrix.tolist()

    def evaluate(self, graph_data: Dict) -> List[List[float]]:
        return self.matrix.tolist()
