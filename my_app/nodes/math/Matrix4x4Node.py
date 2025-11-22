from nodes.node_base import Node
import numpy as np
from typing import Optional, List, Dict

class Matrix4x4Node(Node):
    """
    Represents a 4x4 Homogeneous Transformation Matrix.
    Used for translating, rotating, and scaling objects.
    """
    def __init__(self, node_id: str, values: Optional[List[float]] = None):
        super().__init__(node_id)
        
        # Initialize as identity if no values provided
        if values is None or len(values) != 16:
            self.matrix = np.identity(4, dtype=np.float32)
        else:
            self.matrix = np.array(values, dtype=np.float32).reshape((4, 4))
            
        self.outputs['Matrix'] = self.matrix.tolist()

    def evaluate(self, graph_data: Dict) -> List[List[float]]:
        """Returns the 4x4 matrix as a list of lists."""
        return self.matrix.tolist()
        