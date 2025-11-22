import numpy as np
from nodes.node_base import Node



class MatrixMultiplyNode(Node):
    """
    Multiplies Matrix A by Matrix B (A * B).
    Crucial for concatenating transformations.
    """
    def __init__(self, node_id: str):
        super().__init__(node_id, "MatrixMultiply")
        self.inputs['Matrix A'] = None
        self.inputs['Matrix B'] = None
        self.outputs['ResultMatrix'] = None

    def evaluate(self, graph_data: dict) -> list[list[float]]:
        matrix_a_list = resolve_input(self.id, 'Matrix A', graph_data)
        matrix_b_list = resolve_input(self.id, 'Matrix B', graph_data)

        matrix_a = np.array(matrix_a_list, dtype=np.float32)
        matrix_b = np.array(matrix_b_list, dtype=np.float32)

        if matrix_a.shape != (4, 4) or matrix_b.shape != (4, 4):
            raise ValueError("Inputs must be 4x4 matrices.")

        result_matrix = matrix_a @ matrix_b
        self.outputs['ResultMatrix'] = result_matrix.tolist()
        return result_matrix.tolist()
