from tronpy import Tron
from tronpy.exceptions import AddressNotFound
from decimal import Decimal

# Initialize the Tron client (mainnet)
client = Tron(network="mainnet")

# USDT (TRC-20) Contract Address on the Tron blockchain
USDT_CONTRACT_ADDRESS = "TQFTT9JP3fnSVo4G65g7zXqLwXfJJwxtQm"

# Initialize the contract object for USDT (TRC-20)
contract = client.get_contract(USDT_CONTRACT_ADDRESS)


# Function to check the balance of a TRC-20 token for a given address
def check_balance(address: str) -> float:
    """
    Check the balance of the TRC-20 token for a specific address.

    :param address: The address to check the balance of.
    :return: The balance of the TRC-20 token in USDT.
    """
    try:
        if not client.is_address(address):
            raise ValueError("Invalid TRON address")
        balance = contract.functions.balanceOf(address).call()
        return balance / 1e6  # USDT has 6 decimal places
    except AddressNotFound:
        return 0.0
    except Exception as e:
        print(f"Error checking balance: {e}")
        return 0.0


# Function to check TRX balance (needed for fees)
def check_trx_balance(address: str) -> float:
    """
    Check the TRX balance of an address.

    :param address: The address to check.
    :return: TRX balance.
    """
    try:
        return client.get_account_balance(address)
    except Exception as e:
        print(f"Error checking TRX balance: {e}")
        return 0.0


# Function to send USDT from one address to another
def send_usdt(from_address: str, private_key: str, to_address: str, amount: float) -> str:
    """
    Send USDT (TRC-20) from one address to another.

    :param from_address: The address to send USDT from.
    :param private_key: The private key of the sender to sign the transaction.
    :param to_address: The address to send USDT to.
    :param amount: The amount of USDT to send.
    :return: The transaction ID of the broadcasted transaction or an error message.
    """
    try:
        if not client.is_address(to_address):
            return "Invalid recipient address."

        # Ensure sender has TRX for fees
        trx_balance = check_trx_balance(from_address)
        if trx_balance < 10:  # keep a small buffer (10 TRX is safe)
            return "Insufficient TRX for fees."

        # Get account from private key
        account = client.from_key(private_key)

        # Convert USDT to smallest unit (6 decimals)
        usdt_amount = int(Decimal(amount) * 1_000_000)

        # Build, sign, and send transaction with fee limit
        txn = (
            contract.functions.transfer(to_address, usdt_amount)
            .with_owner(from_address)
            .fee_limit(5_000_000)  # 5 TRX max fee
            .build()
        )

        signed_tx = txn.sign(account)
        result = signed_tx.broadcast()

        return result["txid"]

    except Exception as e:
        return f"Error sending USDT: {e}"
