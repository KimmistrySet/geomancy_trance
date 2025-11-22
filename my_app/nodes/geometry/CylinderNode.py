from nodes.node_base import Node
import numpy as np

class CylinderNode(Node):
    def __init__(self, node_id: str, radius: float = 1.0, height: float = 2.0, segments: int = 16):
        super().__init__(node_id)
        self.radius, self.height, self.segments = radius, height, segments

    def evaluate(self, context):
        theta = np.linspace(0, 2*np.pi, self.segments, endpoint=False)
        bottom = np.column_stack([self.radius*np.cos(theta), self.radius*np.sin(theta), np.zeros(self.segments)])
        top = np.column_stack([self.radius*np.cos(theta), self.radius*np.sin(theta), np.full(self.segments, self.height)])
        return np.vstack([bottom, top])
