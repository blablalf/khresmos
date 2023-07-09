import requests

def get_eth_price():
    url = 'https://www.bitrue.com/api/v1/ticker/price?symbol=prntusdt'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        eth_price = data['price']
        return float(eth_price)
    else:
        print('Erreur lors de la requête API')
        return None

eth_price = get_eth_price()
if eth_price is not None:
    print(f'PRNT/USDT price: {eth_price} USDT')