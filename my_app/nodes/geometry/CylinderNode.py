import numpy as np
from nodes.node_base import Node


class CylinderNode(Node):
    """
    Generates a cylinder mesh with circular base and top.
    """
    def __init__(self, node_id: str, radius: float = 1.0, height: float = 2.0, segments: int = 16):
        super().__init__(node_id, "Cylinder")
        self.radius = radius
        self.height = height
        self.segments = segments
        self.outputs['Vertices'] = None

    def evaluate(self, graph_data: dict) -> list[list[float]]:
        vertices = []
        for i in range(self.segments):
            angle = 2 * np.pi * i / self.segments
            x = self.radius * np.cos(angle)
            y = self.radius * np.sin(angle)
            # bottom circle
            vertices.append([x, y, 0])
            # top circle
            vertices.append([x, y, self.height])
        self.outputs['Vertices'] = vertices
        return vertices
