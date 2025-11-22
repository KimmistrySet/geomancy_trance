import numpy as np
from nodes.node_base import Node


class TerrainNode(Node):
    """
    Generates a terrain mesh from a numeric data column.
    Each value maps to vertex height in a grid.
    """
    def __init__(self, node_id: str, grid_size: int = 10):
        super().__init__(node_id, "Terrain")
        self.inputs['DataColumn'] = None
        self.grid_size = grid_size
        self.outputs['Vertices'] = None

    def evaluate(self, graph_data: dict) -> list[list[float]]:
        data = resolve_input(self.id, 'DataColumn', graph_data)
        norm = (np.array(data) - np.min(data)) / (np.max(data) - np.min(data))

        vertices = []
        idx = 0
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                z = float(norm[idx % len(norm)])
                vertices.append([x, y, z])
                idx += 1

        self.outputs['Vertices'] = vertices
        return vertices
