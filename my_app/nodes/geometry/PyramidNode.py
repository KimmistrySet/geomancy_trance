from nodes.node_base import Node
import numpy as np

class PyramidNode(Node):
    def __init__(self, node_id: str, base: float = 1.0, height: float = 1.0):
        super().__init__(node_id)
        self.base, self.height = base, height

    def evaluate(self, context):
        half = self.base / 2.0
        base_vertices = np.array([
            [-half, -half, 0],
            [ half, -half, 0],
            [ half,  half, 0],
            [-half,  half, 0]
        ])
        apex = np.array([[0, 0, self.height]])
        return np.vstack([base_vertices, apex])
