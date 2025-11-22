import numpy as np
from nodes.node_base import Node


class NoiseNode(Node):
    """
    Applies Perlin-style noise or random distortion to geometry vertices.
    Useful for terrain, organic shapes, or procedural variation.
    """
    def __init__(self, node_id: str, scale: float = 0.1, seed: int = None):
        super().__init__(node_id, "Noise")
        self.inputs['Vertices'] = None
        self.scale = scale
        self.seed = seed
        self.outputs['NoisyVertices'] = None

    def evaluate(self, graph_data: dict) -> list[list[float]]:
        vertices = resolve_input(self.id, 'Vertices', graph_data)
        arr = np.array(vertices, dtype=np.float32)

        # Optional reproducibility
        if self.seed is not None:
            np.random.seed(self.seed)

        # Add random noise scaled by factor
        noise = (np.random.rand(*arr.shape) - 0.5) * 2 * self.scale
        noisy = arr + noise

        self.outputs['NoisyVertices'] = noisy.tolist()
        return noisy.tolist()
