import os
import streamlit as st
import json

# Créer la tab Dashboard
def render_dashboard(nfts):
    st.title("Dashboard NFT pour Voitures")
    st.write(f"{len(nfts)} NFTs trouvés pour votre adresse publique.")
    with st.expander("Voir les détails"):
        st.write("Détails des NFTs...", nfts)

# Créer la tab DEX
def render_dex():
    st.title("Plateforme d'Échange DEX")
    st.write("Fonctionnalités d'échange à implémenter...")

def ensure_user_directory(public_address):
    """Assure que le répertoire utilisateur existe et crée un fichier vide si nécessaire."""
    directory_path = f"script/db/"
    file_path = f"{directory_path}/{public_address}.json"
    
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump({"public_address": public_address, "list_smart_contracts_addresses": []}, file)
    
    return file_path

def load_nft_data(public_address):
    """Charge les données NFT pour un utilisateur donné."""
    file_path = ensure_user_directory(public_address)
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def append_smart_contract_address(public_address, new_smart_contract_address):
    """Ajoute une nouvelle adresse de smart contract à l'utilisateur spécifié."""
    file_path = ensure_user_directory(public_address)
    
    with open(file_path, "r+") as file:
        data = json.load(file)
        if new_smart_contract_address not in data["list_smart_contracts_addresses"]:
            data["list_smart_contracts_addresses"].append(new_smart_contract_address)
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

def create_wallet_collection():
    """Demands the user's public address and handles new wallet creation."""
    # Use a temporary state variable for the new wallet creation process
    if 'create_wallet' not in st.session_state:
        st.session_state.create_wallet = False

    if st.session_state.create_wallet:
        new_wallet_address = st.text_input("Entrez votre nouvelle adresse publique:", key="new_wallet_address")
        if new_wallet_address:
            st.session_state.public_address = new_wallet_address
            ensure_user_directory(new_wallet_address)
            st.success(f"Wallet créé avec succès! Votre nouvelle adresse est: {new_wallet_address}")
            st.session_state.create_wallet = False  # Reset the wallet creation process
    else:
        public_address = st.text_input("Entrez votre adresse publique:", key="public_address")
        if not public_address:
            st.warning("Vous n'avez pas encore de wallet, veuillez en créer un pour continuer.")
            if st.button("Créer un wallet"):
                st.session_state.create_wallet = True
                st.rerun()
        else:
            st.success("Wallet chargé avec succès!")

def main():
    st.sidebar.write(st.session_state)
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choisir la page:", ["Dashboard", "DEX"])
    
    public_address = st.session_state.get("public_address")
    if "nfts" not in st.session_state:
        st.session_state["nfts"] = None
    
    if public_address:
        st.session_state["nfts"] = load_nft_data(public_address)
    else:
        create_wallet_collection()
        public_address = st.session_state.get("public_address")
        st.session_state["nfts"] = load_nft_data(public_address) if public_address else None
    
    if app_mode == "Dashboard" and st.session_state["nfts"]:
        render_dashboard(st.session_state["nfts"])
    elif app_mode == "DEX":
        render_dex()

if __name__ == "__main__":
    main()
