import numpy as np
from nodes.node_base import Node


class SphereNode(Node):
    """
    Generates a sphere mesh using latitude/longitude subdivision.
    """
    def __init__(self, node_id: str, radius: float = 1.0, segments: int = 16):
        super().__init__(node_id, "Sphere")
        self.radius = radius
        self.segments = segments
        self.outputs['Vertices'] = None

    def evaluate(self, graph_data: dict) -> list[list[float]]:
        vertices = []
        for i in range(self.segments + 1):
            theta = np.pi * i / self.segments
            for j in range(self.segments + 1):
                phi = 2 * np.pi * j / self.segments
                x = self.radius * np.sin(theta) * np.cos(phi)
                y = self.radius * np.sin(theta) * np.sin(phi)
                z = self.radius * np.cos(theta)
                vertices.append([x, y, z])
        self.outputs['Vertices'] = vertices
        return vertices
