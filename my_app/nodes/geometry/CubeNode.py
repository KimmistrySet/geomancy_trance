from nodes.node_base import Node
import numpy as np

class CubeNode(Node):
    def __init__(self, node_id: str, width: float = 1.0, height: float = 1.0, depth: float = 1.0, size: float = None):
        super().__init__(node_id)
        if size is not None:
            width = height = depth = size
        self.width, self.height, self.depth = width, height, depth

    def evaluate(self, context):
        w, h, d = self.width / 2, self.height / 2, self.depth / 2
        return np.array([
            [-w, -h, -d], [ w, -h, -d], [ w,  h, -d], [-w,  h, -d],
            [-w, -h,  d], [ w, -h,  d], [ w,  h,  d], [-w,  h,  d],
        ])
