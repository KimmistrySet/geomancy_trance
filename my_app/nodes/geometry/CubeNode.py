import numpy as np
from core.node_base import Node

class CubeNode(Node):
    """
    Generates a unit cube mesh (8 vertices).
    """
    def __init__(self, node_id: str):
        super().__init__(node_id, "Cube")
        self.outputs['Vertices'] = None

    def evaluate(self, graph_data: dict) -> list[list[float]]:
        vertices = [
            [-0.5, -0.5, -0.5],
            [ 0.5, -0.5, -0.5],
            [ 0.5,  0.5, -0.5],
            [-0.5,  0.5, -0.5],
            [-0.5, -0.5,  0.5],
            [ 0.5, -0.5,  0.5],
            [ 0.5,  0.5,  0.5],
            [-0.5,  0.5,  0.5],
        ]
        self.outputs['Vertices'] = vertices
        return vertices
