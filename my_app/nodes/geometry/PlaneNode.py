from nodes.node_base import Node
import numpy as np

class PlaneNode(Node):
    """
    Generates a grid of points on the XY plane centered at origin.
    """
    def __init__(self, node_id: str, width: float = 1.0, height: float = 1.0, divisions: int = 10):
        super().__init__(node_id)
        self.width = float(width)
        self.height = float(height)
        self.divisions = int(divisions)
        self.outputs["Vertices"] = None

    def evaluate(self, context):
        xs = np.linspace(-self.width/2.0, self.width/2.0, self.divisions, dtype=np.float32)
        ys = np.linspace(-self.height/2.0, self.height/2.0, self.divisions, dtype=np.float32)
        X, Y = np.meshgrid(xs, ys, indexing="xy")
        verts = np.column_stack([X.flatten(), Y.flatten(), np.zeros(X.size, dtype=np.float32)])
        self.outputs["Vertices"] = verts.tolist()
        return self.outputs["Vertices"]
