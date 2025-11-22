from nodes.node_base import Node
import numpy as np

class TerrainNode(Node):
    def __init__(self, node_id: str, width: int = 10, depth: int = 10, scale: float = 1.0):
        super().__init__(node_id)
        self.width, self.depth, self.scale = width, depth, scale

    def evaluate(self, context):
        xs = np.linspace(-self.width/2, self.width/2, self.width)
        zs = np.linspace(-self.depth/2, self.depth/2, self.depth)
        verts = []
        for x in xs:
            for z in zs:
                y = np.sin(x*0.2) * np.cos(z*0.2) * self.scale
                verts.append([x,y,z])
        return np.array(verts)
