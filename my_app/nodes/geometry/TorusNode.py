from nodes.node_base import Node
import numpy as np

class TorusNode(Node):
    """
    Generates vertices on a torus with major (R) and minor (r) radii.
    """
    def __init__(self, node_id: str, major_radius: float = 2.0, minor_radius: float = 0.5, segments: int = 64, rings: int = 32):
        super().__init__(node_id)
        self.R = float(major_radius)
        self.r = float(minor_radius)
        self.segments = int(segments)
        self.rings = int(rings)
        self.outputs["Vertices"] = None

    def evaluate(self, context):
        theta = np.linspace(0, 2*np.pi, self.segments, endpoint=False, dtype=np.float32)
        phi = np.linspace(0, 2*np.pi, self.rings, endpoint=False, dtype=np.float32)
        T, P = np.meshgrid(theta, phi, indexing="xy")
        x = (self.R + self.r*np.cos(P)) * np.cos(T)
        y = (self.R + self.r*np.cos(P)) * np.sin(T)
        z = self.r * np.sin(P)
        verts = np.column_stack([x.flatten(), y.flatten(), z.flatten()]).astype(np.float32)
        self.outputs["Vertices"] = verts.tolist()
        return self.outputs["Vertices"]
