import numpy as np
from core.node_base import Node

class Matrix4x4Node(Node):
    """
    Represents a 4x4 Homogeneous Transformation Matrix.
    Used for translating, rotating, and scaling objects.
    """
    def __init__(self, node_id: str, values=None):
        super().__init__(node_id, "Matrix4x4")
        if values is None or len(values) != 16:
            self.matrix = np.identity(4, dtype=np.float32)
        else:
            self.matrix = np.array(values, dtype=np.float32).reshape((4, 4))
        self.outputs['Matrix'] = self.matrix.tolist()

    def evaluate(self, graph_data: dict) -> list[list[float]]:
        return self.matrix.tolist()
