import requests
import random
import time
import os
import ctypes
import threading
from colorama import Fore, init
import STikTok
from urllib.parse import urlencode
init(autoreset=True)

banner = """

                    ╔═╗╔╗╔╔═╗╦ ╦
                    ╚═╗║║║║ ║║║║
                    ╚═╝╝╚╝╚═╝╚╩╝

"""

def Print(text: str):
    print(
        f"            {Fore.LIGHTBLUE_EX}->{Fore.LIGHTCYAN_EX} {text} {Fore.LIGHTBLUE_EX}<- {Fore.RESET}")


def Input(text: str):
    print(
        f"\r            {Fore.LIGHTBLUE_EX}->{Fore.LIGHTCYAN_EX} {text} {Fore.LIGHTBLUE_EX}-> {Fore.RESET}", end="")
    return input()


class Registry():
    def __init__(self):
        self.done = 0
        self.err = 0
        self.sleep = 300
        self.run = True
        os.system("mode 70,10")
        ctypes.windll.kernel32.SetConsoleTitleW("Made By D7 or @d7ld & F15")
        print(f"{Fore.LIGHTBLUE_EX}{banner}")
        Print("TikTok Accounts Creator")
        self.main()

    def main(self):
        account = int(Input("How Many Accounts Do You Want : "))
        sleep = int(Input("Sleep [20 - 60] : "))
        threading.Thread(target=self.printer).start()
        for i in range(account):
            while True:
                try:
                    req, birth, username, password = self.register_account()
                    if str(req).__contains__("session_key"):
                        sessionkey = req["data"]["session_key"]
                        self.validate_account(sessionkey, birth)
                        with open(f"accounts.txt", "a") as accounts:
                            accounts.write(
                                f"Username : {username}\nPassword : {password}\nSessionid : {sessionkey}\n")
                            accounts.close()
                        with open(f"sessionids.txt", "a") as sessionids:
                            sessionids.write(f"{sessionkey}\n")
                            sessionids.close()
                        self.done += 1
                        break
                    elif str(req).__contains__('Too many attempts. Try again later.'):
                        self.err += 1
                        time.sleep(self.sleep)
                    else:
                        self.err +=1
                        time.sleep(self.sleep)
                except Exception as e:
                    continue
            time.sleep(sleep)
        self.run = False
        print()
        Print(f"{self.done} Accounts Has Been Created")
        Input("Enter To Exit")
        os._exit(0)

    def _get_device(self):
        device = STikTok.Device_Genrator()
        STikTok.CaptchaSolver(
            did=device["device_id"], iid=device["install_id"])
        return device

    def printer(self):
        while self.run:
            print(
                f"\r            {Fore.LIGHTBLUE_EX}->{Fore.LIGHTCYAN_EX} Done : {self.done} | Errors : {self.err} {Fore.LIGHTBLUE_EX}<- {Fore.RESET}", end="")
            time.sleep(0.70)

    def _validate_account_params(self):
        device = self._get_device()
        return urlencode({
            "residence": "SA",
            "device_id": device["device_id"],
            "os_version": "14.4",
            "iid": device["install_id"],
            "app_name": "musical_ly",
            "locale": "en",
            "ac": "WIFI",
            "sys_region": "SA",
            "js_sdk_version": "1.77.0.2",
            "version_code": "21.1.0",
            "channel": "App Store",
            "vid": "7094F26A-EC10-45E4-8854-5D0616167B08",
            "op_region": "SA",
            "tma_jssdk_version": "1.77.0.2",
            "os_api": "18",
            "idfa": "D2CF453D-6981-4F32-A0EB-7A200FED8504",
            "device_platform": "ipad",
            "device_type": "iPad11,6",
            "openudid": device["openudid"],
            "account_region": "",
            "tz_name": "Asia/Riyadh",
            "tz_offset": "10800",
            "app_language": "en",
            "current_region": "SA",
            "build_number": "211023",
            "aid": "1233",
            "mcc_mnc": "",
            "screen_width": "1620",
            "uoo": "1",
            "content_language": "",
            "language": "en",
            "cdid": device["cdid"],
            "app_version": "21.1.0"
        })

    def validate_account(self, sessionkey, birthday):
        return requests.post("https://api16-normal-c-alisg.tiktokv.com/aweme/v3/user/info/sync/?"+self._validate_account_params(), headers={
            'Cookie': f'sessionid='+sessionkey,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'TikTok 21.1.0 rv:211023 (iPad; iOS 14.4; en_SA@calendar=gregorian) Cronet',
            'Sdk-Version': '2'
        }, data=birthday).text

    def _get_random_password(self):
        l = "".join(random.choice(
            "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM") for i in range(6))
        c = "".join(random.choice("@#") for i in range(2))
        n = "".join(random.choice("1234567890") for i in range(4))
        return l + n + c

    def _get_random_username(self):
        l = "".join(random.choice("qwertyuiopasdfghjklzxcvbnm1234567890_")
                    for i in range(7))
        return l

    def register_account(self):
        birthday = f"birthday=1986-01-02"
        password = self._get_random_password()
        username = self._get_random_username()
        deviceid = self._get_device()["device_id"]
        params = STikTok.Sign(f"aid=143243&device_id={deviceid}&verifyFp=verify_lbtcmozr_SV8EAMJv_poB2_4xJD_9klD_JPCNTTpXYuy2&webcast_language=ar&msToken={STikTok.msToken(None)}",
                              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")
        url = f'https://api22-normal-c-useast1a.tiktokv.com/passport/web/username/register/?'+params
        r = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded', "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                          "Referer": "https://www.tiktok.com/"}, data=f'mix_mode=1&password={password}&aid=1459&account_sdk_source=web&language=en&{birthday}&username={username}', verify=True, timeout=3, allow_redirects=True).json()
        return r, birthday, username, password


Registry()
