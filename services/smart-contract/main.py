from web3 import Web3
import json

# Connect to BSC Testnet
bsc_rpc_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"
w3 = Web3(Web3.HTTPProvider(bsc_rpc_url))

# Validate RPC connection
if not w3.is_connected():
    print("Unable to connect to BSC Testnet!")
    exit()

# Account information
private_key = "YOUR_PRIVATE_KEY"  # Use a test wallet only, never a main wallet
account = w3.eth.account.from_key(private_key)
wallet_address = account.address

# Read ABI and bytecode from compiled contract output
with open("SimpleStorage.json") as f:
    contract_data = json.load(f)
abi = contract_data["abi"]
bytecode = contract_data["bytecode"]

# Create contract object
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Build deployment transaction
tx = SimpleStorage.constructor("Hello Binance").build_transaction({
    "from": wallet_address,
    "nonce": w3.eth.get_transaction_count(wallet_address),
    "gas": 2000000,
    "gasPrice": w3.to_wei("10", "gwei")
})

# Sign transaction
signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# Wait for transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
print(f"Contract deployed at: {contract_address}")
