import numpy as np
from core.node_base import Node
from core.execution_engine import resolve_input

class VectorMatrixMultiplyNode(Node):
    """
    Multiplies a 4x4 Matrix by a 3D Vector (M * V).
    Vector is treated as homogeneous [x, y, z, 1].
    """
    def __init__(self, node_id: str):
        super().__init__(node_id, "VectorMatrixMultiply")
        self.inputs['Matrix'] = None
        self.inputs['Vector3'] = None
        self.outputs['ResultVector4'] = None

    def evaluate(self, graph_data: dict) -> list[float]:
        matrix_list = resolve_input(self.id, 'Matrix', graph_data)
        vector_list = resolve_input(self.id, 'Vector3', graph_data)

        if len(vector_list) != 3:
            raise ValueError("Vector must be 3 components.")

        matrix = np.array(matrix_list, dtype=np.float32)
        homogeneous_vector = np.append(np.array(vector_list, dtype=np.float32), 1.0)

        result_vector = matrix @ homogeneous_vector
        self.outputs['ResultVector4'] = result_vector.tolist()
        return result_vector.tolist()
