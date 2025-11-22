from nodes.node_base import Node
import numpy as np

class GridNode(Node):
    """
    Generates a rectangular grid on XY plane with given spacing.
    """
    def __init__(self, node_id: str, nx: int = 5, ny: int = 5, spacing: float = 1.0):
        super().__init__(node_id)
        self.nx = int(nx)
        self.ny = int(ny)
        self.spacing = float(spacing)
        self.outputs["Vertices"] = None

    def evaluate(self, context):
        xs = np.arange(self.nx, dtype=np.float32) * self.spacing
        ys = np.arange(self.ny, dtype=np.float32) * self.spacing
        X, Y = np.meshgrid(xs, ys, indexing="xy")
        verts = np.column_stack([X.flatten(), Y.flatten(), np.zeros(X.size, dtype=np.float32)])
        self.outputs["Vertices"] = verts.tolist()
        return self.outputs["Vertices"]
