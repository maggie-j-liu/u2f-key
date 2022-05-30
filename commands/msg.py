from message import Message
from consts import *
from cryptography.hazmat.primitives.asymmetric.ec import *
from cryptography.hazmat.primitives.serialization import *
from cryptography.hazmat.primitives import hashes
from util import *


def handle(message: Message):
    print("handling msg")
    data = message.data
    ins = data[1]
    p1 = data[2]
    req_data_len = (data[4] << 16) | (data[5] << 8) | data[6]
    print("ins", ins)
    if ins == U2F_REGISTER:
        # TODO: validate that req_data_len is 64
        req_data = data[7:7 + req_data_len]
        challenge_param = req_data[:32]
        application_param = req_data[32:]
        # generate new keypair
        public_key = generate_private_key(
            curve=SECP256R1).public_key().public_bytes(encoding=Encoding.X962, format=PublicFormat.UncompressedPoint)
        # print("public key", format_bytes(public_key), len(public_key))
        key_handle = bytes((1,))
        key_handle_len = len(key_handle).to_bytes(1, byteorder="big")
        cert_file = open("keys/certificate.der", "rb")
        attestation_cert = cert_file.read()
        cert_file.close()

        key_file = open("keys/ecprivkey.pem", "rb")
        attestation_key = load_pem_private_key(
            data=key_file.read(), password=None
        )
        key_file.close()

        print("app param", format_bytes(application_param),
              "chal param", format_bytes(challenge_param))
        sig_data = bytes((0,)) + application_param + \
            challenge_param + key_handle + public_key
        print(len(application_param), len(challenge_param),
              len(key_handle), len(public_key))
        signature = attestation_key.sign(
            sig_data,
            ECDSA(hashes.SHA256())
        )

        # print("signature", format_bytes(signature), len(signature))
        res_data = bytes((5,)) + public_key + key_handle_len + \
            key_handle + attestation_cert + signature
        # status words
        res_data += bytes((0x90, 0x00))
        print(len(public_key), len(key_handle_len), len(
            key_handle), len(attestation_cert), len(signature))
        # print("res data", format_bytes(res_data))
        response = build_response(message.cid, message.cmd, res_data)
        input("type to simulate touching the key")
        return response
    return False
