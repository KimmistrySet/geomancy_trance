from nodes.node_base import Node
import numpy as np
from typing import Dict, List

class ScaleNode(Node):
    """
    Scale vertices along x, y, z axes.
    """
    def __init__(self, node_id: str, sx: float = 1.0, sy: float = 1.0, sz: float = 1.0):
        super().__init__(node_id)
        self.sx, self.sy, self.sz = sx, sy, sz
        self.outputs["Scale"] = [sx, sy, sz]

    def evaluate(self, graph_data: Dict) -> List[List[float]]:
        if not graph_data:
            return []
        last = list(graph_data.values())[-1]
        scale = np.diag([self.sx, self.sy, self.sz])
        return np.dot(last, scale.T).tolist()
