from nodes.node_base import Node
import numpy as np

class SphereNode(Node):
    """
    Generates vertices on a sphere using latitude (phi) and longitude (theta) sampling.
    """
    def __init__(self, node_id: str, radius: float = 1.0, segments: int = 32, rings: int = 16):
        super().__init__(node_id)
        self.radius = float(radius)
        self.segments = int(segments)
        self.rings = int(rings)
        self.outputs["Vertices"] = None

    def evaluate(self, context):
        theta = np.linspace(0, 2*np.pi, self.segments, endpoint=False, dtype=np.float32)
        phi = np.linspace(0, np.pi, self.rings, endpoint=False, dtype=np.float32)
        T, P = np.meshgrid(theta, phi, indexing="xy")
        x = self.radius * np.sin(P) * np.cos(T)
        y = self.radius * np.sin(P) * np.sin(T)
        z = self.radius * np.cos(P)
        verts = np.column_stack([x.flatten(), y.flatten(), z.flatten()]).astype(np.float32)
        self.outputs["Vertices"] = verts.tolist()
        return self.outputs["Vertices"]
