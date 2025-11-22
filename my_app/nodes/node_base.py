# nodes/node_base.py
class Node:
    def __init__(self, node_id: str, **kwargs):
        """
        Base Node class.
        node_id: unique identifier for this node
        kwargs: extra parameters passed by subclasses (ignored unless used)
        """
        self.node_id = node_id
        self.params = kwargs
        self.inputs = {}
        self.outputs = {}