from web3 import Web3, HTTPProvider
import json

def connect_with_blockchain(account):
    # Stage-1: where rpc server is available
    blockchainserver = "http://127.0.0.1:8575"  # Corrected URL format
    web3 = Web3(HTTPProvider(blockchainserver))

    # Stage-2: through which account we have to connect
    if account == 0:
        web3.eth.default_account = web3.eth.accounts[0]
    else:
        web3.eth.default_account = account

    # Stage-3: select your contract
    with open('../build/contracts/contact.json') as f:
        artifact_json = json.load(f)
        contract_abi = artifact_json['abi']  # Application Binary Interface (ABI)
        contract_address = artifact_json['networks']['5777']['address']

    # Stage-4: connect with the contract
    contract = web3.eth.contract(abi=contract_abi, address=contract_address)

    return contract, web3

try:
    # Connect to blockchain and retrieve contract object
    contract, web3 = connect_with_blockchain(0)

    # Insert contact information
    tx_hash = contract.functions.insertContact("sami", "23455677", "sami@gmail.com", "home").transact({
        'from': web3.eth.default_account  # Explicitly provide the 'from' account
    })

    # Wait for the transaction receipt using the updated method
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Contact information stored successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

# View contacts
contract, web3 = connect_with_blockchain(0)
_names, _mobiles, _emails, _organizations = contract.functions.viewContacts().call()
print(_names)
print(_mobiles)
print(_emails)
print(_organizations)
