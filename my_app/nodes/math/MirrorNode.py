from nodes.node_base import Node
import numpy as np
from typing import Dict, List

class MirrorNode(Node):
    """
    Mirror vertices across a chosen axis (x, y, or z).
    """
    def __init__(self, node_id: str, axis: str = "x"):
        super().__init__(node_id)
        self.axis = axis.lower()
        self.outputs["Axis"] = self.axis

    def evaluate(self, graph_data: Dict) -> List[List[float]]:
        if not graph_data:
            return []
        last = list(graph_data.values())[-1]
        mirrored = np.array(last, dtype=np.float32).copy()
        if self.axis == "x":
            mirrored[:,0] *= -1
        elif self.axis == "y":
            mirrored[:,1] *= -1
        elif self.axis == "z":
            mirrored[:,2] *= -1
        return mirrored.tolist()
