import hashlib
import json
import os
import subprocess
import xrpl.wallet.wallet_generation
from script.util.json import read_data_from_car_json
import xrpl

def get_hashes_from(add_smart_contract):
    all_hashes = []
    try:
        command = f"cd evm-interaction && npx truffle exec --network xrpl ./scripts/getHashList.js {add_smart_contract}"
        print(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            raise Exception(stderr.decode())
        else:
            output_lines = stdout.decode().split("\n")
            for line in output_lines:
                if line.startswith('Hash list:'):
                    # Assuming the hash list is comma-separated right after 'Hash list:'
                    hash_list_str = line.split(':', 1)[1].strip()  # Splits once at ':' and strips whitespace
                    all_hashes = hash_list_str.split(',')  # Splits the hash list string into individual hashes
                    break  # No need to continue once we've found and processed the hash list
    except Exception as e:
        print(f"Error during smart contract interaction: {e}")
    return all_hashes


def check_data_integrity_for_one(smart_contract_address, numero_vin):
    all_hashes = get_hashes_from(smart_contract_address)
    
    list_file_in_dir = os.listdir(f"script/db/{numero_vin}")
    list_file_in_dir.remove(f"{numero_vin}.json")
    print(f"List of files in the directory: {list_file_in_dir}")
    print(f"List of hashes in the smart contract: {all_hashes}")
    
    for hash in all_hashes:
        file_name = f"{hash}.json"
        if file_name not in list_file_in_dir:
            print(f"File {file_name} is not in the directory")
            return False
        with open(f"script/db/{numero_vin}/{file_name}", "r") as f:
            content = json.load(f)
        # Convertir le contenu (incluant le timestamp) en chaîne pour le hasher
        content_str_with_timestamp = json.dumps(content, sort_keys=True)  # Utilisation de sort_keys pour la cohérence
        # Créer un hash du contenu incluant le timestamp
        content_hash = hashlib.sha256(content_str_with_timestamp.encode()).hexdigest()
        if content_hash != hash:
            print(f"❌ Incorrect for {numero_vin} | Hash {hash} should be {content_hash}")
            return False
    
    for file in list_file_in_dir:
        file_name = file.split(".")[0]
        if file_name not in all_hashes:
            print(f"Hash {file_name} is not in the smart contract")
            return False
    print(f"✅ Data integrity for {numero_vin} is OK")
    return True

def check_data_integrity_for_all():
    all_data_integrity = {}
    print(os.listdir("script/db"), flush=True)
    for file in os.listdir("script/db"):
        if ".json" not in file:
            numero_vin = file
            with open(f"script/db/{file}/{file}.json", "r") as f:
                print(f"Checking data integrity for {numero_vin}")
                data = json.load(f)
                smart_contract_address = data["SmartContractAddress"]
                all_data_integrity[numero_vin] = check_data_integrity_for_one(smart_contract_address, numero_vin)
                if all_data_integrity[numero_vin]:
                    print(f"Data integrity for {numero_vin} is OK")
                else:
                    print(f"Data integrity for {numero_vin} is NOT OK")
                    return False
    return True
        
# Scoring algorithm for cars either A, B, or C
def scoring():
    cars_data = read_data_from_car_json("data/")

    def score_one_car(car_data):
        battery_health = car_data["batteryHealth"]
        total_kilometers = car_data["totalKilometers"]
        payment_default = car_data["leaseDetails"]["paymentDefault"]
        late_payment_months = car_data["leaseDetails"]["latePaymentMonths"]

        # Scoring criteria
        if (
            battery_health > 90
            and total_kilometers < 30000
            and not payment_default
            and late_payment_months < 2
        ):
            return "A"
        elif (
            80 <= battery_health <= 90
            and total_kilometers < 40000
            and late_payment_months < 4
        ):
            return "B"
        else:
            return "C"

    # Example usage
    car_scores = {
        filename: score_one_car(car_info) for filename, car_info in cars_data.items()
    }
    print(car_scores)

if __name__ == "__main__":
    # Check data integrity
    check_data_integrity_for_all()

# TODO Tranching algorithm

# TODO Create 3 wallets (XRP)

# TODO Move NFTs to wallets according to scoring and tranching

# TODO Get list of investor, generate trustlines for each investor
