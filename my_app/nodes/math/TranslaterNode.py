from nodes.node_base import Node
import numpy as np

class TranslaterNode(Node):
    def __init__(self, node_id: str, tx: float = 0.0, ty: float = 0.0, tz: float = 0.0):
        super().__init__(node_id)
        self.tx, self.ty, self.tz = tx, ty, tz

    def evaluate(self, context):
        if not context:
            return []
        last = list(context.values())[-1]
        return last + np.array([self.tx, self.ty, self.tz])
