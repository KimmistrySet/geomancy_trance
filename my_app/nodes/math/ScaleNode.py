from nodes.node_base import Node
import numpy as np

class ScaleNode(Node):
    def __init__(self, node_id: str, sx: float = 1.0, sy: float = 1.0, sz: float = 1.0):
        """
        Scale vertices along x, y, z axes.
        """
        super().__init__(node_id)
        self.sx, self.sy, self.sz = sx, sy, sz

    def evaluate(self, context):
        if not context:
            return []
        last = list(context.values())[-1]
        scale = np.diag([self.sx, self.sy, self.sz])
        return np.dot(last, scale.T)
