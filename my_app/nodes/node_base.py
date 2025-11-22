# nodes/node_base.py
class Node:
    def __init__(self, node_id: str, **params):
        self.node_id = node_id
        self.params = params

    def evaluate(self, context):
        raise NotImplementedError("Each node must implement evaluate()")
