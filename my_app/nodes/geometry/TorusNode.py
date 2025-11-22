from nodes.node_base import Node
import numpy as np

class TorusNode(Node):
    def __init__(self, node_id: str, major_radius: float = 2.0, minor_radius: float = 0.5, segments: int = 32, rings: int = 16):
        super().__init__(node_id)
        self.major_radius = major_radius
        self.minor_radius = minor_radius
        self.segments = segments
        self.rings = rings

    def evaluate(self, context):
        theta = np.linspace(0, 2*np.pi, self.segments, endpoint=False)
        phi = np.linspace(0, 2*np.pi, self.rings, endpoint=False)
        verts = []
        for t in theta:
            for p in phi:
                x = (self.major_radius + self.minor_radius*np.cos(p)) * np.cos(t)
                y = (self.major_radius + self.minor_radius*np.cos(p)) * np.sin(t)
                z = self.minor_radius * np.sin(p)
                verts.append([x,y,z])
        return np.array(verts)
