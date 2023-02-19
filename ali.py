import hashlib
import ecdsa
import requests
import random

appId = "5dde4e1bdf9e4966b387ba58f4b3fdc3"
nonce = 0


def r(appId: str, deviceId: str, userId: str, nonce: int) -> str:
    return f"{appId}:{deviceId}:{userId}:{nonce}"


def createSession(deviceId, signature, public_key, jwt) -> bool:
    headers = {
        "authorization": f"Bearer {jwt}",
        "origin": "https://www.aliyundrive.com",
        "referer": "https://www.aliyundrive.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41",
        "x-canary": "client=web,app=adrive,version=v3.17.0",
        "x-device-id": deviceId,
        "x-signature": signature,
    }
    req = requests.post(
        "https://api.aliyundrive.com/users/v1/users/device/create_session",
        json={
            "deviceName": "Edge浏览器",
            "modelName": "Windows网页版",
            "pubKey": public_key,
        },
        headers=headers)

    print(req.json())
    if (req.json()["message"] == None):
        return req.json()["success"], None
    return False, req.json()["message"]


def getSign(deviceId, userId):
    private_key = random.randint(1, 2**256-1)
    print(f'private_key: {private_key}')
    ecc_pri = ecdsa.SigningKey.from_secret_exponent(
        private_key, curve=ecdsa.SECP256k1)
    ecc_pub = ecc_pri.get_verifying_key()
    public_key = "04"+ecc_pub.to_string().hex()
    print(f'private_key: {public_key}')
    sign_dat = ecc_pri.sign(r(appId, deviceId, userId, nonce).encode('utf-8'), entropy=None,
                            hashfunc=hashlib.sha256)
    signature = sign_dat.hex()+"01"
    return signature, public_key


def sign(deviceId, userId, jwt):

    signInfo = getSign(deviceId, userId)
    print(signInfo)

    result = createSession(deviceId, signInfo[0], signInfo[1], jwt)
    if (result[0]):
        return signInfo
    return result
