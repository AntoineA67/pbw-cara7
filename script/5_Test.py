import pandas as pd
import os
from dotenv import load_dotenv
import json
import subprocess
import re

from util.tokens import transfer_nft  # Ajoutez la fonction transfer_nft ici
from util.account import get_account

load_dotenv()
XRP_WALLET_SEED = os.getenv("XRP_WALLET_SEED")
RECIPIENT_ADDRESS = "rwGdtaSMLbc2qpgsSfzTUk72AyVtAS41JQ"  # Ajoutez l'adresse du destinataire

wallet = get_account(XRP_WALLET_SEED)

def transfer():
  
    # Transférer le NFT vers le destinataire
    transfer_results = transfer_nft(XRP_WALLET_SEED, RECIPIENT_ADDRESS, "0009013A9BE83B55DFE0E3AA72EB27547E2CA22F6A724EB8B1B05D1A02C9A47F")
    print(f"Transfer results: {transfer_results}")

transfer()
