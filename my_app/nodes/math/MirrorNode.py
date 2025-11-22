from nodes.node_base import Node
import numpy as np

class MirrorNode(Node):
    def __init__(self, node_id: str, axis: str = "x"):
        """
        Mirror vertices across a chosen axis (x, y, or z).
        """
        super().__init__(node_id)
        self.axis = axis.lower()

    def evaluate(self, context):
        if not context:
            return []
        last = list(context.values())[-1]
        mirrored = last.copy()
        if self.axis == "x":
            mirrored[:,0] *= -1
        elif self.axis == "y":
            mirrored[:,1] *= -1
        elif self.axis == "z":
            mirrored[:,2] *= -1
        return mirrored
