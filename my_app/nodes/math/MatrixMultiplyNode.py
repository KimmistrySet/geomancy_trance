from nodes.node_base import Node
import numpy as np
from typing import Dict, List

class MatrixMultiplyNode(Node):
    """
    Multiplies Matrix A by Matrix B (A * B).
    Crucial for concatenating transformations (e.g., Model Matrix * View Matrix).
    """
    def __init__(self, node_id: str):
        super().__init__(node_id)
        self.inputs['Matrix A'] = None
        self.inputs['Matrix B'] = None
        self.outputs['ResultMatrix'] = None

    def evaluate(self, graph_data: Dict) -> List[List[float]]:
        from nodes.execution_engine import resolve_input
        
        matrix_a_list = resolve_input(self.node_id, 'Matrix A', graph_data)
        matrix_b_list = resolve_input(self.node_id, 'Matrix B', graph_data)

        if not isinstance(matrix_a_list, list) or not isinstance(matrix_b_list, list):
            raise ValueError("Matrix inputs must be 4x4 lists of lists.")

        matrix_a = np.array(matrix_a_list, dtype=np.float32)
        matrix_b = np.array(matrix_b_list, dtype=np.float32)

        if matrix_a.shape != (4, 4) or matrix_b.shape != (4, 4):
            raise ValueError("Inputs must be 4x4 matrices.")

        result_matrix = matrix_a @ matrix_b
        return result_matrix.tolist()
