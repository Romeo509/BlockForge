from bitcoinlib.wallets import Wallet
from bitcoinlib.services import Service

# Initialize a Bitcoin service (mainnet by default)
service = Service(network='bitcoin')

def create_btc_wallet(wallet_name: str) -> dict:
    """
    Create a new bitcoin wallet.
    
    Args:
        wallet_name: Name of the wallet to create.
    
    Returns:
        Dictionary containing address and private key.
        Format: {"address": str, "private_key": str}
    """
    wallet = Wallet.create(wallet_name)
    key = wallet.get_key()
    return {
        "address": key.address,
        "private_key": key.key_private,  # Using key_private instead of wif
        "wif": key.wif  # Added WIF format as well
    }

def get_btc_balance(address: str) -> float:
    """
    Check the Bitcoin balance of a given address.
    
    Args:
        address: Bitcoin address to check.
    
    Returns:
        Balance in BTC (float)
    """
    balance = service.getbalance(address)
    return balance / 1e8  # Convert satoshis to BTC

def send_btc(wallet_name: str, to_address: str, amount: float, fee: int = 1000) -> str:
    """
    Send BTC from a wallet to another address.
    
    Args:
        wallet_name: Name of the wallet to send from.
        to_address: Recipient BTC address.
        amount: Amount of BTC to send.
        fee: Transaction fee in satoshis (default: 1000)
    
    Returns:
        Transaction ID (str)
    
    Raises:
        ValueError: If insufficient funds or invalid address
    """
    wallet = Wallet(wallet_name)
    try:
        tx = wallet.send_to(
            to_address,
            amount,
            fee=fee,
            network='bitcoin'
        )
        return tx.txid
    except Exception as e:
        raise ValueError(f"Transaction failed: {str(e)}")
