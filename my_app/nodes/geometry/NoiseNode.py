from nodes.node_base import Node
import numpy as np

class NoiseNode(Node):
    def __init__(self, node_id: str, count: int = 50, scale: float = 1.0, seed: int = None):
        """
        NoiseNode generates a set of random 3D points.
        - node_id: unique identifier
        - count: number of points to generate
        - scale: multiplier for noise amplitude
        - seed: optional random seed for reproducibility
        """
        super().__init__(node_id)
        self.count = count
        self.scale = scale
        self.seed = seed

    def evaluate(self, context):
        if self.seed is not None:
            np.random.seed(self.seed)
        pts = np.random.randn(self.count, 3) * self.scale
        return pts
