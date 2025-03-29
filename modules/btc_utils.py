from bitcoinlib.wallets import Wallet
from bitcoinlib.services import Service

#Initialize a Bitcoin service (mainnet by default)
service = Service(network='bitcoin')

def create_btc_wallet(wallet_name: str):
    """
    Create a new bitcoin wallet.
    :param wallet_name: Name of the wallet to create.
    :return: Wallet details including address and private key.
    """
    wallet = Wallet.create(wallet_name)
    address = wallet.get_key().address
    private_key = wallet.get_key().wif
    return {"address": address, "private_key": private_key}

def get_btc_balance(address:  str) -> float:
    """
    Check the Bitcoin balance of a given address.
    :param address: Bitcoin address to check.
    :return: Balance in BTC
    """
    balance = service.getbalance(address)
    return balance / 1e8 # Convert satoshis to BTC

def send_btc(wallet_name: str, to_address: str, amount: float) -> str:
    """
    Send BTC from a wallet to another address.
    :param wallet_name: Name of the wallet to send BTC from.
    :param to_address: Recipient BTC address.
    :param amount: Amount of BTC to send.
    :return: Transaction ID.
    """
    wallet = Wallet(wallet_name)
    tx = wallet.send_to(to_address, amount, fee=1000) #Adjust fee as needed
    return tx.txid
