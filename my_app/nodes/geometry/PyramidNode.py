from nodes.node_base import Node


class PyramidNode(Node):
    """
    Generates a simple pyramid mesh (square base + apex).
    """
    def __init__(self, node_id: str, height: float = 1.0):
        super().__init__(node_id, "Pyramid")
        self.height = height
        self.outputs['Vertices'] = None

    def evaluate(self, graph_data: dict) -> list[list[float]]:
        base = [
            [-0.5, -0.5, 0],
            [ 0.5, -0.5, 0],
            [ 0.5,  0.5, 0],
            [-0.5,  0.5, 0],
        ]
        apex = [0, 0, self.height]
        vertices = base + [apex]
        self.outputs['Vertices'] = vertices
        return vertices
