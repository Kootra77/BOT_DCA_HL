import json

import utils
from hyperliquid.utils import constants
from hyperliquid.info import Info



def main():
    address, info, exchange = utils.setup(base_url=constants.MAINNET_API_URL, skip_ws=True)

    montant_usd = float(input("Quel montant voulez vous acheter ? (min 15$) "))

    info = Info(skip_ws=True)  # instancie sans websocket

    # Récupère tous les prix en USD
    mids = info.all_mids()  # dict: coin_name -> float
    # Accès direct au prix
    btc_price = mids.get("BTC")
    print(f"Token: BTC, Spot Price: {btc_price}")
    price_usd_btc = round(montant_usd/ float(btc_price), 5)


    # Get the user state and print out position information
    spot_user_state = info.spot_user_state(address)
    if len(spot_user_state["balances"]) > 0:
        print("spot balances:")
        for balance in spot_user_state["balances"]:
            print(json.dumps(balance, indent=2))
    else:
        print("no available token balances")
       
    order_result = exchange.market_open("UBTC/USDC", True, price_usd_btc)
    print(order_result)
    

if __name__ == "__main__":
    main()
