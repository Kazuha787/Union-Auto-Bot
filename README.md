

![IMG_20250709_232943_431](https://github.com/user-attachments/assets/815be46d-3640-46f7-b42f-957007a711bf)







# 🚀 Union V3.5 Comple 150 Stars And 50 Forks I will Drop Asap 🌌

**Union Auto Bot** is a cutting-edge Node.js automation tool crafted for seamless cross-chain token transfers on testnet networks like SEI, XION, Babylon, Corn, Sepolia, and Holesky. With a sleek command-line interface (CLI) and robust functionality, it empowers users to execute token swaps effortlessly using the Union protocol. Whether you're a developer testing interoperability or a blockchain enthusiast exploring testnets, this bot is your ultimate companion! 🛠️

> ⚠️ **Important**: This tool is for **testnet use only**. Ensure you have testnet tokens for gas and transfers. Use responsibly!

---

## ✨ Key Features

- **Cross-Chain Magic** 🌍: Transfer tokens between SEI, XION, Babylon, and destinations like Corn, Sepolia, and Holesky.
- **Interactive CLI** 🖥️: Navigate a vibrant menu with arrow keys and Enter to select options.
- **Flexible Token Support** 💰: Swap native tokens (SEI, XION, BBN) or stablecoins (USDC).
- **Customizable Transfers** ⚙️: Set transfer amounts, transaction counts, and delays with ease.
- **Real-Time Feedback** 📊: Enjoy a loading spinner, color-coded outputs, and transaction summaries.
- **Error Resilience** 🛡️: Handles wallet misconfigurations, insufficient balances, and network hiccups gracefully.
- **Transaction Insights** 🔍: View transaction hashes, packet hashes, and block explorer links for transparency.
- **Wallet Integration** 🔐: Supports EVM (SEI) and Cosmos (XION, Babylon) wallets for secure operations.

---

## 🌐 Supported Networks & Destinations

| Network       | Chain ID         | RPC Endpoint                              | Denom  | Gas Price       |
|---------------|------------------|-------------------------------------------|--------|-----------------|
| SEI Testnet   | 1328             | `https://evm-rpc-testnet.sei-apis.com`    | SEI    | Dynamic         |
| XION Testnet  | `xion-testnet-2` | `https://rpc.xion-testnet-2.burnt.com/`   | uxion  | 0.025uxion      |
| Babylon Testnet | `bbn-test-3`   | `https://babylon-testnet-rpc.nodes.guru`  | ubbn   | 0.0025ubbn      |

### 🎯 Transfer Destinations
- **Corn** 🍿: Channel ID 3, Token Address: `e53dcec07d16d88e386ae0710e86d9a400f83c31`
- **Sepolia** 🧪: Channel ID 1, Token Address: `bd030914ab8d7ab1bd626f09e47c7cc2881550a3`
- **Holesky** 🕳️: Channel ID 2, Token Address: `77b99a27a5fed3bc8fb3e2f1063181f82ec48637`

---

## 🛠️ Prerequisites

Before diving in, ensure you have:

- **Node.js** (v16+): [Download here](https://nodejs.org/) 📦
- **npm**: Comes with Node.js
- **Testnet Wallets**: Private keys for SEI, XION, and Babylon with testnet funds
- **Testnet Tokens**: Grab tokens from testnet faucets for gas and transfers 💧
- **Git**: For cloning the repository [Install Git](https://git-scm.com/)

---

## 📥 Installation

1. **Clone the Repository** 🐙:
   ```bash
   git clone https://github.com/Kazuha787/Union-Auto-Bot.git
   cd Union-Auto-Bot
   ```

2. **Install Dependencies** 📚:
   ```bash
   npm install
   ```

   Key dependencies include:
   - `ethers`: Ethereum-compatible transactions
   - `@cosmjs/proto-signing`, `@cosmjs/stargate`: Cosmos SDK support
   - `axios`: GraphQL queries for packet hashes
   - `viem`: Hex conversions
   - `crypto`: Random salt generation
   - `readline`: CLI input handling

3. **Configure Wallets** 🔑:
   - Create a `wallet.json` file in the project root:
     ```json
     {
       "wallets": [
         {
           "sei_privatekey": "0xYourSeiPrivateKey",
           "xion_privatekey": "0xYourXionPrivateKey",
           "babylon_privatekey": "0xYourBabylonPrivateKey",
           "babylon_address": "bbnYourBabylonAddress"
         }
       ]
     }
     ```
   - **Pro Tip**: Use testnet private keys only and ensure sufficient funds.

4. **Union Instruction Builder** 🧩:
   - The bot requires `union-instruction-builder.js` for token configs and messages. If missing, a placeholder is used. For custom logic, add `union-instruction-builder.js` with:
     - `getTokenConfig(type)`: Returns token details (e.g., USDC, XION)
     - `createSendMessage(params)`: Builds Cosmos transfer messages

---

## 🚀 Usage

1. **Launch the Bot**:
   ```bash
   node main.js
   ```

2. **Navigate the Menu** 🎮:
   - Use **Up** ⬆️ and **Down** ⬇️ arrow keys to highlight options.
   - Press **Enter** ⏎ to select.
   - Menu options:
     - 🌉 **SEI to XION SWAP**
     - 🌽 **SEI to CORN SWAP**
     - 🏛️ **XION to Babylon SWAP**
     - 🌐 **Babylon to Others SWAPS**
     - 🚪 **Exit**

3. **Configure Transfers** 🛠️:
   - **SEI to XION/CORN**:
     - Amount: Enter SEI amount (default: 0.0001 SEI)
     - Count: Number of transfers (default: 1)
   - **XION to Babylon**:
     - Token: Choose USDC or XION
     - Amount: Token amount (e.g., 0.01)
     - Count: Number of transfers (default: 1)
   - **Babylon to Others**:
     - Destination: Select Corn, Sepolia, or Holesky
     - Amount: BBN amount (e.g., 0.001)
     - Count: Number of transfers (default: 1)
     - Delay: Seconds between transactions (default: 0)

4. **Track Progress** 📡:
   - Watch the CLI for:
     - Transaction hashes with block explorer links (e.g., [seitrace.com](https://seitrace.com))
     - Packet hashes (polled via GraphQL)
     - Color-coded status: 🟢 Success, 🔴 Failure
   - A detailed summary shows successful/failed transfers and hashes.

5. **Exit Gracefully**:
   - Select **Exit** or press **Ctrl+C** to stop the bot. 🛑

---

## ⚙️ Advanced Configuration

### Network Settings
Modify network configurations in the script if needed:
- **XION Testnet**:
  ```javascript
  const XION_TESTNET = {
    chainId: "xion-testnet-2",
    rpcEndpoint: "https://rpc.xion-testnet-2.burnt.com/",
    prefix: "xion",
    denom: "uxion",
    gasPrice: GasPrice.fromString("0.025uxion")
  };
  ```
- **Babylon Testnet**:
  ```javascript
  const BABYLON_TESTNET = {
    chainId: "bbn-test-3",
    rpcEndpoint: "https://babylon-testnet-rpc.nodes.guru",
    prefix: "bbn",
    denom: "ubbn",
    gasPrice: GasPrice.fromString("0.0025ubbn")
  };
  ```
- **SEI Testnet**:
  ```javascript
  const provider = new ethers.JsonRpcProvider("https://evm-rpc-testnet.sei-apis.com");
  ```

### Customizing Destinations
Update `DESTINATIONS` to add or modify transfer destinations:
```javascript
const DESTINATIONS = {
  corn: { name: "Corn", channelId: 3, tokenAddress: "e53dcec07d16d88e386ae0710e86d9a400f83c31" },
  sepolia: { name: "Sepolia", channelId: 1, tokenAddress: "bd030914ab8d7ab1bd626f09e47c7cc2881550a3" },
  holesky: { name: "Holesky", channelId: 2, tokenAddress: "77b99a27a5fed3bc8fb3e2f1063181f82ec48637" }
};
```

### Gas and Fees
- **SEI**: Dynamic gas pricing using `provider.getFeeData()`.
- **XION**: Fixed gas of 696861 and 697 uxion per transfer.
- **Babylon**: Fixed gas of 500000 and 1000 ubbn per transfer.

---

## 🛡️ Error Handling

The bot is built to handle errors gracefully:
- **Wallet Errors** 🚫: Validates private keys and addresses in `wallet.json`.
- **Balance Checks** 💸: Ensures sufficient tokens and gas before transfers.
- **Network Failures** 🌐: Retries packet hash queries (50 attempts, 5s delay).
- **User Input** ⌨️: Validates amounts, counts, and delays with clear error messages.
- **Transaction Failures** 🔴: Logs detailed errors and continues with remaining transfers.

Errors are displayed in red with prompts to continue, ensuring a smooth experience.

---

## 🧑‍💻 Contributing

We love contributions! Here's how to get started:

1. **Fork the Repo** 🍴: [https://github.com/Kazuha787/Union-Auto-Bot](https://github.com/Kazuha787/Union-Auto-Bot)
2. **Create a Branch** 🌿:
   ```bash
   git checkout -b feature/your-awesome-feature
   ```
3. **Make Changes** ✍️: Add features, fix bugs, or improve docs.
4. **Commit** 📝:
   ```bash
   git commit -m "Add your awesome feature"
   ```
5. **Push** 🚀:
   ```bash
   git push origin feature/your-awesome-feature
   ```
6. **Submit a Pull Request** 📬: Include a clear description of your changes.

**Contribution Ideas**:
- Add support for new testnet networks 🌐
- Enhance the CLI with progress bars or ASCII art 🎨
- Implement batch transaction optimization ⚡
- Improve error logging with file outputs 📄

---

## 🌟 Community & Support

Join our vibrant community for help and updates:
- **Telegram** 📩: [t.me/Offical_Im_kazuha](https://t.me/Offical_Im_kazuha)
- **GitHub Issues** 🐞: Report bugs or suggest features [here](https://github.com/Kazuha787/Union-Auto-Bot/issues)
- **Discussions** 💬: Share ideas in the [GitHub Discussions](https://github.com/Kazuha787/Union-Auto-Bot/discussions)

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details. 📄

---

## ⚠️ Disclaimer

**Union Auto Bot** is for **testnet environments only**. Using it on mainnet may lead to loss of funds. The author is not liable for any misuse or unintended consequences. Always verify wallet configurations and test thoroughly. 🛑

---

## 🙌 Acknowledgments

- **Union Protocol**: For enabling cross-chain interoperability
- **Cosmos SDK & Ethers.js**: For robust blockchain interactions
- **Community**: For feedback and support on Telegram

---

**Built with 💖 by Kazuha**  
📍 [GitHub](https://github.com/Kazuha787) | 📩 [Telegram](https://t.me/Offical_Im_kazuha)

> Let's conquer the testnet together! 🚀

---

### Enhancements in This README

1. **Visual Appeal**:
   - Added emojis (🚀, 🌌, 🛠️, etc.) for engagement.
   - Used modern Markdown formatting with tables, badges, and callouts.
   - Color-coded CLI feedback mirrored in documentation (🟢, 🔴).

2. **Advanced Sections**:
   - Added **Supported Networks & Destinations** with a table.
   - Included **Advanced Configuration** for developers.
   - Expanded **Contributing** with specific ideas.
   - Added **Acknowledgments** for a professional touch.

3. **User-Friendly**:
   - Clear installation steps with code blocks and links.
   - Detailed usage instructions with menu navigation.
   - Comprehensive error handling section.

4. **Professional Tone**:
   - Maintained a balance between technical accuracy and accessibility.
   - Included a disclaimer for legal clarity.
   - Linked to community resources for support.

To use this README, create a `README.md` file in your repository and paste the content above. If you need a `LICENSE` file or further customization (e.g., badges for build status, npm version), let me know! 😊
