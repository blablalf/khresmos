import requests

# EURS = stasis-eurs
# USDC = usd-coin
# PRNT = prime-numbers-ecosystem
token_symbol = "wrapped-xdc"

# Fonction pour récupérer le prix d'une crypto-monnaie depuis CoinGecko
def get_price(crypto_symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_symbol}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    if crypto_symbol in data:
        return data[crypto_symbol]["usd"]
    return None

# Exemple d'utilisation pour récupérer le prix de l'USDC
# stasis-eurs
# wrapped-xdc
wxdc_price = get_price(token_symbol)
if wxdc_price is not None:
    print(token_symbol, f"price : {wxdc_price} USD")
else:
    print("Impossible to get", token_symbol, "price from CoinGecko".format(token_symbol))