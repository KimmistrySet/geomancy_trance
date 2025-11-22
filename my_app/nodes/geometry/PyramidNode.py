from nodes.node_base import Node
import numpy as np

class PyramidNode(Node):
    """
    Generates a square-based pyramid (4 base vertices + apex).
    """
    def __init__(self, node_id: str, base: float = 1.0, height: float = 1.0):
        super().__init__(node_id)
        self.base = float(base)
        self.height = float(height)
        self.outputs["Vertices"] = None

    def evaluate(self, context):
        half = self.base / 2.0
        base_vertices = np.array([
            [-half, -half, 0.0],
            [ half, -half, 0.0],
            [ half,  half, 0.0],
            [-half,  half, 0.0]
        ], dtype=np.float32)
        apex = np.array([[0.0, 0.0, self.height]], dtype=np.float32)
        verts = np.vstack([base_vertices, apex])
        self.outputs["Vertices"] = verts.tolist()
        return self.outputs["Vertices"]
