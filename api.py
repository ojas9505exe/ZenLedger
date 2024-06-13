# app.py

from flask import Flask, jsonify, request
from core import ZenLedger
from ZenNetwork import ZenNetwork

app = Flask(__name__)
ledger = ZenLedger()
blockchain_network = ZenNetwork(ledger)

@app.route('/wallet/new', methods=['POST'])
def create_wallet():
    # Create a new wallet address
    wallet_address = "address_generated_here"
    return jsonify({"wallet_address": wallet_address}), 200

@app.route('/transactions/new', methods=['POST'])
def submit_transaction():
    values = request.get_json()

    # Check required fields are in the POST data
    required_fields = ['sender', 'recipient', 'amount']
    if not all(field in values for field in required_fields):
        return 'Missing values', 400

    # Add the transaction to the ledger
    index = ledger.NewTransaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine_block():
    # Mine a new block
    last_block = ledger.last_block
    last_proof = last_block['proof']
    proof = ledger.pow(last_proof)

    # Reward the miner by adding a transaction
    ledger.NewTransaction(sender="0", recipient="miner_reward_address", amount=1)

    # Create the new block
    previous_hash = ledger.hash(last_block)
    block = ledger.create_block(proof, previous_hash)

    response = {
        'message': 'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    # Get the full blockchain
    response = {
        'chain': ledger.ledger,
        'length': len(ledger.ledger),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
