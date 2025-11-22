from nodes.node_base import Node
import numpy as np

class GridNode(Node):
    def __init__(self, node_id: str, nx: int = 5, ny: int = 5, spacing: float = 1.0):
        super().__init__(node_id)
        self.nx = nx
        self.ny = ny
        self.spacing = spacing

    def evaluate(self, context):
        xs = np.arange(self.nx) * self.spacing
        ys = np.arange(self.ny) * self.spacing
        grid = np.array([[x,y,0] for x in xs for y in ys])
        return grid
