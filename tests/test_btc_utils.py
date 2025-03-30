import pytest
from unittest.mock import patch, MagicMock
from modules.btc_utils import create_btc_wallet, get_btc_balance, send_btc

# Mock data for testing
MOCK_WALLET_INFO = {
    "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "private_key": "5Kb8kLf9zgWQnogidDA76MzPL6TsZZY36hWXMssSzNydYXYB9KF",
    "wif": "L5agPjZKceSTkhqZF2dmFptT5LFrbr6ZGPvP7u4A6dvhTrr71WZ9"
}

MOCK_TXID = "a1b2c3d4e5f678901234567890123456789012345678901234567890123456"

class TestBTCUtils:
    
    @patch('modules.btc_utils.Wallet')
    def test_create_btc_wallet(self, mock_wallet):
        """Test wallet creation returns expected format"""
        # Setup mock
        mock_key = MagicMock()
        mock_key.address = MOCK_WALLET_INFO["address"]
        mock_key.key_private = MOCK_WALLET_INFO["private_key"]
        mock_key.wif = MOCK_WALLET_INFO["wif"]
        
        mock_wallet_instance = MagicMock()
        mock_wallet_instance.get_key.return_value = mock_key
        mock_wallet.create.return_value = mock_wallet_instance
        
        # Call function
        result = create_btc_wallet("test_wallet")
        
        # Assertions
        assert isinstance(result, dict)
        assert "address" in result
        assert "private_key" in result
        assert "wif" in result
        assert result["address"] == MOCK_WALLET_INFO["address"]
        mock_wallet.create.assert_called_once_with("test_wallet")

    @patch('modules.btc_utils.Service')
    def test_get_btc_balance(self, mock_service):
        """Test balance retrieval converts satoshis to BTC"""
        # Setup mock
        mock_service_instance = MagicMock()
        mock_service_instance.getbalance.return_value = 100000000  # 1 BTC in satoshis
        mock_service.return_value = mock_service_instance
        
        # Call function
        balance = get_btc_balance(MOCK_WALLET_INFO["address"])
        
        # Assertions
        assert balance == 1.0  # Should convert satoshis to BTC
        mock_service_instance.getbalance.assert_called_once_with(MOCK_WALLET_INFO["address"])

    @patch('modules.btc_utils.Wallet')
    def test_send_btc_success(self, mock_wallet):
        """Test successful BTC send returns transaction ID"""
        # Setup mock
        mock_tx = MagicMock()
        mock_tx.txid = MOCK_TXID
        mock_wallet_instance = MagicMock()
        mock_wallet_instance.send_to.return_value = mock_tx
        mock_wallet.return_value = mock_wallet_instance
        
        # Call function
        txid = send_btc("test_wallet", MOCK_WALLET_INFO["address"], 0.1)
        
        # Assertions
        assert txid == MOCK_TXID
        mock_wallet.assert_called_once_with("test_wallet")
        mock_wallet_instance.send_to.assert_called_once_with(
            MOCK_WALLET_INFO["address"],
            0.1,
            fee=1000,
            network='bitcoin'
        )

    @patch('modules.btc_utils.Wallet')
    def test_send_btc_failure(self, mock_wallet):
        """Test send BTC handles errors properly"""
        # Setup mock to raise exception
        mock_wallet_instance = MagicMock()
        mock_wallet_instance.send_to.side_effect = Exception("Insufficient funds")
        mock_wallet.return_value = mock_wallet_instance
        
        # Test that exception is properly raised
        with pytest.raises(ValueError) as excinfo:
            send_btc("test_wallet", MOCK_WALLET_INFO["address"], 1000)
        
        assert "Transaction failed" in str(excinfo.value)

    def test_imports(self):
        """Test that all required functions are imported"""
        from modules.btc_utils import (
            create_btc_wallet,
            get_btc_balance,
            send_btc
        )
        assert all(callable(func) for func in [create_btc_wallet, get_btc_balance, send_btc])
