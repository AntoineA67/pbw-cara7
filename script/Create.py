import pandas as pd
import os
from dotenv import load_dotenv
import json
import subprocess
import re

from script.util.tokens import mint_token
from script.util.account import get_account
from script.util.json import read_data_from_car_json

# Get account info from seed and connect it
load_dotenv()
XRP_WALLET_SEED = os.getenv("XRP_WALLET_SEED")
MY_WALLET_PUB_ADDR = os.getenv("MY_WALLET_PUB_ADDR")
# print(f"Wallet Seed: {XRP_WALLET_SEED}")

def store_smart_contract_in_evm():
    # Define the command to be executed
    command = "cd evm-interaction && npx truffle migrate --network xrpl"

    # Execute the command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the command to complete
    stdout, stderr = process.communicate()

    # Check if the command was executed successfully
    if process.returncode == 0:
        print("Command executed successfully")
        # print(stdout.decode())  # Print the standard output
    else:
        print("Error executing command")
        print(stderr.decode())  # Print the standard error
    # Use regular expression to find the contract address
    match = re.search(r'> contract address:\s+(0x[a-fA-F0-9]+)', stdout.decode())

    # Extract and print the contract address if found
    if match:
        contract_address = match.group(1)
        print("Contract Address:", contract_address)
    else:
        print("Contract address not found.")
    return contract_address

def launch_creation():
    try:
        wallet = get_account(XRP_WALLET_SEED)
        print(f"Wallet address: {wallet.classic_address}")
        vin_numbers = [ v['vehicleId'] for v in read_data_from_car_json("data/").values() ]
        print(f"VIN Numbers: {vin_numbers}")
        wallet_file_path = f"script/db/rsSkGhsGbpcMXNkwuSECQ5k5NZiJfJ7LrH.json"
        
        # Load existing data or initialize if file doesn't exist
        if os.path.exists(wallet_file_path):
            with open(wallet_file_path, "r") as file:
                wallet_data = json.load(file)
        else:
            wallet_data = {"public_address": MY_WALLET_PUB_ADDR, "list_NFTokenId": []}

        # Iterate over VIN numbers to create smart contracts and mint tokens
        for vin in vin_numbers:
            print(f"Creating smart contract for VIN: {vin}")
            smart_contract_address = store_smart_contract_in_evm()

            results = mint_token(XRP_WALLET_SEED, smart_contract_address, 0x0009, 0x13A, 0)

            # Append the new NFTokenId to the list
            wallet_data["list_NFTokenId"].append(results["meta"]["nftoken_id"])

            # Store data specific to VIN in its own file
            vin_data = {"VIN": vin, "SmartContractAddress": smart_contract_address, "NFTokenId": results["meta"]["nftoken_id"]}
            vin_file_path = f"script/db/{vin}/{vin}.json"
            os.makedirs(os.path.dirname(vin_file_path), exist_ok=True)
            with open(vin_file_path, "w") as vin_file:
                json.dump(vin_data, vin_file, indent=4)

        # Save updated wallet data back to file
        with open(wallet_file_path, "w") as wallet_file:
            json.dump(wallet_data, wallet_file, indent=4)
    except Exception as e:
        print(f"Error during token minting: {e}")
        return False
    return True
            
