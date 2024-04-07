import os
import streamlit as st
import json

import yaml
from config import credentials, admin_names, cookie_name, cookie_key, cookie_expiry_days, pre_authorized
import streamlit_authenticator as stauth
from script.Create import launch_creation
from script.Securisation import check_data_integrity_for_all
from script.Update import update_data 

def handle_session_actions(authenticator: stauth.Authenticate):
    """Handles session actions such as data refresh and logout."""
    try:
        # Keys related to authentication that should not be cleared on data refresh
        exclude_auth_keys = ["authentication_status", "username", "logout", "init", "name", "logoutkey", "failed_login_attempts", "last_query", "results", "theme", "role", "size_window", "public_address"]
        
        # Create columns for the buttons and user status
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button('Refresh'):
                for key in list(st.session_state.keys()):
                    if key not in exclude_auth_keys:
                        del st.session_state[key]
        
        with col3:
            authenticator.logout(key="logoutkey")
            
        # Column 2: Logout button
        with col4:
            st.write("🔒", st.session_state.get("role"))
        # Column 3: Display user status
        with col5:
            st.write(st.session_state.get("username", "Guest"), "🟢")
    except Exception as e:
        st.error(f"An error occurred in handle_session_actions(): {e}")

def load_wallet_address_from_yaml():
    with open(os.path.join("confs", "secrets.yaml"), 'r') as file:
        keys_secrets = yaml.load(file, Loader=yaml.SafeLoader)
    wallets_addresses = keys_secrets["wallet_address"]
    current_username = st.session_state.get('username')
    if current_username in wallets_addresses:
        # Directly retrieve the wallet address for the username
        wallet_address = wallets_addresses[current_username]
        st.session_state["public_address"] = wallet_address
        return wallet_address
    return None

# Fonction pour afficher le dashboard NFT
def display_wallet(nfts):
    add = load_wallet_address_from_yaml()
    with st.expander("Public Address"):
        st.write(add)
    st.title("CARS NFT Dashboard")
    with st.expander("See Car NFTs"):
        st.write("Détails des NFTs...", nfts)
    if st.button("Check the integrity of your NFTs"):
        st.write("Checking the integrity of your NFTs...")
        if check_data_integrity_for_all() == True:
            st.success("All NFTs are OK. The raw data integrity is preserved.")
        else:
            st.error("Some NFTs are NOT OK. The raw data integrity is compromised.")

def display_new_data():
    st.title("Update with new data")
    data_folder = "data"  # Chemin vers le dossier contenant les données JSON

    # Vérifier si le dossier existe
    if not os.path.exists(data_folder):
        st.write("Le dossier de données n'existe pas.")
        return

    # Lister tous les fichiers JSON dans le dossier
    json_files = [f for f in os.listdir(data_folder) if f.endswith('.json')]

    if not json_files:
        st.write("Aucune donnée trouvée.")
        return

    with st.expander("Data"):
        # Parcourir chaque fichier JSON
        for json_file in json_files:
            file_path = os.path.join(data_folder, json_file)
            
            # Charger le contenu JSON
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Afficher le nom du fichier et le contenu de manière organisée
            st.write(f"**{json_file}**")  # Nom du fichier en gras
            st.json(data)  # Afficher le contenu JSON de manière interactive

            # Optionnel: insérer une séparation entre les fichiers
            st.markdown("---")
    if st.button("Update data"):
        if update_data() == True:
            st.success("Data updated successfully")
        else:
            st.error("Error updating data, please check the logs")

# Fonction pour afficher la plateforme d'échange DEX
def render_dex():
    st.title("Plateforme d'Échange DEX")
    st.write("Fonctionnalités d'échange à implémenter...")

# Fonction pour s'assurer que le répertoire de l'utilisateur existe
def ensure_user_directory(public_address):
    directory_path = "script/db"
    file_path = os.path.join(directory_path, f"{public_address}.json")
    
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    if not os.path.isfile(file_path):
        with open(file_path, "w") as file:
            json.dump({"public_address": public_address, "list_NFTokenId": []}, file)
    
    return file_path

def create_new_nft_data():
    st.title("Add New Cars")
    st.write("You have the possibility to add new cars to your wallet.")
    if st.button("Add new car"):
        if launch_creation() == True:
            st.success("New cars added successfully")
        else:
            st.error("Error adding new cars, please check the logs")

# Fonction pour charger les données NFT de l'utilisateur
def load_nft_data():
    file_path = ensure_user_directory(st.session_state["public_address"])
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def display_securitization_platform_with_risk():
    st.title("Vehicle Securitization Platform")

    # Simulated data for demonstration
    vehicles = [
        {"model": "Tesla Model S", "year": "2022", "lease_price": "$1,200/month", "risk_level": "Low", "description": "Electric performance car with high autonomy."},
        {"model": "BMW i8", "year": "2020", "lease_price": "$1,500/month", "risk_level": "Medium", "description": "Sporty hybrid with futuristic design."},
        {"model": "Audi e-tron GT", "year": "2021", "lease_price": "$1,100/month", "risk_level": "Low", "description": "Comfort and performance in an elegant electric vehicle."},
        {"model": "Mercedes EQC", "year": "2021", "lease_price": "$950/month", "risk_level": "Medium", "description": "Electric SUV combining luxury and technology."},
        {"model": "Porsche Taycan", "year": "2022", "lease_price": "$1,300/month", "risk_level": "High", "description": "Performance and innovation in a sporty electric vehicle."},
    ]

    # User selects the risk level they are interested in
    risk_selection = st.selectbox("Select risk level:", ["All", "Low", "Medium", "High"])

    filtered_vehicles = vehicles if risk_selection == "All" else [vehicle for vehicle in vehicles if vehicle["risk_level"] == risk_selection]

    # Display each vehicle in its own box based on risk level filter
    for vehicle in filtered_vehicles:
        with st.container():
            cols = st.columns([2, 5, 2, 2, 6])  # Space distribution between columns
            cols[0].image("https://via.placeholder.com/150", use_column_width=True)  # Placeholder for the image
            cols[1].markdown(f"**Model:** {vehicle['model']}")
            cols[2].markdown(f"**Year:** {vehicle['year']}")
            cols[3].markdown(f"**Lease Price:** {vehicle['lease_price']}")
            cols[4].markdown(f"**Risk Level:** {vehicle['risk_level']}\n\n**Description:** {vehicle['description']}")

            # Add a line separator for clarity
            st.markdown("---")

    # Footer with a call to action
    st.info("Interested in investing in our vehicle-backed securities? Contact us for more information.")
    
# La fonction principale orchestrant l'application
def main():
    st.sidebar.title("Navigation")
    tabs = st.tabs(["Wallet", "DEX", "Update Data", "Add New Cars"])
    
    with tabs[0]:
        nfts = load_nft_data()
        display_wallet(nfts)
    with tabs[1]:
        display_securitization_platform_with_risk()
    with tabs[2]:
        display_new_data()
    with tabs[3]:
        create_new_nft_data()

def auth():
    # """Authenticates the user and runs the main function."""
    # try: 
        # Initialize the authenticator
        authenticator = stauth.Authenticate(
            credentials=credentials,
            cookie_name=cookie_name,
            cookie_key=cookie_key,
            cookie_expiry_days=cookie_expiry_days
        )

        # Perform login
        authenticator.login()
        
        if "public_address" not in st.session_state or st.session_state["public_address"] is None:
            st.session_state["public_address"] = load_wallet_address_from_yaml()
        cols = st.columns([1, 8, 1])
        # Authentication status handling
        if st.session_state.get("authentication_status"):
            if admin_names and st.session_state.get("username") in admin_names:
                st.session_state["role"] = "admin"
            else:
                st.session_state["role"] = "user"
            with cols[1]:
                handle_session_actions(authenticator)
                main()
        elif st.session_state.get("authentication_status") is False:
            st.error('Username/password is incorrect')
        elif st.session_state.get("authentication_status") is None:
            st.warning('Please enter your username and password')
    # except Exception as e:
    #     st.error(f"An error occurred in auth(): {e}")

if __name__ == "__main__":
    st.set_page_config(page_title="NFT Dashboard", page_icon="🚗", initial_sidebar_state="collapsed", layout="wide")
    # Initialize session state variables
    if "public_address" not in st.session_state:
        st.session_state["public_address"] = None  # Or any other default value you prefer
    auth()
