BlockForge/
├── modules/                # All your core utility modules (e.g., for BTC, Solana, TRC-20)
│   ├── btc_utils.py        # Bitcoin-related functions (e.g., create wallet, send BTC)
│   ├── solana_utils.py     # Solana-related functions
│   └── trc20_utils.py      # TRC-20 token functions (e.g., USDT)
├── tests/                  # Unit and integration tests for your modules
│   ├── test_btc_utils.py   # Test file for BTC-related functions
│   ├── test_solana_utils.py# Test file for Solana-related functions
│   └── test_trc20_utils.py # Test file for TRC-20 related functions
├── .gitignore              # Git ignore file for excluding unnecessary files from version control
├── requirements.txt        # List of dependencies (e.g., tronpy, solathon, bitcoinlib, etc.)
├── README.md               # Project documentation for setup and usage
└── main.py                 # Main file to run the program, if needed (entry point for the project)

