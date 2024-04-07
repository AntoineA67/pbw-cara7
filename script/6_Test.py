from web3 import Web3
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement
load_dotenv()

# Initialisation de l'interface Web3 avec l'URL du nœud Ethereum
web3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER_URL')))

# Adresse du contrat intelligent des NFT
contract_address = os.getenv('NFT_CONTRACT_ADDRESS')

# ABI du contrat intelligent des NFT
contract_abi = [
    # Définition des fonctions et événements du contrat intelligent
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_tokenId", "type": "uint256"}
        ],
        "name": "transferFrom",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Création de l'instance du contrat intelligent
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Clés privées des deux comptes
account1_private_key = os.getenv('ACCOUNT1_PRIVATE_KEY')
account2_private_key = os.getenv('ACCOUNT2_PRIVATE_KEY')

# Adresses des deux comptes
account1_address = web3.toChecksumAddress(os.getenv('ACCOUNT1_ADDRESS'))
account2_address = web3.toChecksumAddress(os.getenv('ACCOUNT2_ADDRESS'))

# ID du NFT à transférer
token_id = 1

# Fonction pour transférer un NFT d'un compte à un autre
def transfer_nft(from_address, to_address, token_id, private_key):
    nonce = web3.eth.getTransactionCount(from_address)
    tx = contract.functions.transferFrom(from_address, to_address, token_id).buildTransaction({
        'chainId': 1,  # Identifiant de la chaîne Ethereum (1 pour Ethereum Mainnet)
        'gas': 2000000,  # Limite de gaz
        'gasPrice': web3.toWei('50', 'gwei'),  # Prix du gaz en wei
        'nonce': nonce,
    })
    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return receipt

# Transférer le NFT de account1 à account2
receipt = transfer_nft(account1_address, account2_address, token_id, account1_private_key)

# Vérifier le statut de la transaction
if receipt.status:
    print("Le transfert du NFT a été effectué avec succès.")
else:
    print("Le transfert du NFT a échoué.")
