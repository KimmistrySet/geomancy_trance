from nodes.node_base import Node
import numpy as np
from typing import Dict, List

class VectorMatrixMultiplyNode(Node):
    """
    Multiplies a 4x4 Matrix by a 3D Vector (homogeneous).
    """
    def __init__(self, node_id: str):
        super().__init__(node_id)
        self.inputs["Matrix"] = None
        self.inputs["Vector3"] = None
        self.outputs["ResultVector4"] = None

    def evaluate(self, graph_data: Dict) -> List[float]:
        from nodes.execution_engine import resolve_input
        matrix_list = resolve_input(self.node_id, "Matrix", graph_data)
        vector_list = resolve_input(self.node_id, "Vector3", graph_data)
        matrix = np.array(matrix_list, dtype=np.float32)
        homogeneous_vector = np.append(np.array(vector_list, dtype=np.float32), 1.0)
        result = matrix @ homogeneous_vector
        self.outputs["ResultVector4"] = result.tolist()
        return self.outputs["ResultVector4"]
