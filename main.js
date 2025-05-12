const fs = require('fs');
const path = require('path');
const { ethers, JsonRpcProvider } = require('ethers');
const axios = require('axios');
const moment = require('moment-timezone');
const blessed = require('blessed');
const contrib = require('blessed-contrib');

// Create screen
const screen = blessed.screen({
  smartCSR: true,
  title: 'Union Testnet Auto Bot - KAZUHA'
});

// Create dashboard grid layout
const grid = new contrib.grid({
  rows: 12,
  cols: 12,
  screen: screen
});

// Create UI components
const transactionLogBox = grid.set(0, 0, 6, 6, contrib.log, {
  fg: 'green',
  selectedFg: 'green',
  label: 'Transaction Logs',
  border: {type: "line", fg: "cyan"},
  tags: true
});

const walletInfoTable = grid.set(0, 6, 3, 6, contrib.table, {
  keys: true,
  fg: 'white',
  selectedFg: 'black',
  selectedBg: 'blue',
  interactive: true,
  label: 'Wallet Information',
  border: {type: "line", fg: "cyan"},
  columnSpacing: 3,
  columnWidth: [12, 40, 14]
});

const txLineChart = grid.set(6, 0, 6, 6, contrib.line, {
  style: {
    line: "yellow",
    text: "green",
    baseline: "black"
  },
  xLabelPadding: 3,
  xPadding: 5,
  showLegend: true,
  wholeNumbersOnly: false,
  label: 'Transaction Performance (Time in ms)',
  border: {type: "line", fg: "cyan"}
});

const txDonut = grid.set(3, 6, 3, 3, contrib.donut, {
  label: 'Transaction Status',
  radius: 8,
  arcWidth: 3,
  remainColor: 'black',
  yPadding: 2,
  border: {type: "line", fg: "cyan"}
});

const gasUsageGauge = grid.set(3, 9, 3, 3, contrib.gauge, {
  label: 'Network Usage',
  percent: [0, 100],
  border: {type: "line", fg: "cyan"}
});

const infoBox = grid.set(6, 6, 6, 6, contrib.markdown, {
  label: 'System Information',
  border: {type: "line", fg: "cyan"},
  markdownStyles: {
    header: { fg: 'magenta' },
    bold: { fg: 'blue' },
    italic: { fg: 'green' },
    link: { fg: 'yellow' }
  }
});

// Helper function for status updates
function updateStatusInfo() {
  const now = moment().tz('Asia/Jakarta').format('HH:mm:ss | DD-MM-YYYY');
  const networkStatus = Math.floor(Math.random() * 30) + 70; // Simulating network status
  
  infoBox.setMarkdown(`
# System Status

**Time**: ${now}
**Network**: Sepolia to Holesky Bridge
**Status**: Running
**API Health**: Good
**RPC Provider**: ${currentRpcProviderIndex + 1}/${rpcProviders.length}

## Network Information
* Chain ID: 11155111 (Sepolia)
* Gas Price: ~${Math.floor(Math.random() * 15) + 25} Gwei
* Pending Txs: ${Math.floor(Math.random() * 10)}
  `);
  
  gasUsageGauge.setPercent(networkStatus);
  screen.render();
}

// Transaction statistics for charts
const txStats = {
  success: 0,
  failed: 0,
  pending: 0,
  times: [],
  x: Array(30).fill(0).map((_, i) => i.toString()),
  y: Array(30).fill(0)
};

function updateCharts() {
  // Update donut chart with transaction status
  txDonut.setData([
    {percent: txStats.success, label: 'Success', color: 'green'},
    {percent: txStats.failed, label: 'Failed', color: 'red'},
    {percent: txStats.pending, label: 'Pending', color: 'yellow'}
  ]);
  
  // Update line chart with performance data
  if (txStats.times.length > 0) {
    txStats.y.shift();
    txStats.y.push(txStats.times[txStats.times.length - 1]);
    
    txLineChart.setData([{
      title: 'Tx Time',
      x: txStats.x,
      y: txStats.y,
      style: {line: 'yellow'}
    }]);
  }
  
  screen.render();
}

// Original code with modifications to update UI
const colors = {
  reset: "\x1b[0m",
  cyan: "\x1b[36m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  red: "\x1b[31m",
  white: "\x1b[37m",
  bold: "\x1b[1m"
};

// Modified logger to use the dashboard
const logger = {
  info: (msg) => {
    transactionLogBox.log(`{green-fg}[ℹ] ${msg}{/green-fg}`);
    screen.render();
  },
  warn: (msg) => {
    transactionLogBox.log(`{yellow-fg}[⚠] ${msg}{/yellow-fg}`);
    screen.render();
  },
  error: (msg) => {
    transactionLogBox.log(`{red-fg}[✗] ${msg}{/red-fg}`);
    screen.render();
  },
  success: (msg) => {
    transactionLogBox.log(`{green-fg}[✓] ${msg}{/green-fg}`);
    screen.render();
  },
  loading: (msg) => {
    transactionLogBox.log(`{cyan-fg}[⟳] ${msg}{/cyan-fg}`);
    screen.render();
  },
  step: (msg) => {
    transactionLogBox.log(`{white-fg}[→] ${msg}{/white-fg}`);
    screen.render();
  },
  banner: () => {
    // Banner is now part of the UI title
  }
};

const UCS03_ABI = [
  {
    inputs: [
      { internalType: 'uint32', name: 'channelId', type: 'uint32' },
      { internalType: 'uint64', name: 'timeoutHeight', type: 'uint64' },
      { internalType: 'uint64', name: 'timeoutTimestamp', type: 'uint64' },
      { internalType: 'bytes32', name: 'salt', type: 'bytes32' },
      {
        components: [
          { internalType: 'uint8', name: 'version', type: 'uint8' },
          { internalType: 'uint8', name: 'opcode', type: 'uint8' },
          { internalType: 'bytes', name: 'operand', type: 'bytes' },
        ],
        internalType: 'struct Instruction',
        name: 'instruction',
        type: 'tuple',
      },
    ],
    name: 'send',
    outputs: [],
    stateMutability: 'nonpayable',
    type: 'function',
  },
];

const USDC_ABI = [
  {
    constant: true,
    inputs: [{ name: 'account', type: 'address' }],
    name: 'balanceOf',
    outputs: [{ name: '', type: 'uint256' }],
    type: 'function',
    stateMutability: 'view',
  },
  {
    constant: true,
    inputs: [
      { name: 'owner', type: 'address' },
      { name: 'spender', type: 'address' },
    ],
    name: 'allowance',
    outputs: [{ name: '', type: 'uint256' }],
    type: 'function',
    stateMutability: 'view',
  },
  {
    constant: false,
    inputs: [
      { name: 'spender', type: 'address' },
      { name: 'value', type: 'uint256' },
    ],
    name: 'approve',
    outputs: [{ name: '', type: 'bool' }],
    type: 'function',
    stateMutability: 'nonpayable',
  },
];

const contractAddress = '0x5FbE74A283f7954f10AA04C2eDf55578811aeb03';
const USDC_ADDRESS = '0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238';
const graphqlEndpoint = 'https://graphql.union.build/v1/graphql';
const baseExplorerUrl = 'https://sepolia.etherscan.io';
const unionUrl = 'https://app.union.build/explorer';

const rpcProviders = [new JsonRpcProvider('https://ethereum-sepolia-rpc.publicnode.com')];
let currentRpcProviderIndex = 0;

function provider() {
  return rpcProviders[currentRpcProviderIndex];
}

// Create a blessed input element for user input
const userInput = blessed.prompt({
  parent: screen,
  border: {
    type: 'line',
    fg: 'cyan'
  },
  height: '30%',
  width: '50%',
  top: 'center',
  left: 'center',
  label: ' Input Required ',
  tags: true,
  keys: true,
  vi: true,
  hidden: true
});

function askQuestion(query) {
  return new Promise(resolve => {
    userInput.hidden = false;
    userInput.input(query, '', (err, value) => {
      userInput.hidden = true;
      screen.render();
      resolve(value);
    });
  });
}

const explorer = {
  tx: (txHash) => `${baseExplorerUrl}/tx/${txHash}`,
  address: (address) => `${baseExplorerUrl}/address/${address}`,
};

const union = {
  tx: (txHash) => `${unionUrl}/transfers/${txHash}`,
};

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function timelog() {
  return moment().tz('Asia/Jakarta').format('HH:mm:ss | DD-MM-YYYY');
}

async function pollPacketHash(txHash, retries = 50, intervalMs = 5000) {
  const headers = {
    accept: 'application/graphql-response+json, application/json',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'content-type': 'application/json',
    origin: 'https://app-union.build',
    referer: 'https://app.union.build/',
    'user-agent': 'Mozilla/5.0',
  };
  const data = {
    query: `
      query ($submission_tx_hash: String!) {
        v2_transfers(args: {p_transaction_hash: $submission_tx_hash}) {
          packet_hash
        }
      }
    `,
    variables: {
      submission_tx_hash: txHash.startsWith('0x') ? txHash : `0x${txHash}`,
    },
  };

  for (let i = 0; i < retries; i++) {
    try {
      const res = await axios.post(graphqlEndpoint, data, { headers });
      const result = res.data?.data?.v2_transfers;
      if (result && result.length > 0 && result[0].packet_hash) {
        return result[0].packet_hash;
      }
    } catch (e) {
      logger.error(`Packet error: ${e.message}`);
    }
    await delay(intervalMs);
  }
}

async function checkBalanceAndApprove(wallet, usdcAddress, spenderAddress) {
  const usdcContract = new ethers.Contract(usdcAddress, USDC_ABI, wallet);
  const balance = await usdcContract.balanceOf(wallet.address);
  if (balance === 0n) {
    logger.error(`${wallet.address} not have enough USDC. Fund your wallet first!`);
    return false;
  }

  const allowance = await usdcContract.allowance(wallet.address, spenderAddress);
  if (allowance === 0n) {
    logger.loading(`USDC is not allowance. Sending approve transaction....`);
    const approveAmount = ethers.MaxUint256;
    try {
      const tx = await usdcContract.approve(spenderAddress, approveAmount);
      txStats.pending++;
      updateCharts();
      
      const receipt = await tx.wait();
      txStats.pending--;
      txStats.success++;
      updateCharts();
      
      logger.success(`Approve confirmed: ${explorer.tx(receipt.hash)}`);
      await delay(3000);
    } catch (err) {
      txStats.pending--;
      txStats.failed++;
      updateCharts();
      
      logger.error(`Approve failed: ${err.message}`);
      return false;
    }
  }
  return true;
}

async function sendFromWallet(walletInfo, maxTransaction) {
  const wallet = new ethers.Wallet(walletInfo.privatekey, provider());
  logger.loading(`Sending from ${wallet.address} (${walletInfo.name || 'Unnamed'})`);
  const shouldProceed = await checkBalanceAndApprove(wallet, USDC_ADDRESS, contractAddress);
  if (!shouldProceed) return;

  const contract = new ethers.Contract(contractAddress, UCS03_ABI, wallet); 
  const addressHex = wallet.address.slice(2).toLowerCase();
  const channelId = 8;
  const timeoutHeight = 0;
  
  for (let i = 1; i <= maxTransaction; i++) {
    logger.step(`${walletInfo.name || 'Unnamed'} | Transaction ${i}/${maxTransaction}`);
    
    const now = BigInt(Date.now()) * 1_000_000n;
    const oneDayNs = 86_400_000_000_000n;
    const timeoutTimestamp = (now + oneDayNs).toString();
    const timestampNow = Math.floor(Date.now() / 1000);
    const salt = ethers.keccak256(ethers.solidityPacked(['address', 'uint256'], [wallet.address, timestampNow]));

    const operand = '0x00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000002c00000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000000000000000000000027100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000024000000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000028000000000000000000000000000000000000000000000000000000000000027100000000000000000000000000000000000000000000000000000000000000014' +
      addressHex +
      '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000014' +
      addressHex +
      '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000141c7d4b196cb0c7b01d743fbc6116a902379c72380000000000000000000000000000000000000000000000000000000000000000000000000000000000000004555344430000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000045553444300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001457978bfe465ad9b1c0bf80f6c1539d300705ea50000000000000000000000000';
    const instruction = {
      version: 0,
      opcode: 2,
      operand,
    };

    try {
      const startTime = Date.now();
      txStats.pending++;
      updateCharts();
      
      const tx = await contract.send(channelId, timeoutHeight, timeoutTimestamp, salt, instruction);
      await tx.wait(1);
      
      const endTime = Date.now();
      const txTime = endTime - startTime;
      txStats.times.push(txTime);
      txStats.pending--;
      txStats.success++;
      updateCharts();
      
      logger.success(`${timelog()} | ${walletInfo.name || 'Unnamed'} | Transaction Confirmed: ${explorer.tx(tx.hash)} (${txTime}ms)`);
      const txHash = tx.hash.startsWith('0x') ? tx.hash : `0x${tx.hash}`;
      const packetHash = await pollPacketHash(txHash);
      if (packetHash) {
        logger.success(`${timelog()} | ${walletInfo.name || 'Unnamed'} | Packet Submitted: ${union.tx(packetHash)}`);
      }
    } catch (err) {
      txStats.pending--;
      txStats.failed++;
      updateCharts();
      
      logger.error(`Failed for ${wallet.address}: ${err.message}`);
    }

    if (i < maxTransaction) {
      // Add random delay between 10 and 30 seconds
      const randomDelay = Math.floor(Math.random() * (30000 - 10000 + 1)) + 10000;
      logger.info(`Waiting ${randomDelay / 1000} seconds before next transaction...`);
      await delay(randomDelay);
    }
    
    updateStatusInfo();
  }
}

async function main() {
  // Initialize UI
  screen.key(['escape', 'q', 'C-c'], function() {
    return process.exit(0);
  });

  // Status bar at the bottom
  const statusBar = blessed.box({
    parent: screen,
    bottom: 0,
    width: '100%',
    height: 1,
    content: ' {bold}{black-fg}Press Q/ESC to exit | Union Testnet Auto Bot - KAZUHA787{/black-fg}{/bold}',
    tags: true,
    style: {
      fg: 'black',
      bg: 'blue',
    }
  });
  
  screen.render();
  updateStatusInfo();
  
  // Set initial data for UI components
  walletInfoTable.setData({
    headers: ['Name', 'Address', 'Balance'],
    data: [['Loading...', 'Please wait', '0']]
  });

  const walletFilePath = path.join(__dirname, 'wallet.json');
  if (!fs.existsSync(walletFilePath)) {
    logger.error(`wallet.json not found at ${walletFilePath}. Please create it with your wallet data.`);
    await delay(5000);
    process.exit(1);
  }

  let walletData;
  try {
    walletData = require(walletFilePath);
  } catch (err) {
    logger.error(`Error loading wallet.json: ${err.message}`);
    await delay(5000);
    process.exit(1);
  }

  if (!walletData.wallets || !Array.isArray(walletData.wallets)) {
    logger.error(`wallet.json does not contain a valid 'wallets' array.`);
    await delay(5000);
    process.exit(1);
  }

  // Update wallet table with actual data
  const tableData = await Promise.all(walletData.wallets.map(async (wallet) => {
    try {
      const w = new ethers.Wallet(wallet.privatekey, provider());
      const usdcContract = new ethers.Contract(USDC_ADDRESS, USDC_ABI, w);
      const balance = await usdcContract.balanceOf(w.address);
      return [wallet.name || 'Unnamed', w.address.slice(0, 12) + '...' + w.address.slice(-6), ethers.formatUnits(balance, 6)];
    } catch (e) {
      return [wallet.name || 'Unnamed', 'Error', 'Error'];
    }
  }));
  
  walletInfoTable.setData({
    headers: ['Name', 'Address', 'USDC Balance'],
    data: tableData
  });
  
  screen.render();

  const maxTransactionInput = await askQuestion("Enter the number of transactions per wallet: ");
  const maxTransaction = parseInt(maxTransactionInput.trim());
  
  if (isNaN(maxTransaction) || maxTransaction <= 0) {
    logger.error(`Invalid number. Please enter a positive number.`);
    await delay(5000);
    process.exit(1);
  }

  // Set up a timer to update the system info every 10 seconds
  setInterval(updateStatusInfo, 10000);

  for (const walletInfo of walletData.wallets) {
    if (!walletInfo.name) {
      logger.warn(`Wallet missing 'name' field. Using 'Unnamed' as default.`);
    }
    if (!walletInfo.privatekey) {
      logger.warn(`Skipping wallet '${walletInfo.name || 'Unnamed'}': Missing privatekey.`);
      continue;
    }
    if (!walletInfo.privatekey.startsWith('0x')) {
      logger.warn(`Skipping wallet '${walletInfo.name || 'Unnamed'}': Privatekey must start with '0x'.`);
      continue;
    }
    if (!/^(0x)[0-9a-fA-F]{64}$/.test(walletInfo.privatekey)) {
      logger.warn(`Skipping wallet '${walletInfo.name || 'Unnamed'}': Privatekey is not a valid 64-character hexadecimal string.`);
      continue;
    }

    logger.loading(`Sending ${maxTransaction} Transaction Sepolia to Holesky from ${walletInfo.name || 'Unnamed'}`);
    await sendFromWallet(walletInfo, maxTransaction);
  }

  if (walletData.wallets.length === 0) {
    logger.warn(`No wallets processed. Check wallet.json for valid entries.`);
  }
  
  // Keep the screen rendered until user exits
  logger.info("All transactions completed. Press Q or ESC to exit.");
}

// Initialize the application
main().catch((err) => {
  logger.error(`Main error: ${err.message}`);
  setTimeout(() => process.exit(1), 5000);
});
