import asyncio
from union import Union
from ui import display_banner, logger_info, logger_success, logger_error
from utils import generate_address, clear_terminal # Removed load_accounts as it's handled in Union class

async def main():
    try:
        bot = Union()
        display_banner()
        logger_info("Starting Union Auto Swap")
        
        # --- NEW: Select a single wallet ---
        selected_account = bot.select_wallet()
        if not selected_account:
            logger_error("No wallet selected or configured. Exiting.")
            return
        
        private_key = selected_account["PRIVATE_KEY"]
        xion_address = selected_account["XION_ADDRESS"]
        babylon_address = selected_account["BABYLON_ADDRESS"]
        # --- END NEW ---

        option = bot.print_question()
        clear_terminal()
        display_banner()
        
        # Now processing only the selected account
        logger_info(f"Processing Selected Account:")
        separator = "=" * 22
        logger_info(f"{separator}[ 1 Of 1 ]{separator}") # Only one account is processed at a time

        address = generate_address(private_key)
        if not address:
            logger_error("Invalid Private Key or Library Version Not Supported for selected wallet.")
            return
        
        # Pass the specific wallet details to process_accounts
        await bot.process_accounts(private_key, address, xion_address, babylon_address, option)
        
        logger_info("=" * 65)
        logger_success("Selected Account Has Been Processed")
    except Exception as e:
        logger_error(f"Error: {e}")
        raise e

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger_error("EXIT Union Testnet - BOT")

