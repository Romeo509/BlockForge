from tronpy import Tron
from tronpy.keys import PrivateKey

# Initialize Tron client
client = Tron()

# 1. Create a new Tron wallet
def create_wallet():
    # Generate a private key
    private_key = PrivateKey.random()
    public_key = private_key.public_key
    address = public_key.to_base58check_address()

    # Return wallet details
    return {
        'private_key': private_key.hex(),
        'public_key': public_key.hex(),
        'address': address
    }

# 2. Check balance of USDT (TRC-20)
def check_balance(address):
    contract = client.get_contract('TetherUSD_Contract_Address')  # Use USDT contract address on Tron
    balance = contract.functions.balanceOf(address).call()
    return balance

# 3. Send USDT (TRC-20) from one wallet to another
def send_usdt(from_private_key, to_address, amount):
    private_key = PrivateKey.from_hex(from_private_key)
    account = client.trx.get_account(private_key.public_key.to_base58check_address())
    contract = client.get_contract('TetherUSD_Contract_Address')

    # Prepare transaction data
    txn = contract.functions.transfer(to_address, amount).with_owner(private_key.public_key).build()
    txn = txn.sign(private_key)

    # Send transaction
    txn_hash = txn.broadcast().wait()
    return txn_hash

# 4. Check the status of a transaction
def check_transaction_status(txn_hash):
    txn = client.trx.get_transaction(txn_hash)
    return txn['receipt']['result']


