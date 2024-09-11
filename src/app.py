from flask import Flask, render_template, request
from web3 import Web3, HTTPProvider
import json

app = Flask(__name__)

def connect_with_blockchain(account):
    # Stage-1: where rpc server is available
    blockchainserver = "http://127.0.0.1:8575"
    web3 = Web3(HTTPProvider(blockchainserver))

    # Stage-2: through which account we have to connect
    if account == 0:
        web3.eth.default_account = web3.eth.accounts[0]
    else:
        web3.eth.default_account = account

    # Stage-3: select your contract
    with open('../build/contracts/contact.json') as f:
        artifact_json = json.load(f)
        contract_abi = artifact_json['abi']
        contract_address = artifact_json['networks']['5777']['address']

    # Stage-4: connect with the contract
    contract = web3.eth.contract(abi=contract_abi, address=contract_address)

    return contract, web3

@app.route('/')
def homepage():
    return render_template('index.html', err='', res='')

@app.route('/insertcontact', methods=['POST'])
def insertcontact():
    name = request.form.get('name')
    mobile = request.form.get('mobile')
    email = request.form.get('email')
    org = request.form.get('org')

    # Basic validation
    if not (name and mobile and email and org):
        return render_template('index.html', err='All fields are required!', res='')

    try:
        # Connect to blockchain and retrieve contract object
        contract, web3 = connect_with_blockchain(0)

        # Insert contact information
        tx_hash = contract.functions.insertContact(name, mobile, email, org).transact()

        # Wait for the transaction receipt
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print("Contact information stored successfully.")
        return render_template('index.html', err='', res='Contact successfully added!')

    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template('index.html', err='contact already exists.', res='')

@app.route('/viewcontacts')
def viewcontacts():
    contract, web3 = connect_with_blockchain(0)
    _names,_mobiles,_emails,_organizations=contract.functions.viewContacts().call()

    data=[]
    for i in range(len(_names)):
        dummy=[]
        dummy.append(_names[i])
        dummy.append(_mobiles[i])
        dummy.append(_emails[i])
        dummy.append(_organizations[i])
        data.append(dummy)
    print(data)
    return render_template('viewcontacts.html',data=data,l=len(data))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
