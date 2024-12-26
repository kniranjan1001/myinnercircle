import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from datetime import datetime
from typing import Dict

# Logging configuration
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# wallet address
WALLET_NAMES = {
    "GghbeTXXvAjrsRqTe5maywtBT1XPRnR45R8VxAK2YtcG": "Bob",
    "EbNr5s54pCUFzEyBDjJWwqYQc7R5E8udmPEpDLwpbjKq": "Alice",
    "8gx4VKzNVjenF2t7wikTHjwWEUt6mjJT4xmaSZKuCzCG": "Ram",
    "A6EcV1ZhbGwNp6FYEXw4TaTyfVd8ASNGC1xiXL2Dz5zF": "Shyam",
    "AgfjAqBTKMGHAr1ZxjK8NWyMMp2EyyoS3wkYPYTUBjT5": "Lakshman",
    "EP6RiDr27fNDtTkFbofZhtVojyMS9DC9b41VyfvtEQV7": "Arjun",
    "6ocX9nqdTLjm99HXXFVfucshcvWVo7h8BFQDwk9R12xu": "Krishna",
    "6ESwF2ouiH7Vz2uRkzBXftY6Ko9jdqvebMvTFUG2Bthy": "Radha",
    "Engi2TDft8C6R33RMn9YpBeNqxzqpyzKiXQBAsQZPZpw": "Sita",
    "3e4VMNkFwT8t6vVVGLHYWYhhUGQtcACR1F1NrWMwY8eF": "Hanuman",
    "BtxnBqqgCnDQfXLJeijdJm2GdNz3iFEqKAkMw3SuJtNG": "Sugriv",
    "CYEtWTAX4W25MiSQZBwKeH1NLEnEUnzRAbNbNzkdnzVt": "Vibhishan",
    "JD25qVdtd65FoiXNmR89JjmoJdYk9sjYQeSTZAALFiMy": "JohnDoe",
    "5XboKCwuw8diGX1jHZnpx2hn319TwbmmxGtQVbHBCv56": "MeganSmith",
    "GvD5HiZuNcZvny8zhUXStLwEiWmA2spbikj22wEN5LYR": "AlexBrown",
    "Egm9KLWURmXjDEitMVucUnHCVex5NeZ5M3gT4CCb2Q1V": "CharlieDavis",
    "BQ39hZo1eZsnaxGSUdk7MFnJoVsJd1ifCNEUqzY2aSjs": "OliviaTaylor"
}


# Define categories and wallet IDs
CATEGORIES = {
    "High invest": ["GghbeTXXvAjrsRqTe5maywtBT1XPRnR45R8VxAK2YtcG", "EbNr5s54pCUFzEyBDjJWwqYQc7R5E8udmPEpDLwpbjKq","JD25qVdtd65FoiXNmR89JjmoJdYk9sjYQeSTZAALFiMy","5XboKCwuw8diGX1jHZnpx2hn319TwbmmxGtQVbHBCv56"],
    "Best 4 Me": [
        "8gx4VKzNVjenF2t7wikTHjwWEUt6mjJT4xmaSZKuCzCG", "A6EcV1ZhbGwNp6FYEXw4TaTyfVd8ASNGC1xiXL2Dz5zF",
        "AgfjAqBTKMGHAr1ZxjK8NWyMMp2EyyoS3wkYPYTUBjT5", "EP6RiDr27fNDtTkFbofZhtVojyMS9DC9b41VyfvtEQV7",
        "6ocX9nqdTLjm99HXXFVfucshcvWVo7h8BFQDwk9R12xu", "6ESwF2ouiH7Vz2uRkzBXftY6Ko9jdqvebMvTFUG2Bthy",
        "GvD5HiZuNcZvny8zhUXStLwEiWmA2spbikj22wEN5LYR","Egm9KLWURmXjDEitMVucUnHCVex5NeZ5M3gT4CCb2Q1V"
    ],
    "Lowprofit": ["Engi2TDft8C6R33RMn9YpBeNqxzqpyzKiXQBAsQZPZpw", "A6EcV1ZhbGwNp6FYEXw4TaTyfVd8ASNGC1xiXL2Dz5zF"],
    "desprate": ["3e4VMNkFwT8t6vVVGLHYWYhhUGQtcACR1F1NrWMwY8eF", "BtxnBqqgCnDQfXLJeijdJm2GdNz3iFEqKAkMw3SuJtNG","BQ39hZo1eZsnaxGSUdk7MFnJoVsJd1ifCNEUqzY2aSjs"],
    "Risk Checker": ["CYEtWTAX4W25MiSQZBwKeH1NLEnEUnzRAbNbNzkdnzVt"]
}

# Track last transaction hashes to avoid duplicates
last_transaction_hashes = set()

# API URL Template
# API_URL_TEMPLATE = "https://gmgn.ai/api/v1/wallet_activity/sol?type=buy&type=sell&wallet={wallet_id}&limit=10&cost=10"
API_URL_TEMPLATE = "https://gmgn.ai/api/v1/wallet_activity/sol?type=buy&type=sell&wallet={wallet_id}&limit=10&cost=10"
# Headers observed from the browser
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cookie": "_ga=GA1.1.210426056.1735150179; cf_chl_rc_i=1; __cf_bm=zZN28MYKdIhUvHroVMvoYHGoEkd8m0UTlkeeCTYJWXw-1735184017-1.0.1.1-mEDYyYFuEkKWK1ItziH58jyyoEBhiiZ49c_4btLMVr253eHx2v1xNCSdrOS4JubcddqqRKgEORNez2WlPC4kDg; _ga_0XM0LYXGC8=GS1.1.1735182821.3.1.1735184422.0.0.0; cf_clearance=qlynh4pAXK2LAa4rPY95lT_SAudPGefRy8MyTXj9vWg-1735184420-1.2.1.1-e0XI.63JlYMyuGFdZqSal7moqx0JVP6VIX70dW6I_oQquxYNKsrV7.2dA93bgU1Vqkh6tMXbnUjkt9QhFqTn2b.6Iu__ZVwJsu826tzg6clhOGvEpiUk2zURGoNqit91BXfO9cUEIrbVKoRJeVrNGzkqXt5zBntp6K.X6igl4AmCp6RNXhvdRv7lV_Mi5GyAQ4Am9MygcieRWyRXgtuqwlkQMA9RmTMGN.sHzfogY6RlKWRxKW1sG2ItmeMvM468saD3WyLhnfRQaueqv2fPk.bJITFbkgpbrLi_kAzVP9UqreWBlRdYX_za.LKSO3RLJpf2VzQZI24bLUD6PRTqIk0R5ULux5ZsgvTO7.oa1oFNYcD6ZSl0CSTx.tlhryh3vk2trdvPLVveN1Ub3R7hgFb6ovdsodSIoEIY5sOM9IRZGmLiwgEhrPzNf0mZSkoGlv4ROvgCo9yTJv4RyxzrQg",
    "priority": "u=0, i",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-arch": '""',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": '"131.0.6778.205"',
    "sec-ch-ua-full-version-list": '"Google Chrome";v="131.0.6778.205", "Chromium";v="131.0.6778.205", "Not_A Brand";v="24.0.0.0"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-model": '"Nexus 5"',
    "sec-ch-ua-platform": '"Android"',
    "sec-ch-ua-platform-version": '"6.0"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
}

# Convert timestamp to readable time
def convert_timestamp(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

# Fetch transactions for a wallet
def fetch_wallet_activity(wallet_id: str) -> list:
    url = API_URL_TEMPLATE.format(wallet_id=wallet_id)
    # url = API_URL_TEMPLATE
    try:
        response = requests.get(url,headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if data["code"] == 0 and "activities" in data["data"]:
            return data["data"]["activities"]
    except Exception as e:
        logger.error(f"Error fetching data for wallet {wallet_id}: {e}")
    return []

# Monitor wallets and send updates
async def monitor_wallets(context: CallbackContext) -> None:
    bot = context.bot
    chat_id = context.job.data  # Retrieve chat_id from job data
    for category, wallets in CATEGORIES.items():
        for wallet in wallets:
            transactions = fetch_wallet_activity(wallet)
            wallet_name = WALLET_NAMES.get(wallet, wallet[-4:])
            for tx in transactions:
                tx_hash = tx["tx_hash"]
                if tx_hash in last_transaction_hashes:
                    continue  # Skip if already processed
                last_transaction_hashes.add(tx_hash)

                # Format and send the message
                timestamp = convert_timestamp(tx["timestamp"])
                event_type = tx["event_type"]
                token_symbol = tx["token"]["symbol"]
                token_amount = tx["token_amount"]
                quote_amount = tx["quote_amount"]

                message = (
                    f"📣 *{category}*\n"
                    f"🫣 {wallet_name}\n"
                    f"🕒 {timestamp}\n"
                    f"🔹 Event Type: {event_type}\n"
                    f"🔹 Token: {token_symbol}\n"
                    f"🔹 Token Amount: {token_amount}\n"
                    f"🔹 Quote Amount: {quote_amount}"
                )
                await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

# Start monitoring command
async def start_monitoring(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    if context.job_queue:
        context.job_queue.run_repeating(monitor_wallets, interval=60, first=0, data=chat_id)
        await update.message.reply_text("✅ Monitoring started! You will receive live updates on wallet activity.")
    else:
        await update.message.reply_text("❌ Failed to start monitoring. Job queue is not initialized.")

# Handle /start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🤖 Welcome! Use /monitor to start receiving updates.")

def main():
    # Create the Application with a JobQueue enabled
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("monitor", start_monitoring))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
