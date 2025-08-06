# Union Auto Bot

🚀 **Union Auto Bot** is a Python-based automation tool designed to streamline token bridge transactions across multiple testnet networks, including Sepolia, Holesky, Sei, Bitcorn, Xion, and Babylon. With a sleek terminal-based UI powered by the `rich` library, it supports multi-wallet operations, real-time transaction tracking, and secure cross-chain transfers. Perfect for developers, testers, and blockchain enthusiasts looking to automate repetitive tasks on the Union Testnet! 🌉

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Features

- **Multi-Network Support**: Automate token transfers between Sepolia, Holesky, Sei, Bitcorn, Xion, and Babylon testnets.
- **Multi-Wallet Compatibility**: Process transactions using multiple private keys and corresponding Xion/Babylon addresses.
- **Dynamic Gas Estimation**: Automatically calculates gas fees for reliable transaction execution.
- **Real-Time Dashboard**: Terminal-based UI with colorful logs for transaction status, balances, and explorer links.
- **Error Handling**: Robust retry logic and detailed error logging for failed transactions.
- **Configurable Settings**: Customize transaction amounts, delays, and RPC endpoints via class attributes.
- **Cross-Chain Automation**: Supports 12 transfer pairs, including an "Auto All God Mode" for running all pairs sequentially.
- **Secure**: Uses environment variables for sensitive data like private keys.

## Prerequisites

Before using Union Auto Bot, ensure you have:

- **Python 3.8+**: Install from [python.org](https://www.python.org/downloads/).
- **Git**: Installed for cloning the repository.
- **Testnet Funds**: Sufficient testnet tokens (ETH, SEI, BTCN) on supported networks.
- **Xion & Babylon Addresses**: Corresponding addresses for cross-chain transfers.
- A modern terminal (e.g., VS Code, iTerm2, Windows Terminal) for optimal UI rendering.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/CryptoExplor/Union-Auto.git
   cd Union-Auto
   ```

2. **Install Dependencies**:
   Install required Python packages using `pip`:
   ```bash
   pip install web3 eth-utils eth-abi eth-account aiohttp python-dotenv rich
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root and add your private key and addresses:
   ```env
   PRIVATE_KEY=your_private_key_here
   XION_ADDRESS=your_xion_address_here
   BABYLON_ADDRESS=your_babylon_address_here
   ```
   > **Note**: Never expose your private keys publicly. Ensure the `.env` file is added to `.gitignore`.

4. **Verify Configuration**:
   Ensure the `.env` file is correctly formatted and contains valid EVM private keys and corresponding Xion/Babylon addresses.

## Usage

1. **Run the Bot**:
   Start the bot by executing:
   ```bash
   python main.py
   ```

2. **Select Transfer Option**:
   The bot will display an interactive menu with 13 options:
   ```
   ╔════════════════════════════════════╗
   ║      Select Transfer Option        ║
   ╚════════════════════════════════════╝
   1. Sepolia Testnet to Holesky Testnet
   2. Sepolia Testnet to Babylon Testnet
   3. Holesky Testnet to Sepolia Testnet
   4. Holesky Testnet to Xion Testnet
   5. Holesky Testnet to Babylon Testnet
   6. Sei Testnet to Xion Testnet
   7. Sei Testnet to Bitcorn Testnet
   8. Sei Testnet to Binance Smart Chain Testnet
   9. Sei Testnet to Babylon Testnet
   10. Bitcorn Testnet to Xion Testnet
   11. Bitcorn Testnet to Sei Testnet
   12. Bitcorn Testnet to Babylon Testnet
   13. Auto All God Mod
   ══════════════════════════════════════
   Choose -> 
   ```
   Enter a number (1–13) to select a transfer pair or the "Auto All God Mode" to run all pairs.

3. **Specify Transaction Count**:
   Enter the number of transactions to perform for the selected pair:
   ```
   How Many Times Do You Want To Make a Transfer? -> 
   ```

4. **Monitor Progress**:
   The bot will display real-time logs with balance checks, transaction details, and explorer links for each transfer. Successful transactions will show block numbers and Union explorer links.

## File Structure

```
Union-Auto-Bot/
├── main.py              # Entry point for running the bot
├── union.py             # Core logic for transaction processing and cross-chain transfers
├── ui.py                # Terminal UI utilities using the rich library
├── utils.py             # Helper functions for encoding and formatting data
├── .env.example         # Example environment file for configuration
├── .gitignore           # Git ignore rules for sensitive files
├── README.md            # Project documentation (this file)
└── requirements.txt     # List of Python dependencies
```

### File Descriptions

- **`main.py`**: Initializes the bot, loads environment variables, and orchestrates the transfer process.
- **`union.py`**: Contains the `Union` class with methods for transaction execution, balance checks, and cross-chain instruction generation.
- **`ui.py`**: Provides logging functions (`logger_info`, `logger_success`, etc.) for a colorful terminal interface.
- **`utils.py`**: Utility functions for hex padding and data encoding used in transaction construction.
- **`.env.example`**: Template for the `.env` file to store private keys and addresses.
- **`.gitignore`**: Excludes sensitive files (e.g., `.env`, `*.pyc`) from version control.
- **`requirements.txt`**: Lists required Python packages for easy installation.

## Configuration

### Environment Variables
The `.env` file must include:
- `PRIVATE_KEY`: Your EVM-compatible private key (e.g., for Sepolia, Holesky, etc.).
- `XION_ADDRESS`: Your Xion Testnet address (e.g., `xion1...`).
- `BABYLON_ADDRESS`: Your Babylon Testnet address (e.g., `bbn1...`).

Example `.env`:
```env
PRIVATE_KEY=0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
XION_ADDRESS=xion1exampleaddresshere
BABYLON_ADDRESS=bbn1exampleaddresshere
```

### Transaction Amounts
Default transaction amounts are set in `union.py` and can be modified:
```python
self.sepolia_amount = 0.0001  # ETH for Sepolia transfers
self.holesky_amount = 0.0001  # ETH for Holesky transfers
self.sei_amount = 0.01        # SEI for Sei transfers
self.corn_amount = 0.0000001  # BTCN for Bitcorn transfers
```

### Delay Between Transactions
Adjust the delay between transactions (in seconds) in `union.py`:
```python
self.min_delay = 1  # Minimum delay
self.max_delay = 1  # Maximum delay
```

### RPC Endpoints
The bot uses the following RPC URLs, which can be updated in `union.py` if needed:
```python
self.SEPOLIA_RPC_URL = "https://sepolia.drpc.org/"
self.HOLESKY_RPC_URL = "https://ethereum-holesky-rpc.publicnode.com/"
self.SEI_RPC_URL = "https://evm-rpc-testnet.sei-apis.com/"
self.CORN_RPC_URL = "https://21000001.rpc.thirdweb.com/"
```

## Troubleshooting

- **Error: `'SignedTransaction' object has no attribute 'raw_transaction'`**:
  - Ensure you’re using `web3.py` version 6.0.0 or higher:
    ```bash
    pip install --upgrade web3
    ```
  - The bot uses `rawTransaction` (correct for `web3.py` v6+). If using an older version, downgrade to `web3==5.31.4` or update the code to use `raw_transaction`.

- **Error: Insufficient Funds**:
  - Verify you have enough testnet tokens for the transaction amount and gas fees.
  - Obtain testnet tokens from faucets for Sepolia, Holesky, Sei, or Bitcorn.

- **Error: Invalid RPC**:
  - Check the RPC URLs in `union.py`. Replace with alternative endpoints if needed (e.g., Alchemy, Infura).
  - Ensure your internet connection is stable.

- **Error: Invalid Private Key or Address**:
  - Double-check the `.env` file for correct formatting and valid EVM private key, Xion, and Babylon addresses.

- **Transaction Fails or Reverts**:
  - Verify the `UCS03_ROUTER_ADDRESS` and contract ABI in `union.py`.
  - Check the Union Testnet documentation for any updates to contract addresses or parameters.

- **Need Help?**:
  - Join the official Union Testnet community (e.g., Discord or Telegram) for support.
  - Open an issue on this repository with detailed logs.

## Contributing

Contributions are welcome! 🎉 To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a Pull Request with a clear description of your changes.

Please ensure your code follows PEP 8 style guidelines and includes appropriate comments.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This bot is for **educational purposes only** and should be used on testnet networks. The developers are not responsible for any financial losses, account suspensions, or other consequences resulting from the use of this bot. Always audit the code and use it at your own risk.

---

## Support

If you find this project helpful, give it a ⭐ on GitHub! For questions, issues, or feature requests, contact me via [GitHub Issues](https://github.com/Kazuha787/Union-Auto-Bot/issues) or join the community on [Telegram: @Offical_Im_kazuha](https://t.me/Offical_Im_kazuha).[](https://github.com/Kazuha787)

---

### Notes for You
- **File Structure**: The file structure in the README reflects the provided code (`main.py`, `union.py`, `ui.py`, `utils.py`) and includes standard files like `.env.example` and `requirements.txt` for clarity. If your repository has additional files, let me know, and I can update the structure.
- **Customization**: The README is tailored to your GitHub profile (Kazuha787) and includes a Telegram link based on your other projects (e.g., Pharos-Auto-Bot). Update the Telegram handle if it’s incorrect.
- **Visual Appeal**: Added badges, emojis, and clear sections to make the README professional and engaging.
- **Troubleshooting**: Included a fix for the `raw_transaction` error you encountered, ensuring compatibility with `web3.py` v6+.
- **Assumptions**: Assumed the presence of `.env.example` and `requirements.txt`. If these don’t exist, you can create them:
  - `requirements.txt`:
    ```text
    web3>=6.0.0
    eth-utils
    eth-abi
    eth-account
    aiohttp
    python-dotenv
    rich
    ```
  - `.env.example`:
    ```env
    PRIVATE_KEY=
    XION_ADDRESS=
    BABYLON_ADDRESS=
    ```
