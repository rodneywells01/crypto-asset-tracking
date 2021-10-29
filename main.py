import requests
import yaml

# Fetch the current price of certain crypto currencies. 
COIN_DETAILS_BY_TICKER = { 
    "sol": {
        "id": "solana",
        "symbol": "sol",
        "name": "Solana"
    },
    "btc": {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin"
    },    
    "eth": {
        "id": "ethereum",
        "symbol": "eth",
        "name": "Ethereum"
    },    
    "dot": {
        "id": "polkadot",
        "symbol": "dot",
        "name": "Polkadot"
    },    
    "xrp": {
        "id": "ripple",
        "symbol": "xrp",
        "name": "XRP"
    }
}


def load_assets(): 
    """
    Loads your assets from an `accounts.yaml` file. 
    This must be present and is not provided in the project. 
    Example accounts.yaml file is provided here: 

    btc:
        BTC_Coinbase: 1
    eth:
        ETH_Metamask: 2
    sol:
        SOL_Coinbase: 10
        SOL_Wallet: 3.4
        SOL_Stake: 5
    dot:
        DOT_Coinbase: 15
    xrp:
        XRP_Coinbase: 1000
    """

    with open("accounts.yaml", "r") as my_assets_file:
        try:
            return yaml.safe_load(my_assets_file)
        except yaml.YAMLError as exc:
            print(exc)


def fetch_current_price(coin_id):
    """
    Get the current price in USD for a given coin id. 
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&tickers=true&market_data=true&community_data=true&developer_data=true&sparkline=true"
    response = requests.request("GET", url)
    return response.json()["market_data"]["current_price"]["usd"]



def fetch_all_prices(): 
    """
    Fetch the prices of all crypto assets that I care about. 
    """
    desired_coin_ids = [COIN_DETAILS_BY_TICKER[coin]["id"] for coin in COIN_DETAILS_BY_TICKER]

    prices = {}
    for ticker in COIN_DETAILS_BY_TICKER: 
        coin_id = COIN_DETAILS_BY_TICKER[ticker]["id"]
        prices[ticker] = fetch_current_price(coin_id)

    return prices

def calculate_total_assets(assets): 
    """
    Sum the total value of all of my accounts. 
    """
    total = 0 
    prices = fetch_all_prices() 
    print(prices) 

    for asset in assets: 
        for account in assets[asset]:
            total += assets[asset][account] * prices[asset]

    return total         
    

if __name__ == "__main__":
    my_assets = load_assets()
    total_assets = calculate_total_assets(my_assets)
    print(f"My crypto is worth: ${total_assets}")
