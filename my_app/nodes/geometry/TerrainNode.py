from nodes.node_base import Node
import numpy as np

class TerrainNode(Node):
    """
    Generates a heightfield mesh vertices using a simple sinusoid pattern.
    """
    def __init__(self, node_id: str, width: int = 50, depth: int = 50, scale: float = 1.0, freq_x: float = 0.2, freq_z: float = 0.2):
        super().__init__(node_id)
        self.width = int(width)
        self.depth = int(depth)
        self.scale = float(scale)
        self.fx = float(freq_x)
        self.fz = float(freq_z)
        self.outputs["Vertices"] = None

    def evaluate(self, context):
        xs = np.linspace(-self.width/2.0, self.width/2.0, self.width, dtype=np.float32)
        zs = np.linspace(-self.depth/2.0, self.depth/2.0, self.depth, dtype=np.float32)
        X, Z = np.meshgrid(xs, zs, indexing="xy")
        Y = np.sin(X * self.fx) * np.cos(Z * self.fz) * self.scale
        verts = np.column_stack([X.flatten(), Y.flatten(), Z.flatten()]).astype(np.float32)
        self.outputs["Vertices"] = verts.tolist()
        return self.outputs["Vertices"]
