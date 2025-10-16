from web3 import Web3

ARB_RPC = "https://arb1.arbitrum.io/rpc"
w3 = Web3(Web3.HTTPProvider(ARB_RPC))
print("Connecté :", w3.is_connected())

