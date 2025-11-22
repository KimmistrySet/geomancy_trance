from nodes.node_base import Node
import numpy as np

class ConeNode(Node):
    def __init__(self, node_id: str, radius: float = 1.0, height: float = 2.0, segments: int = 16):
        super().__init__(node_id)
        self.radius = radius
        self.height = height
        self.segments = segments

    def evaluate(self, context):
        # Simple cone vertices (circle base + apex)
        theta = np.linspace(0, 2*np.pi, self.segments, endpoint=False)
        base = np.column_stack([self.radius*np.cos(theta), self.radius*np.sin(theta), np.zeros(self.segments)])
        apex = np.array([[0,0,self.height]])
        return np.vstack([base, apex])
