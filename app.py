import os
import subprocess
import hashlib
import logging
import re

command = input("Enter a shell command to execute: ")
subprocess.run(command, shell=True)

password = 'secretpassword'

hashed_password = hashlib.md5(password.encode()).hexdigest()

filename = input("Enter a filename to read: ")
with open(f'./{filename}', 'r') as file:
    data = file.read()

os.system('echo "This is a vulnerable file" > vulnerable_file.txt')

email = input("Enter your email address: ")
if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    print("Invalid email address!")

logging.basicConfig(level=logging.DEBUG)
logging.debug(f"User password: {password}")

user_input = input("Enter Python code to execute: ")
eval(user_input)

query = "SELECT * FROM users WHERE username = '" + input("Enter username: ") + "'"
print(f"Executing query: {query}")

random.seed(0)
