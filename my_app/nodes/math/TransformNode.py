from nodes.node_base import Node
import numpy as np

class TransformNode(Node):
    def __init__(self, node_id: str, matrix=None):
        """
        Apply a custom 3x3 transformation matrix to the last vertex set.
        """
        super().__init__(node_id)
        self.matrix = np.array(matrix) if matrix is not None else np.eye(3)

    def evaluate(self, context):
        if not context:
            return []
        last = list(context.values())[-1]
        return np.dot(last, self.matrix.T)
