import os
from dotenv import load_dotenv
from eth_account import Account
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info

load_dotenv()  # charge les variables depuis .env

def get_secret_key(_config=None):
    """
    Récupère la clé privée depuis la variable d'environnement HYPERLIQUID_SECRET_KEY.
    La clé doit être en hexadécimal.
    """
    secret_key_hex = os.getenv("HYPERLIQUID_SECRET_KEY")
    if not secret_key_hex:
        raise Exception("La variable HYPERLIQUID_SECRET_KEY n'est pas définie dans .env")
    return bytes.fromhex(secret_key_hex)


def setup(base_url=None, skip_ws=False, perp_dexs=None):
    """
    Initialise le compte, Info et Exchange depuis les variables d'environnement.
    Logique identique à l'ancienne fonction.
    """
    account = Account.from_key(get_secret_key())
    
    # Adresse du compte (optionnelle dans .env, sinon prend l'adresse dérivée de la clé)
    address = os.getenv("HYPERLIQUID_ACCOUNT_ADDRESS", account.address)
    print("Running with account address:", address)
    if address != account.address:
        print("Running with agent address:", account.address)

    info = Info(base_url, skip_ws, perp_dexs=perp_dexs)
    user_state = info.user_state(address)
    spot_user_state = info.spot_user_state(address)
    margin_summary = user_state["marginSummary"]

    if float(margin_summary["accountValue"]) == 0 and len(spot_user_state["balances"]) == 0:
        print("Not running the example because the provided account has no equity.")
        url = info.base_url.split(".", 1)[1]
        error_string = (
            f"No accountValue:\n"
            f"If you think this is a mistake, make sure that {address} has a balance on {url}.\n"
            f"If address shown is your API wallet address, set HYPERLIQUID_ACCOUNT_ADDRESS in .env to your main account address."
        )
        raise Exception(error_string)

    exchange = Exchange(account, base_url, account_address=address, perp_dexs=perp_dexs)
    return address, info, exchange
