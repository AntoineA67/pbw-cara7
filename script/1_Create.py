import pandas as pd
import os
from dotenv import load_dotenv
import json

from util.tokens import mint_token
from util.account import get_account

VIN_FILE_PATH = "VIN.csv"

df = pd.read_csv(VIN_FILE_PATH)

vin_numbers = df["VIN"].tolist()
print(f"VIN Numbers: {vin_numbers}")

# Get account info from seed and connect it
load_dotenv()
WALLET_SEED = os.getenv("WALLET_SEED")
print(f"Wallet Seed: {WALLET_SEED}")
wallet = get_account(WALLET_SEED)
print(f"Wallet address: {wallet.classic_address}")

# TODO Get EVM Wallet from seed

# Create smart contract for each VIN number and store them (EVM)
for vin in vin_numbers:
    print(f"Creating smart contract for VIN: {vin}")

    smart_contract_address = "0x1234567890"
    # Create a dictionary with VIN and smart contract address
    data = {"VIN": vin, "SmartContractAddress": smart_contract_address}

    # TODO Create NFT for VIN
    # TODO Store NFT in EVM

    # Create a JSON file named after the VIN number and store the data
    file_name = f"db/{vin}.json"
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)
    # TODO Mint an NFT for each VIN number and store them (XRP)
    results = mint_token(
        WALLET_SEED,
        ent_standby_uri.get(),
        0x0009,  # lsfBurnable + lsfTransferable, see https://xrpl.org/docs/references/protocol/data-types/nftoken/
        ent_standby_transfer_fee.get(),
        ent_standby_taxon.get(),
    )
