
import binascii
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
import binascii

#random_generator = Random.new().read
#private_key = RSA.generate(1024, random_generator)
#public_key = private_key.publickey()

#private_key = private_key.exportKey(format='DER')
#public_key = public_key.exportKey(format='DER')

#private_key: str = binascii.hexlify(private_key).decode('utf8')
#public_key: str = binascii.hexlify(public_key).decode('utf8')

#print("PRIVATE:", private_key, ":")
#print("PUBLIC: ", public_key, ":")

private_key: str = "3082025d02010002818100b73d870408f10733c5628f78585a0980b5cba510a9eabbe1c59cd91dfd186f2ede57de48f3344b4d8763282f17c645f8cd0ce9bf3eee6011e4ceff3c26378c4ee0706820ba10de6a233650f9a00b421d3fa930c22e5118e4f160e1e2a2143acc6896ae9be8f8a31a289e88ac975ec3533e0e927dd716d7e2cb519c6e2aa16a89020301000102818006855bc3eebe871b564ba8dfe74303020fd628b0645f9c628f3a02f7007e095ce1603ea2997713b3f55cb7be1f4a38ccbf1d55c72ec9e464d69ff030d78a54059e1d1b34a16cc7534378ac1f03c680bfb8c3db9759cb5e955fcd869641e00abec45f9cd368e0e2e24634a05d60b83c369d42a87a3f96cccf05f7562c8039dd81024100c8e8b805270368720a85996268956a3d384584488990b5bf0d694b5905196ec50c3a2b00c5e2b9ed077144805c3a822dbbb5aaffdc876154a23d4ac38afcb3c9024100e97c82fee2491e4316a3a51a2686efc0784630aa1e12a46e7c38f720997636fd0ea929c9c3cde74aebc9745bf83a2ffc1a65aa7208d316f81bd02ab7b95ee0c10241008dcf8e4cbcbbf016470d04366d21c20a9254a749d82817d1523317672f6d433dbd22b5c5e6e7e15ac89d0fc016d98997a45e57e4201243064d3a3c32884154d9024100906428da9974205bdad74ed6123766733fae209043d2c18f7611007b4f8c34cb6052aafe14b1f434780678881bc558416ecdaa8fa4f76dfff7ab4f8f98fa9cc10240426bd48edaf827bca5dc50258357555ed46f215952b082849b2560d7764d14c5525a51ad302db76ccaea748c39b4903defc1f0bd0ba6042dc6f53669e121e0a5"
#public_key: str = "30819f300d06092a864886f70d010101050003818d0030818902818100b73d870408f10733c5628f78585a0980b5cba510a9eabbe1c59cd91dfd186f2ede57de48f3344b4d8763282f17c645f8cd0ce9bf3eee6011e4ceff3c26378c4ee0706820ba10de6a233650f9a00b421d3fa930c22e5118e4f160e1e2a2143acc6896ae9be8f8a31a289e88ac975ec3533e0e927dd716d7e2cb519c6e2aa16a890203010001"

private_key = RSA.importKey(binascii.unhexlify(private_key))
public_key = private_key.publickey()


def encrypt(password: str):
    cipher = PKCS1_OAEP.new(public_key)
    encrypted = cipher.encrypt(str.encode(password))
    return binascii.hexlify(encrypted).decode('utf8')


def decrypt(hash: str):
    cipher = PKCS1_OAEP.new(private_key)
    hash = binascii.unhexlify(hash)
    return cipher.decrypt(hash).decode('utf8')

