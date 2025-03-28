import solathon
from solathon import Keypair, Client

# Set up the Solana client (Testnet for now, can change to Mainnet later)
SOLANA_RPC = "https://api.testnet.solana.com"  # You can change to Mainnet later
client = Client(SOLANA_RPC)

def create_solana_wallet():
    """
    Create a new Solana wallet (keypair) and return its public and private keys.
    """
    keypair = Keypair.generate()  # Generate a new keypair
    return {"public_key": str(keypair.public_key), "private_key": keypair.secret_key.decode()}

def get_solana_balance(public_key):
    """
    Get the balance of a given Solana wallet address.
    """
    try:
        # Get balance from Solana RPC client
        balance = client.get_balance(public_key)
        return balance / 1e9  # Convert lamports to SOL
    except Exception as e:
        print(f"Error retrieving balance: {e}")
        return None

def send_solana(from_private_key, to_address, amount):
    """
    Send Solana from one wallet to another.
    """
    try:
        # Get the sender's keypair from the private key
        from_keypair = Keypair.from_secret_key(from_private_key.encode())

        # Build and send the transaction
        transaction = solathon.Transaction().add(
            solathon.SystemInstruction.transfer(
                from_keypair.public_key, to_address, int(amount * 1e9)  # Convert SOL to lamports
            )
        )

        # Sign the transaction with the sender's private key
        transaction.sign(from_keypair)

        # Send the transaction
        response = client.send_transaction(transaction)
        return response
    except Exception as e:
        print(f"Error sending Solana: {e}")
        return None

