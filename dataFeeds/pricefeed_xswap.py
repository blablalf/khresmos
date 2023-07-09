from web3 import Web3
from web3.middleware import geth_poa_middleware
import json


# Adresse du nœud RPC Ethereum
rpc_url = "https://erpc.xinfin.network"

# Adresse du contrat du Router XSWAP
router_contract_address = "0xf9c5E4f6E627201aB2d6FB6391239738Cf4bDcf9"

#XUSDT
# 0xD4B5f10D61916Bd6E0860144a91Ac658dE8a1437
#WXDC
#0x951857744785E80e2De051c32EE7b25f9c458C42


# Chargement de l'ABI du contrat Router XSWAP 
with open("xswap_router_abi.json", "r") as abi_file:
    router_abi = json.load(abi_file)

# Nombre de blocs à examiner
block_range = 10

# Connexion au nœud RPC XTC
web3 = Web3(Web3.HTTPProvider(rpc_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Chargement du contrat Router XSWAP
router_contract = web3.eth.contract(address=router_contract_address, abi=router_abi)

# Récupération du numéro du dernier bloc
latest_block_number = web3.eth.block_number

# Récupération du prix de la pool XSWAP pour chaque bloc
for block_number in range(latest_block_number - block_range + 1, latest_block_number + 1):
    # Récupération du hachage du bloc
    block_hash = web3.eth.get_block(block_number)["hash"]
    
    # Appel de la fonction getAmountsOut du Router XSWAP pour obtenir le prix de la paire de tokens
    amounts_out = router_contract.functions.getAmountsOut(1, ["0xD4B5f10D61916Bd6E0860144a91Ac658dE8a1437", "0x951857744785E80e2De051c32EE7b25f9c458C42"]).call(block_identifier=block_number)
    price = (amounts_out[1] / amounts_out[0]) / 10**15 # Prix de la paire (USDC/WETH)
    
    print(f"Block {block_number}: WXDC Price = {price} ")