from nodes.node_base import Node
import numpy as np

class ConeNode(Node):
    """
    Generates base circle vertices and apex for a right circular cone.
    """
    def __init__(self, node_id: str, radius: float = 1.0, height: float = 2.0, segments: int = 32):
        super().__init__(node_id)
        self.radius = float(radius)
        self.height = float(height)
        self.segments = int(segments)
        self.outputs["Vertices"] = None

    def evaluate(self, context):
        theta = np.linspace(0, 2*np.pi, self.segments, endpoint=False, dtype=np.float32)
        base = np.column_stack([
            self.radius*np.cos(theta),
            self.radius*np.sin(theta),
            np.zeros(self.segments, dtype=np.float32)
        ])
        apex = np.array([[0.0, 0.0, self.height]], dtype=np.float32)
        verts = np.vstack([base, apex])
        self.outputs["Vertices"] = verts.tolist()
        return self.outputs["Vertices"]
