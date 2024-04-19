import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from termcolor import colored, cprint

# Pre-defined encryption key
ENCRYPTION_KEY = b'ThisIsASecretKey' # AES-128, must be 16 characters

def encrypt_file(file_path):
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_EAX)
    with open(file_path, 'rb') as file:
        data = file.read()
    ciphertext, tag = cipher.encrypt_and_digest(data)
    encrypted_file_path = f"{file_path}.enc"
    with open(encrypted_file_path, 'wb') as file:
        file.write(cipher.nonce)
        file.write(tag)
        file.write(ciphertext)
    cprint("Encryption successful.", color='green')

def decrypt_file(file_path):
    if not file_path.endswith('.enc'):
        cprint("Error: This file is not encrypted.", color='red')
        return

    with open(file_path, 'rb') as file:
        nonce = file.read(16)
        tag = file.read(16)
        ciphertext = file.read()
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    filename, _ = os.path.splitext(os.path.basename(file_path))
    decrypted_filename = f"decrypted_{filename}"
    decrypted_file_path = os.path.join(os.path.dirname(file_path), decrypted_filename)
    with open(decrypted_file_path, 'wb') as file:
        file.write(data)
    cprint("Decryption successful.", color='green')

def get_files_in_directory(directory):
    return [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

def main():
    script_directory = os.path.dirname(__file__)

    cprint("\nAES File Encryption and Decryption Tool", color='red')

    while True:
        files = get_files_in_directory(script_directory)

        print(colored("\n1. Encrypt a file", 'yellow'))
        print(colored("2. Decrypt a file", 'yellow'))
        print(colored("3. Exit", 'yellow'))
        operation = input("\nSelect Operation: ")

        if operation == '3':
            break

        if operation not in ['1', '2']:
            cprint("Invalid operation.", color='red')
            continue

        cprint("\nFiles in directory:", color='cyan')
        cprint(files, color='cyan')
        file_name = input("\nEnter filename with extension: ")
        if file_name not in files:
            cprint("File not found in directory.", color='red')
            continue

        file_path = os.path.join(script_directory, file_name)
        if operation == '1':
            encrypt_file(file_path)
        else:
            decrypt_file(file_path)
            if not file_path.endswith('.enc'):
                continue

        continue_program = input("\nDo you want to continue the program? (y/n): ").lower()
        if continue_program == 'n':
            break
        elif continue_program != 'y':
            cprint("Invalid input. Please enter 'y' or 'n'.", color='red')

if __name__ == "__main__":
    main()