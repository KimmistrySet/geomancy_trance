from nodes.node_base import Node
import numpy as np
from typing import Dict, List, Any

class RotateNode(Node):
    """
    Rotate vertices around x, y, or z axis by angle (radians).
    """
    def __init__(self, node_id: str, axis: str = "z", angle: float = 0.0):
        super().__init__(node_id)
        self.axis = axis.lower()
        self.angle = angle
        self.outputs["Rotation"] = {"axis": axis, "angle": angle}

    def evaluate(self, inputs: Dict[str, Any]) -> List[List[float]]:
        # 1. Input Validation
        if not inputs:
            return []

        # 2. Collect ALL incoming geometry
        all_vertices = []
        for input_data in inputs.values():
            if isinstance(input_data, list):
                all_vertices.extend(input_data)
        
        if not all_vertices:
            return []

        # 3. Convert to Numpy
        vertices = np.array(all_vertices, dtype=np.float32)

        # 4. Build Rotation Matrix
        c, s = np.cos(self.angle), np.sin(self.angle)
        
        if self.axis == "x":
            R = np.array([[1, 0, 0],
                          [0, c, -s],
                          [0, s, c]], dtype=np.float32)
        elif self.axis == "y":
            R = np.array([[c, 0, s],
                          [0, 1, 0],
                          [-s, 0, c]], dtype=np.float32)
        else: # Default to Z
            R = np.array([[c, -s, 0],
                          [s, c, 0],
                          [0, 0, 1]], dtype=np.float32)

        # 5. Apply Rotation (Matrix Multiplication)
        # We use @ for matrix multiplication and R.T (transpose) because 
        # our points are rows [x, y, z]
        return (vertices @ R.T).tolist()
