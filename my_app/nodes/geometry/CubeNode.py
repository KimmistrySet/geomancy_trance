from nodes.node_base import Node
import numpy as np

class CubeNode(Node):
    """
    Generates 8 vertices of an axis-aligned cube centered at origin.
    Supports either width/height/depth or size shorthand.
    """
    def __init__(self, node_id: str,
                 width: float = 1.0,
                 height: float = 1.0,
                 depth: float = 1.0,
                 size: float = None):
        super().__init__(node_id)
        if size is not None:
            width = height = depth = float(size)
        self.width = float(width)
        self.height = float(height)
        self.depth = float(depth)
        self.outputs["Vertices"] = None

    def evaluate(self, context):
        w = self.width / 2.0
        h = self.height / 2.0
        d = self.depth / 2.0
        verts = np.array([
            [-w, -h, -d], [ w, -h, -d], [ w,  h, -d], [-w,  h, -d],
            [-w, -h,  d], [ w, -h,  d], [ w,  h,  d], [-w,  h,  d],
        ], dtype=np.float32)
        self.outputs["Vertices"] = verts.tolist()
        return self.outputs["Vertices"]
