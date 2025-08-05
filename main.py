import asyncio
from union import Union
from ui import display_banner, logger_info, logger_success, logger_error
from utils import load_accounts, generate_address, clear_terminal

async def main():
    try:
        bot = Union()
        display_banner()
        logger_info("Starting Union Auto Swap")
        accounts = load_accounts()
        if not accounts:
            logger_error("No Accounts Loaded")
            return
        option = bot.print_question()
        clear_terminal()
        display_banner()
        logger_info(f"Account's Total: {len(accounts)}")
        separator = "=" * 22
        for idx, account in enumerate(accounts, start=1):
            if account:
                private_key = account["PrivateKey"]
                xion_address = account["XionAddress"]
                babylon_address = account["BabylonAddress"]
                logger_info(f"{separator}[ {idx} Of {len(accounts)} ]{separator}")
                if not private_key or not xion_address or not babylon_address:
                    logger_error("Invalid Account Data")
                    continue
                address = generate_address(private_key)
                if not address:
                    logger_error("Invalid Private Key or Library Version Not Supported")
                    continue
                bot.xion_address[address] = xion_address
                bot.babylon_address[address] = babylon_address
                await bot.process_accounts(private_key, address, option)
        logger_info("=" * 65)
        logger_success("All Accounts Have Been Processed")
    except Exception as e:
        logger_error(f"Error: {e}")
        raise e

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger_error("EXIT Union Testnet - BOT")
