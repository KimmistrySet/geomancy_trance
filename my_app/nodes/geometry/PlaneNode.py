from nodes.node_base import Node
import numpy as np

class PlaneNode(Node):
    def __init__(self, node_id: str, width: float = 1.0, height: float = 1.0, divisions: int = 10):
        super().__init__(node_id)
        self.width, self.height, self.divisions = width, height, divisions

    def evaluate(self, context):
        xs = np.linspace(-self.width/2, self.width/2, self.divisions)
        ys = np.linspace(-self.height/2, self.height/2, self.divisions)
        return np.array([[x,y,0] for x in xs for y in ys])
