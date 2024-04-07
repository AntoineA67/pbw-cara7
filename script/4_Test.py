import pandas as pd
import os
from dotenv import load_dotenv
import json
import subprocess
import re

from util.tokens import mint_token
from util.account import get_account

# VIN_FILE_PATH = "VIN.csv"

# df = pd.read_csv(VIN_FILE_PATH)

# vin_numbers = df["VIN"].tolist()
# print(f"VIN Numbers: {vin_numbers}")

# Get account info from seed and connect it
load_dotenv()
XRP_WALLET_SEED = os.getenv("XRP_WALLET_SEED")
print(f"Wallet Seed: {XRP_WALLET_SEED}")
wallet = get_account(XRP_WALLET_SEED)
print(f"Wallet address: {wallet.classic_address}")

def create_nft():
    print(f"Create tokem")

    results = mint_token(
        XRP_WALLET_SEED,
        "test",
        0x0009,
        0x13A,
        0,
    )
    print(f"result {results}")

#create_nft()

