from nodes.node_base import Node
import numpy as np
from typing import Dict, List, Any

class MirrorNode(Node):
    """
    Mirror vertices across a chosen axis (x, y, or z).
    Handles multiple inputs by mirroring EVERYTHING connected to it.
    """
    def __init__(self, node_id: str, axis: str = "x"):
        super().__init__(node_id)
        self.axis = axis.lower()
        self.outputs["Axis"] = self.axis

    def evaluate(self, inputs: Dict[str, Any]) -> List[List[float]]:
        """
        inputs: A dictionary where keys are the input names (or node IDs) 
                and values are the geometry lists from previous nodes.
        """
        if not inputs:
            return []

        # 1. Collect ALL geometry from all connected nodes
        all_vertices = []
        for input_data in inputs.values():
            if isinstance(input_data, list):
                all_vertices.extend(input_data)
        
        if not all_vertices:
            return []

        # 2. Convert to Numpy for fast math
        # Ensure we are working with float32 for 3D compatibility
        arr = np.array(all_vertices, dtype=np.float32)
        
        # 3. Create the Mirror Copy
        mirrored = arr.copy()
        
        if self.axis == "x":
            mirrored[:, 0] *= -1
        elif self.axis == "y":
            mirrored[:, 1] *= -1
        elif self.axis == "z":
            mirrored[:, 2] *= -1
            
        # 4. Return the result
        # Note: Do you want JUST the reflection? Or Original + Reflection?
        # This code returns JUST the reflection (matching your original logic).
        return mirrored.tolist()
