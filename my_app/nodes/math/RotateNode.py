from nodes.node_base import Node
import numpy as np

class RotateNode(Node):
    def __init__(self, node_id: str, axis: str = "z", angle: float = 0.0):
        """
        Rotate vertices around x, y, or z axis by angle (radians).
        """
        super().__init__(node_id)
        self.axis = axis.lower()
        self.angle = angle

    def evaluate(self, context):
        if not context:
            return []
        last = list(context.values())[-1]
        if not isinstance(last, np.ndarray):
            last = np.array(last)

        c, s = np.cos(self.angle), np.sin(self.angle)
        if self.axis == "x":
            R = np.array([[1, 0, 0],
                          [0, c, -s],
                          [0, s, c]])
        elif self.axis == "y":
            R = np.array([[c, 0, s],
                          [0, 1, 0],
                          [-s, 0, c]])
        else:  # default z
            R = np.array([[c, -s, 0],
                          [s,  c, 0],
                          [0,  0, 1]])
        return np.dot(last, R.T)
