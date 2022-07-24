from message import Message
from consts import *
from cryptography.hazmat.primitives.asymmetric.ec import *
from cryptography.hazmat.primitives.serialization import *
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
import cryptography
from util import *
from data import Data
import os


def handle(message: Message):
    print("handling msg")
    data = message.data
    ins = data[1]
    p1 = data[2]
    print("ins", ins)
    if ins == U2F_REGISTER:
        req_data_len = (data[4] << 16) | (data[5] << 8) | data[6]
        # TODO: validate that req_data_len is 64
        req_data = data[7:7 + req_data_len]
        challenge_param = req_data[:32]
        application_param = req_data[32:]
        # generate new keypair

        # implementing yubico's method for creating a key
        # https://developers.yubico.com/U2F/Protocol_details/Key_generation.html

        private_key = generate_private_key(curve=SECP256R1)
        public_key = private_key.public_key().public_bytes(
            encoding=Encoding.X962, format=PublicFormat.UncompressedPoint)
        master_key_file = open("keys/masterkey.bin", "rb")
        master_key = master_key_file.read()
        master_key_file.close()

        private_key_bytes = private_key.private_bytes(
            encoding=Encoding.DER, format=PrivateFormat.PKCS8, encryption_algorithm=NoEncryption())
        print("private key bytes", private_key_bytes)
        aesccm = AESCCM(master_key)
        nonce = os.urandom(13)
        key_handle = nonce + \
            aesccm.encrypt(nonce, private_key_bytes, bytes(application_param))
        key_handle_len = len(key_handle).to_bytes(1, byteorder="big")
        print("key handle", key_handle, len(key_handle))
        cert_file = open("keys/certificate.der", "rb")
        attestation_cert = cert_file.read()
        cert_file.close()

        key_file = open("keys/ecprivkey.pem", "rb")
        attestation_key = load_pem_private_key(
            data=key_file.read(), password=None
        )
        key_file.close()

        sig_data = bytes((0,)) + application_param + \
            challenge_param + key_handle + public_key
        signature = attestation_key.sign(
            sig_data,
            ECDSA(hashes.SHA256())
        )

        # print("signature", format_bytes(signature), len(signature))
        res_data = bytes((5,)) + public_key + key_handle_len + \
            key_handle + attestation_cert + signature
        # status words
        res_data += SW_NO_ERROR.to_bytes(2, byteorder="big")
        # print("res data", format_bytes(res_data))
        response = build_response(message.cid, message.cmd, res_data)
        input("type to simulate touching the key: ")
        return response
    elif ins == U2F_AUTHENTICATE:
        req_data_len = (data[4] << 16) | (data[5] << 8) | data[6]
        req_data = data[7:7 + req_data_len]
        print("all data", format_bytes(data))
        print("req_data", format_bytes(req_data))
        control_byte = p1
        challenge_param = req_data[0:32]
        application_param = req_data[32:64]
        key_handle_len = req_data[64]
        key_handle = req_data[65:65 + key_handle_len]
        nonce = key_handle[:13]
        ciphertext = key_handle[13:]

        master_key_file = open("keys/masterkey.bin", "rb")
        master_key = master_key_file.read()
        master_key_file.close()

        aesccm = AESCCM(master_key)
        try:
            private_key_data = aesccm.decrypt(
                nonce, bytes(ciphertext), bytes(application_param))
        except cryptography.exceptions.InvalidTag as e:
            print("key handle doesn't match application param")
            return build_response(
                message.cid, message.cmd, SW_WRONG_DATA.to_bytes(
                    2, byteorder="big"
                )
            )
        private_key = load_der_private_key(private_key_data, None)

        print("control byte", control_byte)
        if control_byte == 0x70:  # check only
            # already verified key handle above
            return build_response(
                message.cid, message.cmd, SW_CONDITIONS_NOT_SATISFIED.to_bytes(
                    2, byteorder="big"
                )
            )
        # enforce user presence and sign OR don't enforce user presence and sign
        elif control_byte == 0x03 or control_byte == 0x08:
            user_presence = bytes(
                (0,)) if control_byte == 0x08 else bytes((1,))
            counter = Data.counter.to_bytes(4, byteorder="big")
            sig_data = application_param + user_presence + counter + challenge_param
            signature = private_key.sign(
                sig_data,
                ECDSA(hashes.SHA256())
            )
            if control_byte == 0x03:  # enforce user presence
                input("type to simulate touching the key: ")
            res_data = user_presence + counter + signature + \
                SW_NO_ERROR.to_bytes(2, byteorder="big")
            print('response data', format_bytes(res_data))
            Data.counter += 1
            return build_response(
                message.cid, message.cmd, res_data
            )
        else:
            raise Exception(f"Unrecognized control byte {control_byte}")
    elif ins == U2F_VERSION:
        return build_response(message.cid, message.cmd, b'U2F_V2' + SW_NO_ERROR.to_bytes(2, byteorder="big"))
    else:
        raise Exception(f"Unrecognized ins {ins}")
