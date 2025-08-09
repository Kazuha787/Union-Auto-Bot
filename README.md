# Union Auto Bot (Multi-Wallet Fork by CryptoExplor)

🚀 **Union Auto Bot** is a Python-based automation tool designed to streamline token bridge transactions across multiple testnet networks, including Sepolia, Holesky, Sei, Bitcorn, Xion, and Babylon. This fork by [CryptoExplor](https://github.com/CryptoExplor) enhances the original bot with advanced **multi-wallet support**, allowing each wallet to operate independently across chains without cross-wallet interactions.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Features

* **Multi-Wallet Compatibility**: Seamless support for unlimited wallets with unique private keys, Xion, and Babylon addresses.
* **Separate Wallet Execution**: Each wallet performs transfers independently (no cross-wallet transfers).
* **Multi-Network Support**: Works across Sepolia, Holesky, Sei, Bitcorn, Xion, and Babylon testnets.
* **Dynamic Gas Estimation**
* **Colorful CLI Dashboard**: Real-time balance checks, transaction logs, and explorer links.
* **Flexible Configs**: Easily configure RPCs, token amounts, and delays per session.
* **Resilient Error Handling**
* **Secure**: Keeps private keys in a `.env` file. Never hardcoded.

## Prerequisites

* Python **3.8+**
* Git
* Terminal with Unicode and color support
* Testnet tokens (ETH, SEI, BTCN, etc.)
* Valid Xion and Babylon testnet addresses

## 🔧 Installation Guide

### Step 1: Clone the Repo

```bash
git clone https://github.com/CryptoExplor/Union-Auto.git
cd Union-Auto
```

### Step 2: Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv union-bot-env

# Activate it
source union-bot-env/bin/activate

# Deactivate when done
deactivate
```

### Step 3: Install Required Packages

```bash
pip install web3 eth-utils eth-abi eth-account aiohttp python-dotenv rich
```

> ⚠️ **Avoid using** `--break-system-packages` unless absolutely necessary.

### Step 4: Configure Environment

Create a `.env` file in the project root:

```dotenv
# Wallet 1
PRIVATE_KEY_1=your_private_key_1
XION_ADDRESS_1=xion1...
BABYLON_ADDRESS_1=bbn1...

# Wallet 2
PRIVATE_KEY_2=your_private_key_2
XION_ADDRESS_2=xion1...
BABYLON_ADDRESS_2=bbn1...

# Add more as needed
```

> 🔒 Add `.env` to `.gitignore` to prevent accidental leaks.

## 🧠 Usage

```bash
python main.py
```

1. Select which wallet to use (auto-detected from `.env`)
2. Choose the transfer option (1–13)
3. Set number of transactions
4. Watch real-time logs and progress

## 💼 Transfer Options

Supports 13 bridge paths:

1. Sepolia → Holesky
2. Sepolia → Babylon
3. Holesky → Sepolia
4. Holesky → Xion
5. Holesky → Babylon
6. Sei → Xion
7. Sei → Bitcorn
8. Sei → Binance Smart Chain (BSC)
9. Sei → Babylon
10. Bitcorn → Xion
11. Bitcorn → Sei
12. Bitcorn → Babylon
13. **Auto All God Mode**

## 🔧 Configuration

### Default Transfer Amounts (edit in `union.py`):

```python
self.sepolia_amount = 0.00001
self.holesky_amount = 0.00001
self.sei_amount = 0.001
self.corn_amount = 0.0000001
```

### Delay Between Transfers:

```python
self.min_delay = 5
self.max_delay = 20
```

### RPC URLs:

```python
self.SEPOLIA_RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"
self.HOLESKY_RPC_URL = "https://ethereum-holesky-rpc.publicnode.com/"
self.SEI_RPC_URL = "https://evm-rpc-testnet.sei-apis.com/"
self.CORN_RPC_URL = "https://21000001.rpc.thirdweb.com/"
```

## 📁 File Structure

```
Union-Auto/
├── main.py              # Entry point
├── union.py             # Core logic
├── ui.py                # CLI visuals & logs
├── utils.py             # Data/hex helpers
├── .env.example         # Sample config
├── README.md            # This file
├── requirements.txt     # Python packages
└── .gitignore
```

## 🛠 Troubleshooting

| Issue                                                 | Solution                                                                                 |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `SignedTransaction has no attribute 'rawTransaction'` | Use `Account.sign_transaction(...)` and extract `rawTransaction`, or RLP-encode manually |
| `Invalid private key`                                 | Ensure key is 64 hex chars (no `0x`)                                                     |
| `Insufficient funds`                                  | Claim from faucets and retry                                                             |
| `Invalid RPC URL`                                     | Replace RPC with working one (check Infura, Alchemy, etc.)                               |

## 🤝 Contributing

Fork → Feature branch → PR.
Follow PEP 8, include logs/comments, test thoroughly.

## 📜 License

MIT

## 🙏 Acknowledgments

* Original base: [Kazuha787/Union-Auto-Bot](https://github.com/Kazuha787/Union-Auto-Bot)
* Forked & upgraded by: [CryptoExplor](https://github.com/CryptoExplor)

## ⭐️ Support

Star the repo, join the Telegram @Offical\_Im\_kazuha, or open an issue!

> This bot is for educational/testnet use only. DYOR.
