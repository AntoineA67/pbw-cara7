import os
import sys
import yaml
from yaml.loader import SafeLoader

# Load secrets from YAML file
with open(os.path.join("confs", "secrets.yaml"), 'r') as file:
    keys_secrets = yaml.load(file, Loader=SafeLoader)

# Extract credentials and cookie settings correctly
# Extracting configurations correctly
credentials = keys_secrets["credentials"]  # Stores the whole 'credentials' dictionary
cookie_name = keys_secrets["cookie"]["name"]
cookie_key = keys_secrets["cookie"]["key"]
cookie_expiry_days = keys_secrets["cookie"]["expiry_days"]
admin_names = keys_secrets['role']['admin']  # Assuming 'role' exists and contains an 'admin' key
pre_authorized = keys_secrets['pre-authorized']['emails']  # Adjusted to match the structure