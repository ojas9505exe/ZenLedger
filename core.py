from time import time
import json
import hashlib


class ZenLedger:
    def __init__(self):
        self.ledger = []
        self.current_transactions = []
        self.nodes = set()
        self.create_block(proof=100,previous_hash ='1')

    #structure of the block - dictionary data structure
    def create_block(self, proof, previous_hash=None):
        block = {
            'index':len(self.ledger)+1,
            'timestamp':time(),
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.ledger[-1]),
            }
        self.current_transactions = []
        self.ledger.append(block)
        return block
    
    #create a new transaction
    def NewTransaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1
    
    @property
    def last_block(self):
        return self.ledger[-1]
    
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    #proof of work
    def pow(self,last_proof):
        proof = 0
        while self.valid_proof(last_proof,proof) is False:
            proof+=1
        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    