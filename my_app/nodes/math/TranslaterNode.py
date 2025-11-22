from nodes.node_base import Node
import numpy as np
from typing import Dict, List

class TranslaterNode(Node):
    """
    Translate vertices by tx, ty, tz.
    """
    def __init__(self, node_id: str, tx: float = 0.0, ty: float = 0.0, tz: float = 0.0):
        super().__init__(node_id)
        self.tx, self.ty, self.tz = tx, ty, tz
        self.outputs["Translation"] = [tx, ty, tz]

    def evaluate(self, graph_data: Dict) -> List[List[float]]:
        if not graph_data:
            return []
        last = list(graph_data.values())[-1]
        return (last + np.array([self.tx, self.ty, self.tz], dtype=np.float32)).tolist()
