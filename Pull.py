from cryptography.fernet import Fernet
from os import environ, listdir, getcwd
from os.path import isfile, join
import subprocess
import os
key = environ['k'].encode("utf-8")


if os.name == 'nt':
    path = "C:\\Stream-Deck-Icons"
    print("Pulling from  Github")
    subprocess.run("git pull origin main")


files = []
[files.append(os.path.join(r, file))
     for r, d, f in os.walk(path + '/Encrypted') for file in f]

for i in files:    
    os.makedirs(os.path.dirname(i.replace("Encrypted", "Decrypted")), exist_ok=True)
    with open(i, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.decrypt(data)

    with open(i.replace("Encrypted", "Decrypted"), 'wb') as f:
        f.write(encrypted)