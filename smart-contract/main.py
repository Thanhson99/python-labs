from web3 import Web3
import json

# Kết nối với BSC Testnet
bsc_rpc_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"
w3 = Web3(Web3.HTTPProvider(bsc_rpc_url))

# Kiểm tra kết nối
if not w3.is_connected():
    print("Không kết nối được với BSC Testnet!")
    exit()

# Thông tin tài khoản
private_key = "YOUR_PRIVATE_KEY"  # Dùng ví test, KHÔNG DÙNG VÍ CHÍNH
account = w3.eth.account.from_key(private_key)
wallet_address = account.address

# Đọc ABI và bytecode từ file biên dịch (hoặc tự định nghĩa)
with open("SimpleStorage.json") as f:
    contract_data = json.load(f)
abi = contract_data["abi"]
bytecode = contract_data["bytecode"]

# Tạo hợp đồng
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Tạo giao dịch triển khai hợp đồng
tx = SimpleStorage.constructor("Hello Binance").build_transaction({
    "from": wallet_address,
    "nonce": w3.eth.get_transaction_count(wallet_address),
    "gas": 2000000,
    "gasPrice": w3.to_wei("10", "gwei")
})

# Ký giao dịch
signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# Chờ giao dịch hoàn tất
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
print(f"Hợp đồng được triển khai tại: {contract_address}")
