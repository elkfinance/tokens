import os
import shutil
import re

# Prompt user for input
chain_name = input("Enter Chain Name (CHAINNAME): ")
native_token_address = input("Enter Native Token Symbol Address (NATIVETOKENSYMBOLADDRESS): ")
chain_id = int(input("Enter Chain ID Number (ChainID): "))
address = input("Enter Wrapped ETH address: ")
decimals = int(input("Enter Wrapped ETH decimals: "))
name = input("Enter Wrapped ETH Name: ")
symbol = input("Enter Wrapped ETH symbol: ")

# Create the folder at /logos/CHAINNAME
logos_folder = os.path.join(os.path.dirname(__file__), "logos", chain_name)
os.makedirs(logos_folder, exist_ok=True)
print(f"Created folder: {logos_folder}")

# Create the folder at /logos/CHAINNAME/address if it doesn't exist
address_folder = os.path.join(logos_folder, address)
if not os.path.exists(address_folder):
    os.makedirs(address_folder)
    print(f"Created folder: {address_folder}")
else:
    print(f"Folder already exists: {address_folder}")

# Create the folder at /logos/CHAINNAME/NATIVETOKENLOGOADDRESS if it doesn't exist
native_token_folder = os.path.join(logos_folder, native_token_address)
if not os.path.exists(native_token_folder):
    os.makedirs(native_token_folder)
    print(f"Created folder: {native_token_folder}")
else:
    print(f"Folder already exists: {native_token_folder}")

# Load template file
template_file_path = os.path.join(os.path.dirname(__file__), 'template.tokenlist.json')
try:
    with open(template_file_path, 'r') as f:
        template = f.read()
except FileNotFoundError:
    print(f"Error: Template file not found at {template_file_path}")
    exit(1)

# Replace placeholders in template
output = template.replace('CHAINNAME', chain_name)
output = output.replace('NATIVETOKENLOGOADDRESS', native_token_address)
output = output.replace('WRAPPEDTOKENLOGOADDRESS', address)
output = re.sub(r'"chainId": ,', f'"chainId": {chain_id},', output)
output = re.sub(r'"address": "",', f'"address": "{address}",', output)
output = re.sub(r'"decimals": ,', f'"decimals": {decimals},', output)
output = re.sub(r'"name": "",', f'"name": "{name}",', output)
output = re.sub(r'"symbol": ""', f'"symbol": "{symbol}"', output)

# Write output to new file
new_file_path = os.path.join(os.path.dirname(__file__), f'{chain_name.lower()}.tokenlist.json')
try:
    with open(new_file_path, 'w') as f:
        f.write(output)
    print(f"Created file: {new_file_path}")
except IOError as e:
    print(f"Error creating file: {new_file_path}")
    print(f"Error: {e}")

# Update generate_ts_config.py
generate_ts_config_path = os.path.join(os.path.dirname(__file__), 'generate_ts_config.py')
try:
    with open(generate_ts_config_path, 'r') as f:
        config = f.read()
except FileNotFoundError:
    print(f"Error: generate_ts_config.py not found at {generate_ts_config_path}")
    exit(1)

if f"'{chain_name.upper()}': {chain_id}" not in config:
    config = re.sub(r"(CHAIN_IDS = {[^}]+)", f"\\1\n\t'{chain_name.upper()}': {chain_id},", config)
    print(f"Added '{chain_name.upper()}': {chain_id} to CHAIN_IDS")
else:
    print(f"'{chain_name.upper()}': {chain_id} already exists in CHAIN_IDS")

if f"'{chain_name.upper()}': '{address}'" not in config:
    config = re.sub(r"(WETH = {[^}]+)", f"\\1\n\t'{chain_name.upper()}': '{address}',", config)
    print(f"Added '{chain_name.upper()}': '{address}' to WETH")
else:
    print(f"'{chain_name.upper()}': '{address}' already exists in WETH")

if re.search(rf"IGNORE = \[.*'{symbol}'.*\]", config) is None:
    config = re.sub(r"(IGNORE = \[.*\])", f"\\1, '{symbol}'", config)
    print(f"Added '{symbol}' to IGNORE")
else:
    print(f"'{symbol}' already exists in IGNORE")

try:
    with open(generate_ts_config_path, 'w') as f:
        f.write(config)
    print(f"Updated file: {generate_ts_config_path}")
except IOError as e:
    print(f"Error updating file: {generate_ts_config_path}")
    print(f"Error: {e}")

# Update fetch_new_lists.sh
fetch_new_lists_path = os.path.join(os.path.dirname(__file__), 'fetch_new_lists.sh')
try:
    with open(fetch_new_lists_path, 'a') as f:
        f.write(f'\npython update_list.py -o {chain_name.lower()}.tokenlist.json -c {chain_name.lower()} --logos')
    print(f"Updated file: {fetch_new_lists_path}")
except IOError as e:
    print(f"Error updating file: {fetch_new_lists_path}")
    print(f"Error: {e}")

# Add symbol to symbols_farms.txt, symbols_top.txt, and symbols_all.txt if not already present
for filename in ['symbols_farms.txt', 'symbols_top.txt', 'symbols_all.txt']:
    file_path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(file_path, 'r+') as f:
            content = f.read()
            if symbol not in content:
                f.write(f'\n{symbol}')
        print(f"Updated file: {file_path}")
    except IOError as e:
        print(f"Error updating file: {file_path}")
        print(f"Error: {e}")

print("If this has succeeded, remember to put WETH logo in address folder.")