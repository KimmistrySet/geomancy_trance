from nodes.node_base import Node
import numpy as np
from typing import Dict, List, Any

class VectorMatrixMultiplyNode(Node):
    """
    Multiplies a 4x4 Matrix by a 3D Vector (homogeneous).
    """
    def __init__(self, node_id: str):
        super().__init__(node_id)
        # These keys must match the "target_input" in your JSON connections
        self.inputs["Matrix"] = None
        self.inputs["Vector3"] = None
        self.outputs["ResultVector4"] = None

    def evaluate(self, inputs: Dict[str, Any]) -> List[float]:
        # 1. Retrieve Pre-Resolved Inputs
        # The new autogen.py has already put the data into the 'inputs' dict for us.
        matrix_list = inputs.get("Matrix")
        vector_list = inputs.get("Vector3")

        if matrix_list is None or vector_list is None:
            # Return origin or raise error if inputs are missing
            return [0.0, 0.0, 0.0, 1.0]

        # 2. Math
        matrix = np.array(matrix_list, dtype=np.float32)
        
        # Convert 3D vector [x, y, z] to 4D homogeneous [x, y, z, 1.0]
        # This allows translation matrices to work correctly
        vector_np = np.array(vector_list, dtype=np.float32)
        if vector_np.shape[0] == 3:
            homogeneous_vector = np.append(vector_np, 1.0)
        else:
            homogeneous_vector = vector_np # It's already 4D

        # 3. Multiply
        result = matrix @ homogeneous_vector
        
        self.outputs["ResultVector4"] = result.tolist()
        return self.outputs["ResultVector4"]
