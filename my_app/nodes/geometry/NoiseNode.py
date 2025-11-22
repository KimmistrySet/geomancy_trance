from nodes.node_base import Node
import numpy as np

class NoiseNode(Node):
    """
    Generates Gaussian noise points in 3D.
    """
    def __init__(self, node_id: str, count: int = 100, scale: float = 1.0, seed: int = None):
        super().__init__(node_id)
        self.count = int(count)
        self.scale = float(scale)
        self.seed = seed
        self.outputs["Vertices"] = None

    def evaluate(self, context):
        if self.seed is not None:
            np.random.seed(int(self.seed))
        pts = np.random.randn(self.count, 3).astype(np.float32) * self.scale
        self.outputs["Vertices"] = pts.tolist()
        return self.outputs["Vertices"]
