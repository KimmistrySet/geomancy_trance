from nodes.node_base import Node
import numpy as np
from typing import Dict, List, Any

class TranslaterNode(Node):
    """
    Translate vertices by tx, ty, tz.
    """
    def __init__(self, node_id: str, tx: float = 0.0, ty: float = 0.0, tz: float = 0.0):
        super().__init__(node_id)
        self.tx, self.ty, self.tz = tx, ty, tz
        self.outputs["Translation"] = [tx, ty, tz]

    def evaluate(self, inputs: Dict[str, Any]) -> List[List[float]]:
        # 1. Input Validation
        if not inputs:
            return []
        
        # 2. Collect ALL incoming geometry
        all_vertices = []
        for input_data in inputs.values():
            if isinstance(input_data, list):
                all_vertices.extend(input_data)
        
        if not all_vertices:
            return []
            
        # 3. Convert to Numpy
        vertices = np.array(all_vertices, dtype=np.float32)
        
        # 4. Apply Translation
        # Numpy handles the broadcasting automatically (adding [x,y,z] to every row)
        translation_vector = np.array([self.tx, self.ty, self.tz], dtype=np.float32)
        translated_vertices = vertices + translation_vector
        
        return translated_vertices.tolist()
