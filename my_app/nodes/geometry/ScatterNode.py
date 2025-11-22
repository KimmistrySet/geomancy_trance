from nodes.node_base import Node
import numpy as np

class ScatterNode(Node):
    """
    Generates random points within a box centered at origin.
    """
    def __init__(self, node_id: str, count: int = 100, range_x: float = 5.0, range_y: float = 5.0, range_z: float = 5.0, seed: int = None):
        super().__init__(node_id)
        self.count = int(count)
        self.rx = float(range_x)
        self.ry = float(range_y)
        self.rz = float(range_z)
        self.seed = seed
        self.outputs["Vertices"] = None

    def evaluate(self, context):
        if self.seed is not None:
            np.random.seed(int(self.seed))
        pts = np.random.rand(self.count, 3).astype(np.float32)
        pts[:, 0] = (pts[:, 0] - 0.5) * self.rx
        pts[:, 1] = (pts[:, 1] - 0.5) * self.ry
        pts[:, 2] = (pts[:, 2] - 0.5) * self.rz
        self.outputs["Vertices"] = pts.tolist()
        return self.outputs["Vertices"]
