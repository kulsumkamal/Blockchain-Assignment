import hashlib
import pandas as pd
import streamlit as st
from datetime import datetime


# Define a class to represent a block in a government blockchain system.
class GovernmentBlock:
    def __init__(self, index, timestamp, data, location, name, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.location = location
        self.name = name
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(
            f"{self.index}{self.timestamp}{self.data}{self.location}{self.name}{self.previous_hash}".encode()
        ).hexdigest()


# Function to save government transactions to separate files based on action.
def save_transaction(block, action):
    filename = (
        "land_registry_blocks.txt"
        if action == "Land Registry Update"
        else "identity_blocks.txt"
    )
    with open(filename, "a") as file:
        if action == "Land Registry Update":
            file.write(
                f"{block.index},{block.timestamp},{block.data},{block.location},{block.previous_hash},{block.hash}\n"
            )
        elif action == "New Identity Added":
            file.write(
                f"{block.index},{block.timestamp},{block.data},{block.name},{block.previous_hash},{block.hash}\n"
            )


# Function to load government blockchain blocks from separate files based on action.
def load_blocks(action):
    filename = (
        "land_registry_blocks.txt"
        if action == "Land Registry Update"
        else "identity_blocks.txt"
    )
    try:
        with open(filename, "r") as file:
            blocks = []
            for line in file:
                parts = line.strip().split(",")
                if action == "Land Registry Update":
                    block = GovernmentBlock(
                        int(parts[0]), parts[1], parts[2], parts[3], "", parts[4]
                    )
                elif action == "New Identity Added":
                    block = GovernmentBlock(
                        int(parts[0]), parts[1], parts[2], "", parts[3], parts[4]
                    )
                block.hash = parts[5]
                blocks.append(block)
            return blocks
    except FileNotFoundError:
        return []


# Function to create the genesis block for a government blockchain.
def create_genesis_block():
    return GovernmentBlock(0, str(datetime.now()), "Genesis Block", "", "", "0")


# Function to simulate a land registry update (transaction).
def simulate_land_registry_update(blocks, location):
    blocks_count = len(blocks)
    previous_block = blocks[-1]
    timestamp = str(datetime.now())
    transaction_data = "Land Registry Update"
    new_block = GovernmentBlock(
        blocks_count, timestamp, transaction_data, location, "", previous_block.hash
    )
    save_transaction(new_block, "Land Registry Update")
    blocks.append(new_block)


# Function to simulate adding a new identity (transaction).
def simulate_add_identity(blocks, name):
    blocks_count = len(blocks)
    previous_block = blocks[-1]
    timestamp = str(datetime.now())
    transaction_data = "New Identity Added"
    new_block = GovernmentBlock(
        blocks_count, timestamp, transaction_data, "", name, previous_block.hash
    )
    save_transaction(new_block, "New Identity Added")
    blocks.append(new_block)


# Streamlit application to display government blockchain information.
def main():
    st.markdown(
        "## Government Blockchain: Land Registry and Identity Management - By Kulsum Kamal"
    )

    # Create tabs for land registry and adding identity.
    tabs = st.sidebar.radio(
        "Choose an Action", ("Update Land Registry", "Add New Identity")
    )

    # Load existing government blockchain blocks or create the genesis block if none exist.
    land_registry_blocks = load_blocks("Land Registry Update")
    identity_blocks = load_blocks("New Identity Added")

    if not land_registry_blocks:
        land_registry_blocks.append(create_genesis_block())

    if not identity_blocks:
        identity_blocks.append(create_genesis_block())

    # Display the appropriate action based on the selected tab.
    if tabs == "Update Land Registry":
        # Input field for location (land).
        location = st.text_input("Enter Location of Land:")
        if st.button("Update Land Registry") and location:
            simulate_land_registry_update(land_registry_blocks, location)
        st.markdown("## Land Registry Database")
        if len(land_registry_blocks) > 1:
            df = pd.DataFrame(
                {
                    "Timestamp": [
                        block.timestamp for block in land_registry_blocks[1:]
                    ],
                    "Transaction Type": [
                        block.data for block in land_registry_blocks[1:]
                    ],
                    "Location": [block.location for block in land_registry_blocks[1:]],
                    "Previous Hash": [
                        block.previous_hash for block in land_registry_blocks[1:]
                    ],
                    "Hash": [block.hash for block in land_registry_blocks[1:]],
                }
            )
            st.dataframe(df)
        else:
            st.write("No land registry updates yet.")

    elif tabs == "Add New Identity":
        # Input field for person's name (identity).
        name = st.text_input("Enter Name of Citizen:")
        if st.button("Add New Identity") and name:
            simulate_add_identity(identity_blocks, name)
        st.markdown("## Citizen Identity Database")
        if len(identity_blocks) > 1:
            df = pd.DataFrame(
                {
                    "Timestamp": [block.timestamp for block in identity_blocks[1:]],
                    "Transaction Type": [block.data for block in identity_blocks[1:]],
                    "Person's Name": [block.name for block in identity_blocks[1:]],
                    "Previous Hash": [
                        block.previous_hash for block in identity_blocks[1:]
                    ],
                    "Hash": [block.hash for block in identity_blocks[1:]],
                }
            )
            st.dataframe(df)
        else:
            st.write("No new identities added yet.")


if __name__ == "__main__":
    main()