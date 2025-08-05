import asyncio
import json
import time
import random
from web3 import Web3
from eth_utils import keccak
from eth_abi.abi import encode
from aiohttp import ClientSession, ClientTimeout
from ui import logger_error, logger_success, logger_info, logger_loading, logger_step, logger_warn
from utils import pad_hex, encode_hex_as_string, encode_string_as_bytes

class Union:
    def __init__(self) -> None:
        self.GRAPHQL_API = "https://graphql.union.build/v1/graphql"
        self.SEPOLIA_RPC_URL = "https://sepolia.drpc.org/"
        self.HOLESKY_RPC_URL = "https://ethereum-holesky-rpc.publicnode.com/"
        self.SEI_RPC_URL = "https://evm-rpc-testnet.sei-apis.com/"
        self.CORN_RPC_URL = "https://21000001.rpc.thirdweb.com/"
        self.UCS03_ROUTER_ADDRESS = "0x5FbE74A283f7954f10AA04C2eDf55578811aeb03"
        self.BASE_TOKEN_ADDRESS = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
        self.ERC20_CONTRACT_ABI = json.loads('''[
            {"type":"function","name":"balanceOf","stateMutability":"view","inputs":[{"name":"address","type":"address"}],"outputs":[{"name":"","type":"uint256"}]}
        ]''')
        self.UCS03_CONTRACT_ABI = [
            {
                "inputs": [
                    { "internalType": "uint32", "name": "channelId", "type": "uint32" },
                    { "internalType": "uint64", "name": "timeoutHeight", "type": "uint64" },
                    { "internalType": "uint64", "name": "timeoutTimestamp", "type": "uint64" },
                    { "internalType": "bytes32", "name": "salt", "type": "bytes32" },
                    {
                        "components": [
                            { "internalType": "uint8", "name": "version", "type": "uint8" },
                            { "internalType": "uint8", "name": "opcode", "type": "uint8" },
                            { "internalType": "bytes", "name": "operand", "type": "bytes" },
                        ],
                        "internalType": "struct Instruction",
                        "name": "instruction",
                        "type": "tuple",
                    },
                ],
                "name": "send",
                "outputs": [],
                "stateMutability": "payable",
                "type": "function",
            },
        ]
        self.xion_address = {}
        self.babylon_address = {}
        self.used_rpc = 0
        self.tx_count = 0
        self.sepolia_amount = 0.0001
        self.holesky_amount = 0.0001
        self.sei_amount = 0.01
        self.corn_amount = 0.0000001
        self.min_delay = 1
        self.max_delay = 1

    async def get_web3_with_check(self, address: str, retries=3, timeout=60):
        request_kwargs = {"timeout": timeout}
        for attempt in range(retries):
            try:
                web3 = Web3(Web3.HTTPProvider(self.used_rpc, request_kwargs=request_kwargs))
                web3.eth.get_block_number()
                return web3
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(3)
                    continue
                raise Exception(f"Failed to Connect to RPC: {str(e)}")

    async def get_token_balance(self, address: str):
        try:
            web3 = await self.get_web3_with_check(address)
            balance = web3.eth.get_balance(address)
            token_balance = balance / (10 ** 18)
            return token_balance
        except Exception as e:
            logger_error(f"Failed to get balance: {str(e)}")
            return None

    def generate_instruction_data(self, address: str, amount: int, pair: str):
        try:
            if pair == "Sepolia Testnet to Holesky Testnet":
                quote_token = "0x92b3bc0bc3ac0ee60b04a0bbc4a09deb3914c886"
                operand = (
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(3) +
                    pad_hex(96) +
                    pad_hex(704) +
                    pad_hex(320) +
                    pad_hex(384) +
                    pad_hex(448) +
                    pad_hex(amount) +
                    pad_hex(512) +
                    pad_hex(576) +
                    pad_hex(18) +
                    pad_hex(0) +
                    pad_hex(640) +
                    pad_hex(amount) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(20) +
                    encode_hex_as_string(self.BASE_TOKEN_ADDRESS) +
                    pad_hex(3) +
                    encode_string_as_bytes("ETH", 32) +
                    pad_hex(5) +
                    encode_string_as_bytes("Ether", 32) +
                    pad_hex(20) +
                    encode_hex_as_string(quote_token)
                )

            elif pair == "Sepolia Testnet to Babylon Testnet":
                quote_token = "0x62626e313837656178666171656d67336e7466656e356a6b73656c77706b367636357a353438393266327070746c78356733703971736d73633967683463"
                operand = (
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(3) +
                    pad_hex(96) +
                    pad_hex(768) +
                    pad_hex(320) +
                    pad_hex(384) +
                    pad_hex(480) +
                    pad_hex(amount) +
                    pad_hex(544) +
                    pad_hex(608) +
                    pad_hex(18) +
                    pad_hex(0) +
                    pad_hex(672) +
                    pad_hex(amount) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(42) +
                    encode_string_as_bytes(self.babylon_address[address], 64) +
                    pad_hex(20) +
                    encode_hex_as_string(self.BASE_TOKEN_ADDRESS) +
                    pad_hex(3) +
                    encode_string_as_bytes("ETH", 32) +
                    pad_hex(5) +
                    encode_string_as_bytes("Ether", 32) +
                    pad_hex(62) +
                    encode_hex_as_string(quote_token, 64)
                )

            elif pair == "Holesky Testnet to Sepolia Testnet":
                quote_token = "0xf6e7e2725b40ec8226036906cab0f5dc3722b8e7"
                operand = (
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(3) +
                    pad_hex(96) +
                    pad_hex(704) +
                    pad_hex(320) +
                    pad_hex(384) +
                    pad_hex(448) +
                    pad_hex(amount) +
                    pad_hex(512) +
                    pad_hex(576) +
                    pad_hex(18) +
                    pad_hex(0) +
                    pad_hex(640) +
                    pad_hex(amount) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(20) +
                    encode_hex_as_string(self.BASE_TOKEN_ADDRESS) +
                    pad_hex(3) +
                    encode_string_as_bytes("ETH", 32) +
                    pad_hex(5) +
                    encode_string_as_bytes("Ether", 32) +
                    pad_hex(20) +
                    encode_hex_as_string(quote_token)
                )

            elif pair == "Holesky Testnet to Xion Testnet":
                quote_token = "0x78696f6e317863397661687972726d33676d6c39787338396b3866753933673366736d35326a686a636b6d6778727a6c617a66307376303571366e75756e65"
                operand = (
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(3) +
                    pad_hex(96) +
                    pad_hex(768) +
                    pad_hex(320) +
                    pad_hex(384) +
                    pad_hex(480) +
                    pad_hex(amount) +
                    pad_hex(544) +
                    pad_hex(608) +
                    pad_hex(18) +
                    pad_hex(0) +
                    pad_hex(672) +
                    pad_hex(amount) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(43) +
                    encode_string_as_bytes(self.xion_address[address], 64) +
                    pad_hex(20) +
                    encode_hex_as_string(self.BASE_TOKEN_ADDRESS) +
                    pad_hex(3) +
                    encode_string_as_bytes("ETH", 32) +
                    pad_hex(5) +
                    encode_string_as_bytes("Ether", 32) +
                    pad_hex(63) +
                    encode_hex_as_string(quote_token, 64)
                )

            elif pair == "Holesky Testnet to Babylon Testnet":
                quote_token = "0x62626e31766a6172726e72716d366e63346a36303964746537677771666363706461643963776474747973356432737a6a717770377274736c726e373636"
                operand = (
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(3) +
                    pad_hex(96) +
                    pad_hex(768) +
                    pad_hex(320) +
                    pad_hex(384) +
                    pad_hex(480) +
                    pad_hex(amount) +
                    pad_hex(544) +
                    pad_hex(608) +
                    pad_hex(18) +
                    pad_hex(0) +
                    pad_hex(672) +
                    pad_hex(amount) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(42) +
                    encode_string_as_bytes(self.babylon_address[address], 64) +
                    pad_hex(20) +
                    encode_hex_as_string(self.BASE_TOKEN_ADDRESS) +
                    pad_hex(3) +
                    encode_string_as_bytes("ETH", 32) +
                    pad_hex(5) +
                    encode_string_as_bytes("Ether", 32) +
                    pad_hex(62) +
                    encode_hex_as_string(quote_token, 64)
                )

            elif pair == "Sei Testnet to Xion Testnet":
                quote_token = "0x78696f6e31746d733932636d33346c786c6e346b76787732786473676e63756d7a6570723565326575673930766d74797735357a38646a757176776e656537"
                operand = (
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(3) +
                    pad_hex(96) +
                    pad_hex(768) +
                    pad_hex(320) +
                    pad_hex(384) +
                    pad_hex(480) +
                    pad_hex(amount) +
                    pad_hex(544) +
                    pad_hex(608) +
                    pad_hex(18) +
                    pad_hex(0) +
                    pad_hex(672) +
                    pad_hex(amount) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(43) +
                    encode_string_as_bytes(self.xion_address[address], 64) +
                    pad_hex(20) +
                    encode_hex_as_string(self.BASE_TOKEN_ADDRESS) +
                    pad_hex(3) +
                    encode_string_as_bytes("SEI", 32) +
                    pad_hex(3) +
                    encode_string_as_bytes("Sei", 32) +
                    pad_hex(63) +
                    encode_hex_as_string(quote_token, 64)
                )

            elif pair == "Sei Testnet to Bitcorn Testnet":
                quote_token = "0xe86bed5b0813430df660d17363b89fe9bd8232d8"
                operand = (
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(3) +
                    pad_hex(96) +
                    pad_hex(704) +
                    pad_hex(320) +
                    pad_hex(384) +
                    pad_hex(448) +
                    pad_hex(amount) +
                    pad_hex(512) +
                    pad_hex(576) +
                    pad_hex(18) +
                    pad_hex(0) +
                    pad_hex(640) +
                    pad_hex(amount) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(20) +
                    encode_hex_as_string(self.BASE_TOKEN_ADDRESS) +
                    pad_hex(3) +
                    encode_string_as_bytes("SEI", 32) +
                    pad_hex(3) +
                    encode_string_as_bytes("Sei", 32) +
                    pad_hex(20) +
                    encode_hex_as_string(quote_token)
                )

            elif pair == "Sei Testnet to Binance Smart Chain Testnet":
                quote_token = "0xe86bed5b0813430df660d17363b89fe9bd8232d8"
                operand = (
                    pad_hex(32) +
                    pad_hex(2) +
                    pad_hex(64) +
                    pad_hex(896) +
                    pad_hex(1) +
                    pad_hex(3) +
                    pad_hex(96) +
                    pad_hex(704) +
                    pad_hex(320) +
                    pad_hex(384) +
                    pad_hex(448) +
                    pad_hex(amount) +
                    pad_hex(512) +
                    pad_hex(576) +
                    pad_hex(18) +
                    pad_hex(0) +
                    pad_hex(640) +
                    pad_hex(amount) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(20) +
                    encode_hex_as_string(self.BASE_TOKEN_ADDRESS) +
                    pad_hex(3) +
                    encode_string_as_bytes("SEI", 32) +
                    pad_hex(3) +
                    encode_string_as_bytes("Sei", 32) +
                    pad_hex(20) +
                    encode_hex_as_string(quote_token) +
                    pad_hex(1) +
                    pad_hex(3) +
                    pad_hex(96) +
                    pad_hex(704) +
                    pad_hex(320) +
                    pad_hex(384) +
                    pad_hex(448) +
                    pad_hex(0) +
                    pad_hex(512) +
                    pad_hex(576) +
                    pad_hex(18) +
                    pad_hex(0) +
                    pad_hex(640) +
                    pad_hex(0) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(20) +
                    encode_hex_as_string(self.BASE_TOKEN_ADDRESS) +
                    pad_hex(3) +
                    encode_string_as_bytes("SEI", 32) +
                    pad_hex(3) +
                    encode_string_as_bytes("Sei", 32) +
                    pad_hex(20) +
                    encode_hex_as_string(quote_token)
                )

            elif pair == "Sei Testnet to Babylon Testnet":
                quote_token = "0x62626e313639686e61396c7a7474797067343765686175303468353465786d756c30723079396a37706c6178737767356e33646537666e716438776e7579"
                operand = (
                    pad_hex(32) +
                    pad_hex(2) +
                    pad_hex(64) +
                    pad_hex(960) +
                    pad_hex(1) +
                    pad_hex(3) +
                    pad_hex(96) +
                    pad_hex(768) +
                    pad_hex(320) +
                    pad_hex(384) +
                    pad_hex(480) +
                    pad_hex(amount) +
                    pad_hex(544) +
                    pad_hex(608) +
                    pad_hex(18) +
                    pad_hex(0) +
                    pad_hex(672) +
                    pad_hex(amount) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(42) +
                    encode_string_as_bytes(self.babylon_address[address], 64) +
                    pad_hex(20) +
                    encode_hex_as_string(self.BASE_TOKEN_ADDRESS) +
                    pad_hex(3) +
                    encode_string_as_bytes("SEI", 32) +
                    pad_hex(3) +
                    encode_string_as_bytes("Sei", 32) +
                    pad_hex(62) +
                    encode_hex_as_string(quote_token, 64) +
                    pad_hex(1) +
                    pad_hex(3) +
                    pad_hex(96) +
                    pad_hex(768) +
                    pad_hex(320) +
                    pad_hex(384) +
                    pad_hex(480) +
                    pad_hex(0) +
                    pad_hex(544) +
                    pad_hex(608) +
                    pad_hex(18) +
                    pad_hex(0) +
                    pad_hex(672) +
                    pad_hex(0) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(42) +
                    encode_string_as_bytes(self.babylon_address[address], 64) +
                    pad_hex(20) +
                    encode_hex_as_string(self.BASE_TOKEN_ADDRESS) +
                    pad_hex(3) +
                    encode_string_as_bytes("SEI", 32) +
                    pad_hex(3) +
                    encode_string_as_bytes("Sei", 32) +
                    pad_hex(62) +
                    encode_hex_as_string(quote_token, 64)
                )

            elif pair == "Bitcorn Testnet to Xion Testnet":
                quote_token = "0x78696f6e31683734366464796b396339796834666363757a6b636d65703839776d6b356e357a6b773735373237336d71636d75656d633338733278746d7466"
                operand = (
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(3) +
                    pad_hex(96) +
                    pad_hex(768) +
                    pad_hex(320) +
                    pad_hex(384) +
                    pad_hex(480) +
                    pad_hex(amount) +
                    pad_hex(544) +
                    pad_hex(608) +
                    pad_hex(18) +
                    pad_hex(0) +
                    pad_hex(672) +
                    pad_hex(amount) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(43) +
                    encode_string_as_bytes(self.xion_address[address], 64) +
                    pad_hex(20) +
                    encode_hex_as_string(self.BASE_TOKEN_ADDRESS) +
                    pad_hex(4) +
                    encode_string_as_bytes("BTCN", 32) +
                    pad_hex(7) +
                    encode_string_as_bytes("Bitcorn", 32) +
                    pad_hex(63) +
                    encode_hex_as_string(quote_token, 64)
                )

            elif pair == "Bitcorn Testnet to Sei Testnet":
                quote_token = "0x92b3bc0bc3ac0ee60b04a0bbc4a09deb3914c886"
                operand = (
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(3) +
                    pad_hex(96) +
                    pad_hex(704) +
                    pad_hex(320) +
                    pad_hex(384) +
                    pad_hex(448) +
                    pad_hex(amount) +
                    pad_hex(512) +
                    pad_hex(576) +
                    pad_hex(18) +
                    pad_hex(0) +
                    pad_hex(640) +
                    pad_hex(amount) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(20) +
                    encode_hex_as_string(self.BASE_TOKEN_ADDRESS) +
                    pad_hex(4) +
                    encode_string_as_bytes("BTCN", 32) +
                    pad_hex(7) +
                    encode_string_as_bytes("Bitcorn", 32) +
                    pad_hex(20) +
                    encode_hex_as_string(quote_token)
                )

            elif pair == "Bitcorn Testnet to Babylon Testnet":
                quote_token = "0x62626e3170397a68377032667866337471766b306d64716e613273706b6a6c3030713230616a77656a34386d7a6d38327a6e61356e74377339707732706c"
                operand = (
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(32) +
                    pad_hex(1) +
                    pad_hex(3) +
                    pad_hex(96) +
                    pad_hex(768) +
                    pad_hex(320) +
                    pad_hex(384) +
                    pad_hex(480) +
                    pad_hex(amount) +
                    pad_hex(544) +
                    pad_hex(608) +
                    pad_hex(18) +
                    pad_hex(0) +
                    pad_hex(672) +
                    pad_hex(amount) +
                    pad_hex(20) +
                    encode_hex_as_string(address) +
                    pad_hex(42) +
                    encode_string_as_bytes(self.babylon_address[address], 64) +
                    pad_hex(20) +
                    encode_hex_as_string(self.BASE_TOKEN_ADDRESS) +
                    pad_hex(4) +
                    encode_string_as_bytes("BTCN", 32) +
                    pad_hex(7) +
                    encode_string_as_bytes("Bitcorn", 32) +
                    pad_hex(62) +
                    encode_hex_as_string(quote_token, 64)
                )

            instruction = {
                "version": 0,
                "opcode": 2,
                "operand": "0x" + operand
            }
            return instruction
        except Exception as e:
            raise Exception(f"Generate Instruction Data Failed: {str(e)}")

    async def perform_send(self, private_key: str, address: str, tx_amount: float, pair: str):
        try:
            web3 = await self.get_web3_with_check(address)
            if pair == "Sepolia Testnet to Holesky Testnet":
                channel_id = 8
                fee = 1.5
            elif pair == "Sepolia Testnet to Babylon Testnet":
                channel_id = 7
                fee = 1.5
            elif pair == "Holesky Testnet to Sepolia Testnet":
                channel_id = 2
                fee = 0.001
            elif pair == "Holesky Testnet to Xion Testnet":
                channel_id = 4
                fee = 0.001
            elif pair == "Holesky Testnet to Babylon Testnet":
                channel_id = 3
                fee = 0.001
            elif pair == "Sei Testnet to Xion Testnet":
                channel_id = 1
                fee = 1.1
            elif pair == "Sei Testnet to Bitcorn Testnet":
                channel_id = 2
                fee = 1.1
            elif pair == "Sei Testnet to Binance Smart Chain Testnet":
                channel_id = 5
                fee = 1.1
            elif pair == "Sei Testnet to Babylon Testnet":
                channel_id = 4
                fee = 1.1
            elif pair == "Bitcorn Testnet to Xion Testnet":
                channel_id = 2
                fee = 0.01
            elif pair == "Bitcorn Testnet to Sei Testnet":
                channel_id = 3
                fee = 0.01
            elif pair == "Bitcorn Testnet to Babylon Testnet":
                channel_id = 1
                fee = 0.01
            amount = web3.to_wei(tx_amount, "ether")
            timeout_height = 0
            timeout_timestamp = int(time.time() * 1_000_000_000) + 86_400_000_000_000
            timestamp_now = int(time.time())
            encoded_data = keccak(encode(["address", "uint256"], [address, timestamp_now]))
            salt = "0x" + encoded_data.hex()
            instruction = self.generate_instruction_data(address, amount, pair)
            token_contract = web3.eth.contract(address=web3.to_checksum_address(self.UCS03_ROUTER_ADDRESS), abi=self.UCS03_CONTRACT_ABI)
            send_data = token_contract.functions.send(channel_id, timeout_height, timeout_timestamp, salt, instruction)
            estimated_gas = send_data.estimate_gas({"from": address, "value": amount})
            latest_block = web3.eth.get_block("latest")
            base_fee = latest_block.get("baseFeePerGas", 0)
            max_priority_fee = web3.to_wei(fee, "gwei")
            max_fee = base_fee + max_priority_fee
            send_tx = send_data.build_transaction({
                "from": address,
                "value": amount,
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": web3.eth.get_transaction_count(address, "pending"),
                "chainId": web3.eth.chain_id,
            })
            signed_tx = web3.eth.account.sign_transaction(send_tx, private_key)
            raw_tx = web3.eth.send_raw_transaction(signed_tx.rawTransaction)  # Updated to rawTransaction
            tx_hash = web3.to_hex(raw_tx)
            receipt = await asyncio.to_thread(web3.eth.wait_for_transaction_receipt, tx_hash, timeout=600)
            block_number = receipt.blockNumber
            return tx_hash, block_number
        except Exception as e:
            logger_error(f"Perform Send Failed: {str(e)}")
            return None, None

    async def print_timer(self):
        for remaining in range(random.randint(self.min_delay, self.max_delay), 0, -1):
            logger_loading(f"Waiting {remaining} Seconds For Next Tx...")
            await asyncio.sleep(1)

    def print_tx_count_question(self):
        while True:
            try:
                tx_count = int(input("How Many Times Do You Want To Make a Transfer? -> ").strip())
                if tx_count > 0:
                    self.tx_count = tx_count
                    break
                else:
                    logger_error("Please enter a positive number.")
            except ValueError:
                logger_error("Invalid input. Enter a number.")

    def print_question(self):
        while True:
            try:
                logger_info("\n╔════════════════════════════════════╗")
                logger_info("║      Select Transfer Option        ║")
                logger_info("╚════════════════════════════════════╝")
                logger_info("1. Sepolia Testnet to Holesky Testnet")
                logger_info("2. Sepolia Testnet to Babylon Testnet")
                logger_info("3. Holesky Testnet to Sepolia Testnet")
                logger_info("4. Holesky Testnet to Xion Testnet")
                logger_info("5. Holesky Testnet to Babylon Testnet")
                logger_info("6. Sei Testnet to Xion Testnet")
                logger_info("7. Sei Testnet to Bitcorn Testnet")
                logger_info("8. Sei Testnet to Binance Smart Chain Testnet")
                logger_info("9. Sei Testnet to Babylon Testnet")
                logger_info("10. Bitcorn Testnet to Xion Testnet")
                logger_info("11. Bitcorn Testnet to Sei Testnet")
                logger_info("12. Bitcorn Testnet to Babylon Testnet")
                logger_info("13. Auto All God Mod")
                logger_info("══════════════════════════════════════")
                option = int(input("Choose -> ").strip())
                if option in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
                    option_type = (
                        "Sepolia Testnet to Holesky Testnet" if option == 1 else 
                        "Sepolia Testnet to Babylon Testnet" if option == 2 else 
                        "Holesky Testnet to Sepolia Testnet" if option == 3 else 
                        "Holesky Testnet to Xion Testnet" if option == 4 else 
                        "Holesky Testnet to Babylon Testnet" if option == 5 else 
                        "Sei Testnet to Xion Testnet" if option == 6 else 
                        "Sei Testnet to Bitcorn Testnet" if option == 7 else 
                        "Sei Testnet to Binance Smart Chain Testnet" if option == 8 else 
                        "Sei Testnet to Babylon Testnet" if option == 9 else 
                        "Bitcorn Testnet to Xion Testnet" if option == 10 else
                        "Bitcorn Testnet to Sei Testnet" if option == 11 else
                        "Bitcorn Testnet to Babylon Testnet" if option == 12 else
                        "Run All Pairs"
                    )
                    logger_success(f"{option_type} Selected")
                    break
                else:
                    logger_error("Please enter a number between 1 and 13")
            except ValueError:
                logger_error("Invalid input. Enter a number between 1 and 13")
        self.print_tx_count_question()
        return option

    async def submit_tx_hash(self, tx_hash: str, retries=30):
        data = json.dumps({"query":"query GetPacketHashBySubmissionTxHash($submission_tx_hash: String!) {\n  v2_transfers(args: {p_transaction_hash: $submission_tx_hash}) {\n    packet_hash\n  }\n}","variables":{"submission_tx_hash":f"{tx_hash}"},"operationName":"GetPacketHashBySubmissionTxHash"})
        headers = {
            "Accept": "application/graphql-response+json, application/json",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://app.union.build",
            "Referer": "https://app.union.build/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            try:
                async with ClientSession(timeout=ClientTimeout(total=120)) as session:
                    async with session.post(url=self.GRAPHQL_API, headers=headers, data=data) as response:
                        response.raise_for_status()
                        result = await response.json()
                        packet = result.get("data", {}).get("v2_transfers", [])
                        if packet == []:
                            raise ValueError("Packet Hash Is Empty")
                        return packet
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                logger_error(f"Submit Tx Hash Failed: {str(e)}")
        return None

    async def process_perform_send(self, private_key: str, address: str, tx_amount: float, pair: str):
        tx_hash, block_number = await self.perform_send(private_key, address, tx_amount, pair)
        if tx_hash and block_number:
            if pair in ["Sepolia Testnet to Holesky Testnet", "Sepolia Testnet to Babylon Testnet"]:
                explorer = f"https://sepolia.etherscan.io/tx/{tx_hash}"
            elif pair in ["Holesky Testnet to Sepolia Testnet", "Holesky Testnet to Xion Testnet", "Holesky Testnet to Babylon Testnet"]:
                explorer = f"https://holesky.etherscan.io/tx/{tx_hash}"
            elif pair in ["Sei Testnet to Xion Testnet", "Sei Testnet to Bitcorn Testnet", "Sei Testnet to Binance Smart Chain Testnet", "Sei Testnet to Babylon Testnet"]:
                explorer = f"https://seitrace.com/tx/{tx_hash}?chain=atlantic-2"
            elif pair in ["Bitcorn Testnet to Xion Testnet", "Bitcorn Testnet to Sei Testnet", "Bitcorn Testnet to Babylon Testnet"]:
                explorer = f"https://testnet.cornscan.io/tx/{tx_hash}"
            logger_success("Perform Transfer Success")
            logger_info(f"Block: {block_number}")
            logger_info(f"Explorer: {explorer}")
            logger_loading("Submitting Tx Hash...")
            await asyncio.sleep(5)
            submit = await self.submit_tx_hash(tx_hash)
            if submit:
                packet_hash = submit[0]["packet_hash"]
                union_explorer = f"https://app.union.build/explorer/transfers/{packet_hash}"
                logger_success("Submit Success")
                logger_info(f"Explorer: {union_explorer}")
            else:
                logger_error("Submit Failed")
        else:
            logger_error("Perform On-Chain Failed")

    async def process_option_1(self, private_key: str, address: str):
        logger_step("Option: Sepolia Testnet to Holesky Testnet")
        for i in range(self.tx_count):
            logger_info(f"Transaction {i+1} of {self.tx_count}")
            self.used_rpc = self.SEPOLIA_RPC_URL
            tx_amount = self.sepolia_amount
            pair = "Sepolia Testnet to Holesky Testnet"
            ticker = "ETH Sepolia"
            balance = await self.get_token_balance(address)
            logger_info(f"Balance: {balance} {ticker}")
            logger_info(f"Amount: {tx_amount} {ticker}")
            logger_info(f"Pair: {pair}")
            if not balance or balance <= tx_amount:
                logger_warn(f"Insufficient {ticker} Token Balance")
                return
            await self.process_perform_send(private_key, address, tx_amount, pair)
            await self.print_timer()

    async def process_option_2(self, private_key: str, address: str):
        logger_step("Option: Sepolia Testnet to Babylon Testnet")
        for i in range(self.tx_count):
            logger_info(f"Transaction {i+1} of {self.tx_count}")
            self.used_rpc = self.SEPOLIA_RPC_URL
            tx_amount = self.sepolia_amount
            pair = "Sepolia Testnet to Babylon Testnet"
            ticker = "ETH Sepolia"
            balance = await self.get_token_balance(address)
            logger_info(f"Balance: {balance} {ticker}")
            logger_info(f"Amount: {tx_amount} {ticker}")
            logger_info(f"Pair: {pair}")
            if not balance or balance <= tx_amount:
                logger_warn(f"Insufficient {ticker} Token Balance")
                return
            await self.process_perform_send(private_key, address, tx_amount, pair)
            await self.print_timer()

    async def process_option_3(self, private_key: str, address: str):
        logger_step("Option: Holesky Testnet to Sepolia Testnet")
        for i in range(self.tx_count):
            logger_info(f"Transaction {i+1} of {self.tx_count}")
            self.used_rpc = self.HOLESKY_RPC_URL
            tx_amount = self.holesky_amount
            pair = "Holesky Testnet to Sepolia Testnet"
            ticker = "ETH Holesky"
            balance = await self.get_token_balance(address)
            logger_info(f"Balance: {balance} {ticker}")
            logger_info(f"Amount: {tx_amount} {ticker}")
            logger_info(f"Pair: {pair}")
            if not balance or balance <= tx_amount:
                logger_warn(f"Insufficient {ticker} Token Balance")
                return
            await self.process_perform_send(private_key, address, tx_amount, pair)
            await self.print_timer()

    async def process_option_4(self, private_key: str, address: str):
        logger_step("Option: Holesky Testnet to Xion Testnet")
        for i in range(self.tx_count):
            logger_info(f"Transaction {i+1} of {self.tx_count}")
            self.used_rpc = self.HOLESKY_RPC_URL
            tx_amount = self.holesky_amount
            pair = "Holesky Testnet to Xion Testnet"
            ticker = "ETH Holesky"
            balance = await self.get_token_balance(address)
            logger_info(f"Balance: {balance} {ticker}")
            logger_info(f"Amount: {tx_amount} {ticker}")
            logger_info(f"Pair: {pair}")
            if not balance or balance <= tx_amount:
                logger_warn(f"Insufficient {ticker} Token Balance")
                return
            await self.process_perform_send(private_key, address, tx_amount, pair)
            await self.print_timer()

    async def process_option_5(self, private_key: str, address: str):
        logger_step("Option: Holesky Testnet to Babylon Testnet")
        for i in range(self.tx_count):
            logger_info(f"Transaction {i+1} of {self.tx_count}")
            self.used_rpc = self.HOLESKY_RPC_URL
            tx_amount = self.holesky_amount
            pair = "Holesky Testnet to Babylon Testnet"
            ticker = "ETH Holesky"
            balance = await self.get_token_balance(address)
            logger_info(f"Balance: {balance} {ticker}")
            logger_info(f"Amount: {tx_amount} {ticker}")
            logger_info(f"Pair: {pair}")
            if not balance or balance <= tx_amount:
                logger_warn(f"Insufficient {ticker} Token Balance")
                return
            await self.process_perform_send(private_key, address, tx_amount, pair)
            await self.print_timer()

    async def process_option_6(self, private_key: str, address: str):
        logger_step("Option: Sei Testnet to Xion Testnet")
        for i in range(self.tx_count):
            logger_info(f"Transaction {i+1} of {self.tx_count}")
            self.used_rpc = self.SEI_RPC_URL
            tx_amount = self.sei_amount
            pair = "Sei Testnet to Xion Testnet"
            ticker = "SEI"
            balance = await self.get_token_balance(address)
            logger_info(f"Balance: {balance} {ticker}")
            logger_info(f"Amount: {tx_amount} {ticker}")
            logger_info(f"Pair: {pair}")
            if not balance or balance <= tx_amount:
                logger_warn(f"Insufficient {ticker} Token Balance")
                return
            await self.process_perform_send(private_key, address, tx_amount, pair)
            await self.print_timer()

    async def process_option_7(self, private_key: str, address: str):
        logger_step("Option: Sei Testnet to Bitcorn Testnet")
        for i in range(self.tx_count):
            logger_info(f"Transaction {i+1} of {self.tx_count}")
            self.used_rpc = self.SEI_RPC_URL
            tx_amount = self.sei_amount
            pair = "Sei Testnet to Bitcorn Testnet"
            ticker = "SEI"
            balance = await self.get_token_balance(address)
            logger_info(f"Balance: {balance} {ticker}")
            logger_info(f"Amount: {tx_amount} {ticker}")
            logger_info(f"Pair: {pair}")
            if not balance or balance <= tx_amount:
                logger_warn(f"Insufficient {ticker} Token Balance")
                return
            await self.process_perform_send(private_key, address, tx_amount, pair)
            await self.print_timer()

    async def process_option_8(self, private_key: str, address: str):
        logger_step("Option: Sei Testnet to Binance Smart Chain Testnet")
        for i in range(self.tx_count):
            logger_info(f"Transaction {i+1} of {self.tx_count}")
            self.used_rpc = self.SEI_RPC_URL
            tx_amount = self.sei_amount
            pair = "Sei Testnet to Binance Smart Chain Testnet"
            ticker = "SEI"
            balance = await self.get_token_balance(address)
            logger_info(f"Balance: {balance} {ticker}")
            logger_info(f"Amount: {tx_amount} {ticker}")
            logger_info(f"Pair: {pair}")
            if not balance or balance <= tx_amount:
                logger_warn(f"Insufficient {ticker} Token Balance")
                return
            await self.process_perform_send(private_key, address, tx_amount, pair)
            await self.print_timer()

    async def process_option_9(self, private_key: str, address: str):
        logger_step("Option: Sei Testnet to Babylon Testnet")
        for i in range(self.tx_count):
            logger_info(f"Transaction {i+1} of {self.tx_count}")
            self.used_rpc = self.SEI_RPC_URL
            tx_amount = self.sei_amount
            pair = "Sei Testnet to Babylon Testnet"
            ticker = "SEI"
            balance = await self.get_token_balance(address)
            logger_info(f"Balance: {balance} {ticker}")
            logger_info(f"Amount: {tx_amount} {ticker}")
            logger_info(f"Pair: {pair}")
            if not balance or balance <= tx_amount:
                logger_warn(f"Insufficient {ticker} Token Balance")
                return
            await self.process_perform_send(private_key, address, tx_amount, pair)
            await self.print_timer()

    async def process_option_10(self, private_key: str, address: str):
        logger_step("Option: Bitcorn Testnet to Xion Testnet")
        for i in range(self.tx_count):
            logger_info(f"Transaction {i+1} of {self.tx_count}")
            self.used_rpc = self.CORN_RPC_URL
            tx_amount = self.corn_amount
            pair = "Bitcorn Testnet to Xion Testnet"
            ticker = "BTCN"
            balance = await self.get_token_balance(address)
            logger_info(f"Balance: {balance} {ticker}")
            logger_info(f"Amount: {tx_amount} {ticker}")
            logger_info(f"Pair: {pair}")
            if not balance or balance <= tx_amount:
                logger_warn(f"Insufficient {ticker} Token Balance")
                return
            await self.process_perform_send(private_key, address, tx_amount, pair)
            await self.print_timer()

    async def process_option_11(self, private_key: str, address: str):
        logger_step("Option: Bitcorn Testnet to Sei Testnet")
        for i in range(self.tx_count):
            logger_info(f"Transaction {i+1} of {self.tx_count}")
            self.used_rpc = self.CORN_RPC_URL
            tx_amount = self.corn_amount
            pair = "Bitcorn Testnet to Sei Testnet"
            ticker = "BTCN"
            balance = await self.get_token_balance(address)
            logger_info(f"Balance: {balance} {ticker}")
            logger_info(f"Amount: {tx_amount} {ticker}")
            logger_info(f"Pair: {pair}")
            if not balance or balance <= tx_amount:
                logger_warn(f"Insufficient {ticker} Token Balance")
                return
            await self.process_perform_send(private_key, address, tx_amount, pair)
            await self.print_timer()

    async def process_option_12(self, private_key: str, address: str):
        logger_step("Option: Bitcorn Testnet to Babylon Testnet")
        for i in range(self.tx_count):
            logger_info(f"Transaction {i+1} of {self.tx_count}")
            self.used_rpc = self.CORN_RPC_URL
            tx_amount = self.corn_amount
            pair = "Bitcorn Testnet to Babylon Testnet"
            ticker = "BTCN"
            balance = await self.get_token_balance(address)
            logger_info(f"Balance: {balance} {ticker}")
            logger_info(f"Amount: {tx_amount} {ticker}")
            logger_info(f"Pair: {pair}")
            if not balance or balance <= tx_amount:
                logger_warn(f"Insufficient {ticker} Token Balance")
                return
            await self.process_perform_send(private_key, address, tx_amount, pair)
            await self.print_timer()

    async def process_option_13(self, private_key: str, address: str):
        logger_step("Option: Run All Pairs")
        await self.process_option_1(private_key, address)
        await self.process_option_2(private_key, address)
        await self.process_option_3(private_key, address)
        await self.process_option_4(private_key, address)
        await self.process_option_5(private_key, address)
        await self.process_option_6(private_key, address)
        await self.process_option_7(private_key, address)
        await self.process_option_8(private_key, address)
        await self.process_option_9(private_key, address)
        await self.process_option_10(private_key, address)
        await self.process_option_11(private_key, address)
        await self.process_option_12(private_key, address)

    async def process_accounts(self, private_key: str, address: str, option: int):
        logger_info(f"Address: {address} [EVM]")
        logger_info(f"Address: {self.xion_address[address]} [XION]")
        logger_info(f"Address: {self.babylon_address[address]} [BABYLON]")
        if option == 1:
            await self.process_option_1(private_key, address)
        elif option == 2:
            await self.process_option_2(private_key, address)
        elif option == 3:
            await self.process_option_3(private_key, address)
        elif option == 4:
            await self.process_option_4(private_key, address)
        elif option == 5:
            await self.process_option_5(private_key, address)
        elif option == 6:
            await self.process_option_6(private_key, address)
        elif option == 7:
            await self.process_option_7(private_key, address)
        elif option == 8:
            await self.process_option_8(private_key, address)
        elif option == 9:
            await self.process_option_9(private_key, address)
        elif option == 10:
            await self.process_option_10(private_key, address)
        elif option == 11:
            await self.process_option_11(private_key, address)
        elif option == 12:
            await self.process_option_12(private_key, address)
        elif option == 13:
            await self.process_option_13(private_key, address)
