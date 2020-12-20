from cryptography.fernet import Fernet
key = Fernet.generate_key().decode("utf-8")
f = open("../secret.key", "w")
f.write(key)
f.close()
print("Created key")
