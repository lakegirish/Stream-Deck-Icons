from cryptography.fernet import Fernet
from os import environ, listdir, getcwd
from os.path import isfile, join
import subprocess
import os
import time
from datetime import datetime
import pickle
import pandas as pd
import hashlib
path = "C:\\Stream-Deck-Icons"

  
def GitAdd():
    print("Sending to Github")
    subprocess.run("git add .")
    subprocess.run("git status")
    subprocess.run("git commit -m """"Python""""")
    subprocess.run("git push origin main")
    print("Send Complete")


def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def Get_md5_from_directory():

    files = []
    [files.append(os.path.join(r, file))
     for r, d, f in os.walk(path + '/Decrypted') for file in f]

    return {i: md5Checksum(i) for i in files}


def Store_md5_to_db():
    files = []
    [files.append(os.path.join(r, file))
     for r, d, f in os.walk(path + '/Decrypted') for file in f]

    hl = {i: md5Checksum(i) for i in files}
    os.makedirs(os.path.dirname(path + '/Decrypted/db.pkl'), exist_ok=True)
    with open(path + '/Decrypted/db.pkl', 'wb') as handle:
        pickle.dump(hl, handle, protocol=pickle.HIGHEST_PROTOCOL)


def Get_md5_from_db():
    if(os.path.exists(path + '/Decrypted/db.pkl')):
        with open(path + '/Decrypted/db.pkl', 'rb') as handle:
            hl = pickle.load(handle)
        return hl
    else:
        print("Creating file db")
        Store_md5_to_db()


def Syncdir():
    encrypted_file = []
    decrypted_file = []
    delete_files = []
    [encrypted_file.append(os.path.join(r, file))
     for r, d, f in os.walk(path + '/Encrypted') for file in f]
    [decrypted_file.append(os.path.join(r, file))
     for r, d, f in os.walk(path + '/Decrypted') for file in f]
    decrypted_file = [i.replace("Decrypted", "Encrypted")
                      for i in decrypted_file]
    [delete_files.append(i) for i in encrypted_file if i not in decrypted_file]
    if delete_files:
        print(
            "Delete files in Encrypted folder but not in Decrypted folder: ", delete_files)

    # Delete files in Encrypted Folder which are not present in Decrypted folder
    for i in delete_files:
        if os.path.exists(i):
            os.remove(i)
            print("The file {} deleted".format(i))
        else:
            print("The file {} does not exist".format(i))

    # Delete Empty Folders in Encrypted Folder
    ls = [x[0] for x in os.walk(path + '/Encrypted')][::-1]
    for i in ls:
        if os.path.isdir(i):
            if not os.listdir(i):
                os.rmdir(i)


if __name__ == '__main__':
    db = Get_md5_from_db()
    if not db:
        print("Directory is Empty!! No changes in Git required")
        db = {}
    directory = Get_md5_from_directory()
    if directory:
        for key, value in directory.items():
            if "/Tools" not in key:
                if db.get(key) == value:
                    print("No change in {} having signature{}".format(key, value))
                else:
                    filename = key.replace("Decrypted", "Encrypted")
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(key, 'rb') as fread:
                        data = fread.read()

                    fernet = Fernet(environ['k'].encode("utf-8"))
                    encrypted = fernet.encrypt(data)

                    with open(filename, 'wb') as fread:
                        fread.write(encrypted)
            if not (os.path.exists(path + '/Encrypted')):
                os.makedirs(os.path.dirname(path + '/Encrypted'), exist_ok=True)

        Syncdir()
        GitAdd()
    Store_md5_to_db()
