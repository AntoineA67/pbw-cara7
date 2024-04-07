import hashlib
import json
import os
from web3 import Web3
from xrpl.clients import JsonRpcClient
from xrpl.models.transactions import Payment
from xrpl.wallet import generate_faucet_wallet
import subprocess


# Function to hash and rename a JSON file based on its content
def hash_and_rename_json_file(file_path):
    try:
        # Load the JSON content
        with open(file_path, 'r') as file:
            content = json.load(file)
        
        # Extract vehicleId
        din_num = content["vehicleId"]
        
        # Convert content back to string to hash it
        content_str = json.dumps(content)
        
        # Create a hash of the content
        content_hash = hashlib.sha256(content_str.encode()).hexdigest()
        
        # Define the new directory path for 'hashed'
        new_dir_path = os.path.join('hashed')
        # Ensure the directory exists, create if not
        os.makedirs(new_dir_path, exist_ok=True)
        
        # Construct the new file path with the hash as the filename within the new directory
        new_file_path = os.path.join(new_dir_path, f"{content_hash}.json")
        
        # Move (effectively renaming and relocating) the file to the new path
        os.rename(file_path, new_file_path)
        
        return content_hash, din_num
    except Exception as e:
        print(f"Error during hashing and renaming: {e}")
        return None, None

def push_hash_to_smart_contract_and_wallet(content_hash, contract_address):
    try:
        command = f"cd ../evm-interaction && npx truffle exec --network xrpl ./scripts/pushHash.js {contract_address} {content_hash}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if stderr:
            raise Exception(stderr.decode())
        else:
            print(f"Output: {stdout.decode()}")
    except Exception as e:
        print(f"Error during smart contract interaction: {e}")

if __name__ == "__main__":
    file_path = '../data/car2.json'
    content_hash, din_num = hash_and_rename_json_file(file_path)
    if content_hash and din_num:
        print(f"Content hash: {content_hash} for {din_num}")

    with open(f'db/{din_num}/{din_num}.json', 'r') as file:
        details = json.load(file)
    
    smart_contract_address = details["SmartContractAddress"]
    
    push_hash_to_smart_contract_and_wallet(content_hash, smart_contract_address)