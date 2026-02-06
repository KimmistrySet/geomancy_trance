from nodes.node_base import Node
import numpy as np
from typing import Dict, List, Any

class ScaleNode(Node):
    """
    Scale vertices along x, y, z axes.
    """
    def __init__(self, node_id: str, sx: float = 1.0, sy: float = 1.0, sz: float = 1.0):
        super().__init__(node_id)
        self.sx, self.sy, self.sz = sx, sy, sz
        self.outputs["Scale"] = [sx, sy, sz]

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

        # 4. Create Scale Matrix
        # Using a diagonal matrix is cleaner than standard multiplication here
        scale_matrix = np.diag([self.sx, self.sy, self.sz]).astype(np.float32)
        
        # 5. Apply Scale (Matrix Multiplication)
        return (vertices @ scale_matrix).tolist()
