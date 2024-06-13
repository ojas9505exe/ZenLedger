import json
import socket

class ZenNetwork:
    def __init__(self, ledger):
        self.ledger = ledger

    def register_node(self, address):
        self.ledger.nodes.add(address)

    def resolve_conflicts(self):
        neighbors = self.ledger.nodes
        new_chain = None
        max_length = len(self.ledger.chain)
        for node in neighbors:
            response = self.get_chain_from_node(node)
            if response:
                length = response.get('length', 0)
                chain = response.get('chain', None)
                if length > max_length and self.ledger.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        if new_chain:
            self.ledger.chain = new_chain
            return True
        return False

    def get_chain_from_node(self, node):
        try:
            response = None
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((node[0], node[1]))
                s.sendall(b'get_chain')
                data = s.recv(4096)
                response = json.loads(data.decode())
        except Exception as e:
            print(f"Failed to get chain from node {node}: {e}")
        return response
