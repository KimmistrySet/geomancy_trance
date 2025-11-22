from nodes.node_base import Node
import numpy as np
from typing import Dict, List

class RotateNode(Node):
    """
    Rotate vertices around x, y, or z axis by angle (radians).
    """
    def __init__(self, node_id: str, axis: str = "z", angle: float = 0.0):
        super().__init__(node_id)
        self.axis = axis.lower()
        self.angle = angle
        self.outputs["Rotation"] = {"axis": axis, "angle": angle}

    def evaluate(self, graph_data: Dict) -> List[List[float]]:
        if not graph_data:
            return []
        last = np.array(list(graph_data.values())[-1], dtype=np.float32)

        c, s = np.cos(self.angle), np.sin(self.angle)
        if self.axis == "x":
            R = np.array([[1, 0, 0],[0, c, -s],[0, s, c]], dtype=np.float32)
        elif self.axis == "y":
            R = np.array([[c, 0, s],[0, 1, 0],[-s, 0, c]], dtype=np.float32)
        else:
            R = np.array([[c, -s, 0],[s, c, 0],[0, 0, 1]], dtype=np.float32)
        return (last @ R.T).tolist()
