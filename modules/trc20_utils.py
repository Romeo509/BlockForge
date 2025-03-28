from tronpy import Tron

# Initialize the Tron client
client = Tron()

# USDT (TRC-20) Contract Address on the Tron blockchain
USDT_CONTRACT_ADDRESS = 'TQFTT9JP3fnSVo4G65g7zXqLwXfJJwxtQm'

# Initialize the contract object for USDT (TRC-20)
contract = client.get_contract(USDT_CONTRACT_ADDRESS)

# Function to check the balance of a TRC-20 token for a given address
def check_balance(address: str) -> float:
    """
    Check the balance of the TRC-20 token for a specific address.
    
    :param address: The address to check the balance of.
    :return: The balance of the TRC-20 token in the smallest unit (converted to USDT).
    """
    balance = contract.functions.balanceOf(address).call()
    return balance / 1e6  # USDT has 6 decimal places

# Function to send USDT from one address to another
def send_usdt(from_address: str, private_key: str, to_address: str, amount: float) -> str:
    """
    Send USDT (TRC-20) from one address to another.
    
    :param from_address: The address to send USDT from.
    :param private_key: The private key of the sender to sign the transaction.
    :param to_address: The address to send USDT to.
    :param amount: The amount of USDT to send.
    :return: The transaction ID of the broadcasted transaction.
    """
    # Get the private key for signing the transaction
    account = client.from_key(private_key)
    
    # Transfer the amount to the recipient address (convert amount to smallest unit, 6 decimals for USDT)
    txn = contract.functions.transfer(to_address, int(amount * 1e6))
    
    # Build and sign the transaction
    transaction = txn.build()
    signed = transaction.sign(account)
    
    # Broadcast the transaction and get the transaction ID
    tx_id = signed.broadcast().txid
    return tx_id

