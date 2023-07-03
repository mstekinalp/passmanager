from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def generate_key(password):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password=password)
        # Change "No Encryption()" if you want to add password
    )

    with open('private_key.pem', 'wb') as f:
        f.write(pem)
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('public_key.pem', 'wb') as f:
        f.write(pem)


def encrypt(to_encrypt):
    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    encrypt_to = to_encrypt.encode()
    encrypted = public_key.encrypt(
        encrypt_to,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted.decode('cp855')


def decrypt(to_decrypt, password_key):
    decrypt_to = to_decrypt.encode('cp855')
    password_key_en = password_key.encode()
    try:
        with open("private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=password_key_en,
                backend=default_backend()
            )
    except Exception as e:
        print(e)
    else:
        original_message = private_key.decrypt(
            decrypt_to,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return original_message.decode('cp855')
