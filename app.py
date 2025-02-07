import os
import subprocess
import hashlib
import getpass
import logging
import re

# Use a safer method for user input (avoid using input for sensitive data)
username = input("Enter your username: ")

# Validate username (ensure the username is valid and prevent hardcoded 'admin' username)
if not re.match(r'^[a-zA-Z0-9_]+$', username):  # Basic alphanumeric check for username
    print("Invalid username format.")
else:
    print(f"Hello, {username}!")

# Use a more secure method to handle passwords
password = getpass.getpass("Enter your password: ")

# Use a stronger hashing algorithm (e.g., SHA-256) for password storage
hashed_password = hashlib.sha256(password.encode()).hexdigest()

# Use subprocess securely, with a predefined list of safe commands
safe_command = ['echo', 'This is a safe command execution']
subprocess.run(safe_command, check=True)

# Write to a file securely using the 'with' statement
file_path = "vulnerable_file.txt"
with open(file_path, 'w') as file:
    file.write("This is a secure file.")

# Proper logging (ensure sensitive data is not logged)
logging.basicConfig(level=logging.INFO)
logging.info(f"User '{username}' has executed the program.")

# Secure method of reading files (use exception handling for file-related operations)
filename = input("Enter a filename to read: ")
try:
    with open(filename, 'r') as file:
        data = file.read()
    print(f"Contents of {filename}: {data}")
except FileNotFoundError:
    print(f"The file {filename} was not found.")
except IOError as e:
    print(f"An error occurred while reading the file: {e}")
