from nodes.node_base import Node
import numpy as np

class ScatterNode(Node):
    def __init__(self, node_id: str, count: int = 50, range_x: float = 5.0, range_y: float = 5.0, range_z: float = 5.0):
        super().__init__(node_id)
        self.count = count
        self.range_x = range_x
        self.range_y = range_y
        self.range_z = range_z

    def evaluate(self, context):
        pts = np.random.rand(self.count, 3)
        pts[:,0] = (pts[:,0]-0.5)*self.range_x
        pts[:,1] = (pts[:,1]-0.5)*self.range_y
        pts[:,2] = (pts[:,2]-0.5)*self.range_z
        return pts
