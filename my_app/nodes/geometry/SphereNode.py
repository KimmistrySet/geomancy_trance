from nodes.node_base import Node
import numpy as np

class SphereNode(Node):
    def __init__(self, node_id: str, radius: float = 1.0, segments: int = 16, rings: int = 16):
        super().__init__(node_id)
        self.radius, self.segments, self.rings = radius, segments, rings

    def evaluate(self, context):
        theta = np.linspace(0, 2*np.pi, self.segments, endpoint=False)
        phi = np.linspace(0, np.pi, self.rings, endpoint=False)
        verts = []
        for t in theta:
            for p in phi:
                x = self.radius * np.sin(p) * np.cos(t)
                y = self.radius * np.sin(p) * np.sin(t)
                z = self.radius * np.cos(p)
                verts.append([x,y,z])
        return np.array(verts)
