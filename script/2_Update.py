from datetime import datetime
import glob
import hashlib
import json
import os
import subprocess

def hash_and_rename_json_file(file_path):
    try:
        # Charger le contenu JSON
        with open(file_path, 'r') as file:
            content = json.load(file)
        
        # Extraire le vehicleId
        din_num = content["vehicleId"]
        
        # Ajouter un timestamp au contenu JSON
        timestamp = datetime.utcnow().isoformat()
        content["timestamp"] = timestamp  # Ajouter le timestamp au contenu
        
        # Convertir le contenu (incluant le timestamp) en chaîne pour le hasher
        content_str_with_timestamp = json.dumps(content, sort_keys=True)  # Utilisation de sort_keys pour la cohérence
        
        # Créer un hash du contenu incluant le timestamp
        content_hash = hashlib.sha256(content_str_with_timestamp.encode()).hexdigest()
        
        # Définir le nouveau chemin du dossier pour 'hashed'
        new_dir_path = os.path.join(f'db/{din_num}')
        # S'assurer que le dossier existe, le créer sinon
        os.makedirs(new_dir_path, exist_ok=True)
        
        # Construire le nouveau chemin du fichier avec le hash comme nom du fichier dans le nouveau dossier
        new_file_path = os.path.join(new_dir_path, f"{content_hash}.json")
        
        # Écrire le contenu mis à jour (incluant le timestamp) dans le nouveau fichier
        with open(new_file_path, 'w') as new_file:
            json.dump(content, new_file, indent=4)  # Conserver le formatage pour la lisibilité
        
        return content_hash, din_num
    except Exception as e:
        print(f"Erreur pendant le hashage et la sauvegarde : {e}")
        return None, None

def push_hash_to_smart_contract_and_wallet(content_hash, contract_address):
    try:
        command = f"cd ../evm-interaction && npx truffle exec --network xrpl ./scripts/pushHash.js {contract_address} {content_hash}"
        print(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if stderr:
            raise Exception(stderr.decode())
        else:
            print(f"Output: {stdout.decode()}")
    except Exception as e:
        print(f"Error during smart contract interaction: {e}")

if __name__ == "__main__":
    # Traitement de tous les fichiers JSON dans le dossier '../data/'
    for file_path in glob.glob('../data/*.json'):
        content_hash, din_num = hash_and_rename_json_file(file_path)
        if content_hash and din_num:            
            try:
                with open(f'db/{din_num}/{din_num}.json', 'r') as file:
                    details = json.load(file)
                
                smart_contract_address = details["SmartContractAddress"]
                push_hash_to_smart_contract_and_wallet(content_hash, smart_contract_address)
            except Exception as e:
                print(f"Erreur lors de la lecture des détails ou de l'interaction avec le smart contract : {e}")