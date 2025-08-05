import os
from dotenv import load_dotenv
from eth_account import Account
from ui import logger_error

# Load environment variables from .env file
load_dotenv()

def load_accounts():
    try:
        private_key = os.getenv("PRIVATE_KEY")
        xion_address = os.getenv("XION_ADDRESS")
        babylon_address = os.getenv("BABYLON_ADDRESS")
        if not private_key or not xion_address or not babylon_address:
            logger_error("Missing PRIVATE_KEY, XION_ADDRESS, or BABYLON_ADDRESS in .env file")
            return []
        return [{"PrivateKey": private_key, "XionAddress": xion_address, "BabylonAddress": babylon_address}]
    except Exception as e:
        logger_error(f"Failed to load .env file: {e}")
        return []

def generate_address(private_key: str):
    try:
        account = Account.from_key(private_key)
        address = account.address
        return address
    except Exception as e:
        logger_error(f"Generate Address Failed: {str(e)}")
        return None

def pad_hex(value, length=64):
    return hex(value)[2:].zfill(length)

def encode_hex_as_string(string, length=32):
    return string.lower()[2:].ljust(length * 2, '0')

def encode_string_as_bytes(string, length):
    hex_str = string.encode('utf-8').hex()
    return hex_str.ljust(length * 2, '0')

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
