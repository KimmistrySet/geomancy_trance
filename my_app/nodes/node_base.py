# nodes/node_base.py
from typing import Dict, Any

class Node:
    def __init__(self, node_id: str, **kwargs):
        """
        Base Node class.
        - node_id: unique identifier
        - kwargs: optional metadata (ignored unless subclass uses it)
        """
        self.node_id = node_id
        self.inputs: Dict[str, Any] = {}
        self.outputs: Dict[str, Any] = {}
        self.params: Dict[str, Any] = kwargs

    def evaluate(self, context):
        raise NotImplementedError("Subclasses must implement evaluate()")
