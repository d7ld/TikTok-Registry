
import binascii
import uuid
import time
import random
import os
APP = {
    "version_code": 160904,
    "sig_hash": "aea615ab910015038f73c47e45d21466",
    "version": "16.9.4",
    "release_build": "f05822b_20201014",
    "git_hash": "9f888696",
    "aid": 1340
}


class Device:
    @staticmethod
    def __openudid() -> str:
        return binascii.hexlify(os.urandom(8)).decode()

    @staticmethod
    def __uuid() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def __install_time() -> int:
        return int(round(time.time() * 1000)) - random.randint(13999, 15555)

    @staticmethod
    def __ut() -> str:
        return random.randint(100, 500)

    @staticmethod
    def __uid() -> int:
        return random.randrange(10000, 10550, 50)

    @staticmethod
    def __ts() -> int:
        return round(random.uniform(1.2, 1.6) * 100000000) * -1

    @staticmethod
    def __cba() -> str:
        return f"0x{os.urandom(4).hex()}"

    @staticmethod
    def __hc() -> str:
        return f"0016777{random.randint(260, 500)}"

    @staticmethod
    def __dp() -> str:
        return f"{random.randint(700000000, 900000000)},0,0"

    @staticmethod
    def __rom() -> int:
        return str(random.randint(700000000, 799999999))

    @staticmethod
    def gen_device() -> dict:
        return {
            "device_model": "G011A",
            "device_serial": "G011A",
            "resolution": "1024x576",
            "resolution2": "576*1024",
            "device_brand": "google",
            "openudid": Device.__openudid(),
            "google_aid": Device.__uuid(),
            "clientudid": Device.__uuid(),
            "cdid": Device.__uuid(),
            "req_id": Device.__uuid(),
            "install_time": Device.__install_time(),
            "ut": Device.__ut(),
            "ts": Device.__ts(),
            "cba": Device.__cba(),
            "hc": Device.__hc(),
            "dp": Device.__dp(),
            "rom": Device.__rom(),
            "uid": Device.__uid(),
            "tz_name": "Asia/Shanghai",
            "tz_offset": 28800,
            "device_id": 0000000000000000000,
            "install_id": 0000000000000000000,
            "install_time": int(round(time.time() * 1000)) - random.randint(13999, 15555)
        }
