import hashlib
import requests

from .utilities import *
from .device import *
from urllib.parse import urlencode


class Applog:
    def __init__(self, device: dict or None = None, proxy: str or None = None) -> tuple:
        self.__device = Device.gen_device() if device is None else device
        self.__host = "log-va.tiktokv.com"
        self.proxies = {'http': f'http://{proxy}',
                        'http': f'http://{proxy}'} if proxy else None

    def __get_headers(self, params: str, payload: bytes):
        sig = Utils._sig(
            params=params,
            body=payload
        )

        return {
            "x-ss-stub": str(hashlib.md5(payload).hexdigest()).upper(),
            "accept-encoding": "gzip",
            "passport-sdk-version": "17",
            "sdk-version": "2",
            "x-ss-req-ticket": str(int(time.time()) * 1000),
            "x-gorgon": sig["X-Gorgon"],
            "x-khronos": sig["X-Khronos"],
            "content-type": "application/octet-stream;tt-data=a",
            "host": "log-va.tiktokv.com",
            "connection": "Keep-Alive",
            "user-agent": "okhttp/3.10.0.1"
        }

    def get_params(self):
        return urlencode(
            {
                "ac": "wifi",
                "channel": "googleplay",
                "aid": APP["aid"],
                "app_name": "musically_ly",
                "version_code": APP["version_code"],
                "version_name": APP["version"],
                "device_platform": "android",
                "ab_version": APP["version"],
                "ssmix": "a",
                "device_type": self.__device["device_model"],
                "device_brand": self.__device["device_brand"],
                "language": "en",
                "os_api": 25,
                "os_version": "7.1.2",
                "openudid": self.__device["openudid"],
                "manifest_version_code": APP["version_code"],
                "resolution": self.__device["resolution"],
                "dpi": 320,
                "update_version_code": APP["version_code"],
                "_rticket": int(time.time() * 1000),
                "storage_type": 0,
                "app_type": "normal",
                "sys_region": "US",
                "pass-route": 1,
                "pass-region": 1,
                "timezone_name": self.__device["tz_name"],
                "timezone_offset": self.__device["tz_offset"],
                "carrier_region_v2": 310,
                "cpu_support64": "false",
                "host_abi": "armeabi-v7a",
                "ts": int(time.time()),
                "build_number": APP["version"],
                "region": "US",
                "uoo": 0,
                "app_language": "en",
                "carrier_region": "IE",
                "locale": "en",
                "op_region": "IE",
                "ac2": "wifi",
                "cdid": self.__device["cdid"],
                "tt_data": "a"
            }
        )

    def __get_payload(self):
        return {
            "magic_tag": "ss_app_log",
            "header": {
                "display_name": "TikTok Lite",
                "update_version_code": APP["version_code"],
                "manifest_version_code": APP["version_code"],
                "app_version_minor": "",
                "aid": 1340,
                "channel": "googleplay",
                "package": "com.zhiliaoapp.musically.go",
                "app_version": "16.9.4",
                "version_code": APP["version_code"],
                "sdk_version": "2.12.1-rc.6-lite",
                "sdk_target_version": 29,
                "git_hash": APP["git_hash"],
                "os": "Android",
                "os_version": "7.1.2",
                "os_api": 25,
                "device_model": self.__device["device_model"],
                "device_brand": self.__device["device_brand"],
                "device_manufacturer": self.__device["device_brand"],
                "cpu_abi": "armeabi-v7a",
                "release_build": APP["release_build"],
                "density_dpi": 320,
                "display_density": "xhdpi",
                "resolution": self.__device["resolution"],
                "language": "en",
                "timezone": 2,
                "access": "wifi",
                "not_request_sender": 0,
                "carrier": "Android",
                "mcc_mnc": "42001",
                "rom": f'rel.se.{"".join(random.choices("qwertyuiopasdfghjklzxcvbnm", k=5))}.{random.randrange(10000000, 23487690)}.{random.randrange(100000, 999999)}',
                "rom_version": f"beyond1qlteue-user 7.1.2 PPR1.190810.011 {random.randrange(10000000, 62994552)}.{random.randrange(100000, 999999)} release-keys",
                "cdid": self.__device["cdid"],
                "sig_hash": APP["sig_hash"],
                "gaid_limited": 0,
                "google_aid": self.__device["google_aid"],
                "openudid": self.__device["openudid"],
                "clientudid": self.__device["clientudid"],
                "region": "US",
                "tz_name": self.__device["tz_name"],
                "tz_offset": self.__device["tz_offset"],
                "sim_region": "IE",
                "oaid_may_support": False,
                "req_id": self.__device["req_id"],
                "apk_first_install_time": self.__device["install_time"],
                "is_system_app": 0,
                "sdk_flavor": "global"
            },
            "_gen_time": int(round(time.time() * 1000))
        }

    def register_device(self):
        try:
            params = self.get_params()
            payload = self.__get_payload()
            # print(payload["header"]["rom_version"])
            payload = bytes.fromhex(Utils._ttencrypt(payload))
            r = requests.post(
                url=(
                    "http://" +
                    self.__host
                    + "/service/2/device_register/?"
                    + params
                ),
                headers=self.__get_headers(params, payload),
                data=payload,
                proxies=self.proxies
            )
            # print(r.json())

            if len(str(r.json()["device_id"])) > 6:
                self.__device["device_id"] = r.json()["device_id"]
                self.__device["install_id"] = r.json()["install_id"]
                return self.__device
        except Exception as e:
            # print(e)
            pass
