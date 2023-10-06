import web3
from web3 import Web3, HTTPProvider
from web3.middleware import construct_sign_and_send_raw_middleware

# Ethereum node (Ropsten testnet) and contract details
infura_url = "https://ropsten.infura.io/v3/"
contract_address = "0xYourContractAddress"
contract_abi = [
    # Sample contract ABI
]

# Ethereum account details
sender_address = "0xYourSenderAddress"
sender_private_key = "YourPrivateKey"

# Create a connection to the Ethereum node
w3 = Web3(HTTPProvider(infura_url))

# Check if connected to the Ethereum node
if w3.isConnected():
    print("Connected to Ethereum node")
else:
    print("Failed to connect to Ethereum node")
    exit(1)

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

location = "123 Main St."


def send_transaction():
    try:
        nonce = w3.eth.getTransactionCount(sender_address)

        transaction = contract.functions.addLandRegistryUpdate(
            location
        ).buildTransaction(
            {
                "chainId": 3,
                "gas": 2000000,
                "gasPrice": w3.toWei("10", "gwei"),
                "nonce": nonce,
            }
        )

        signed_transaction = w3.eth.account.signTransaction(
            transaction, sender_private_key
        )

        w3.middleware_onion.add(
            construct_sign_and_send_raw_middleware(sender_private_key)
        )
        txn_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

        receipt = w3.eth.waitForTransactionReceipt(txn_hash)
        print(f"Transaction Hash: {txn_hash}")
        print(f"Transaction Receipt: {receipt}")

    except Exception as e:
        print(f"Transaction failed: {str(e)}")


send_transaction()