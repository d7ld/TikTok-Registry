import base64

from .utilities import Utils
from .applog import *


class Xlog:
    def __init__(self, proxy: str or None = None):
        self.__device = Applog(proxy=proxy).register_device()
        self.proxy = proxy
        self.proxies = {'http': f'http://{proxy}', 'http': f'http://{proxy}'} if proxy else None

    def _base_payload(
            self,
            extra: str = "install",
            slb: str = "<N/A>",
            hdf: str = "<N/A>",
            acg_m: int = 1,
            rebuild: int = -1,
            sg_s: int = 0,
            sign: str = "",
    ):

        __xlog_data = {
            "extra": extra,
            "grilock": "",
            "ast": 2,
            "p1": str(self.__device["device_id"]),
            "p2": str(self.__device["install_id"]),
            "ait": int(str(self.__device["install_time"])[:10]),
            "ut": self.__device["ut"],
            "pkg": "com.zhiliaoapp.musically.go",
            "prn": "CZL-MRP_T",
            "vc": 160904,
            "fp": f"{self.__device['device_brand']}/{self.__device['device_brand']}/{self.__device['device_model']}:7.1.2/{self.__device['rom']}:user/release-keys",
            "vpn": 0,
            "hw": {
                "brand": self.__device["device_brand"],
                "model": self.__device["device_model"],
                "board": "msm8998",
                "device": self.__device['device_model'],
                "product": self.__device['device_model'],
                "manuf": self.__device["device_brand"],
                "tags": "release-keys",
                "inc": self.__device['rom'],
                "des": f"{self.__device['device_brand']}-user 7.1.2 20171130.276299 release-keys",
                "bt": "uboot",
                "pfbd": "gmin",
                "display": self.__device['resolution2'],
                "dpi": 191,
                "wm_s": "",
                "wm_d": "",
                "bat": 1000,
                "bas": [],
                "cpu": {},
                "mem": {
                    "ram": "3185635328",
                    "rom": self.__device["rom"],
                    "sd": "9892421632"
                },
                "hdf": "<N/A>",
                "slb": "<N/A>"
            },
            "id": {
                "i": 25,
                "r": "7.1.2",
                "acg_m": -127,
                "onm": "42001"
            },
            "emulator": {},
            "env": {
                "ver": "0.6.11.29.18",
                "tag": "CZL_LAST_VER",
                "pkg": "com.zhiliaoapp.musically.go",
                "tz": "GMT+08:00",
                "ml": "en_US",
                "uid": self.__device["uid"],
                "mc": 0,
                "arch": 1,
                "e_arch": 3,
                "v_bnd": 7,
                "su": -1,
                "sp": "",
                "ro.secure_s": "1",
                "ro.debuggable_s": "0",
                "rebuild": -1,
                "jd": 0,
                "dbg": 0,
                "tid": 0,
                "trm": "",
                "dbg_st": -93,
                "dbg_tid": 2,
                "dbg_if": -1,
                "hph": "192.168.8.128",
                "hpp": "8080",
                "envrion": [],
                "oem_s": -1,
                "oem_a": -1,
                "xposed": 0,
                "frida": 0,
                "cydia": 0,
                "jexp": 0,
                "click": "",
                "acb": 0,
                "hook": [],
                "jvh": [],
                "fish": {},
                "vapp": "",
                "vmos": 0,
                "ssr": -1,
                "mal": "",
                "mor": 0,
                "mor2": 0,
                "ech": "4294967295"
            },
            "extension": {
                "sg": 1213,
                "sp": -1,
                "f_clk": 0,
                "u_clk": 0,
                "atify": "0x00000000",
                "notify": 1,
                "sg_s": 0,
                "path": "",
                "bdc": "",
                "dp": self.__device["dp"],
                "sign": "",
                "sha1": "",
                "inst": "com.bytedance.platform.godzilla.b.a.b.a",
                "AMN": "android.app.ActivityManagerProxy",
                "dump": 1,
                "dump2": 1,
                "mk": 0,
                "cba": self.__device["cba"],
                "ts1": -1890141920,
                "ts2": 0,
                "bqq": ""
            },
            "paradox": {},
            "gp_ctl": {
                "usb": -1,
                "adb": -1,
                "acc": ""
            },
            "custom_info": {},
            "hc": self.__device["hc"],
            "fch": "0000000000"
        }

        __xlog_data["fch"] = Utils._fch(json.dumps(__xlog_data).replace(" ", ""))

        return Utils._xlencrypt(
            json.dumps(
                __xlog_data, separators=(",", ":")
            ).replace(" ", "")
        )

    def __get_headers(self, params: str, data: (str or None) = None) -> dict:
        sig = Utils._sig(
            params=params,
            body=bytes.fromhex(data) if data is not None else None
        )

        headers = {
            "x-ss-stub": hashlib.md5(data.encode()).hexdigest().upper() if data is not None else None,
            "accept-encoding": "gzip",
            "cookie": "sessionid=",
            "x-gorgon": sig["X-Gorgon"],
            "x-khronos": sig["X-Khronos"],
            "content-type": "application/octet-stream" if data is not None else None,
            "host": "xlog-va.byteoversea.com",
            "connection": "Keep-Alive",
            "user-agent": "okhttp/3.10.0.1"
        }

        return {
            key: value for key, value in headers.items() if value is not None
        }

    def __get_params(self) -> str:
        return urlencode(
            {
                "os": 0,
                "ver": "0.6.11.29.19-MT",
                "m": 2,
                "app_ver": APP["version"],
                "region": "en_US",
                "aid": 1340,
                "did": self.__device['device_id'],
                "iid": self.__device['install_id']
            }
        )

    def __get_xlog(self) -> requests.Response:
        params = self.__get_params()

        return json.loads(
            XLEncrypt().decrypt(
                requests.get(
                    url="https://xlog-va.byteoversea.com/v2/s?" + params,
                    headers=self.__get_headers(params),
                    proxies=self.proxies
                ).content.hex()
            )
        )

    def __alert_check(self) -> bool:
        url = f"https://applog.musical.ly/service/2/app_alert_check/?iid={self.__device['install_id']}&device_id={self.__device['device_id']}&version_code={APP['version_code']}"
        headers = {
            "accept-encoding": "gzip",
            "x-ss-req-ticket": str(int(time.time() * 1000)),
            "sdk-version": "1",
            "user-agent": "okhttp/3.10.0.1",
        }

        response = requests.get(url, headers=headers, data={}, proxies=self.proxies)

        return response.json()

    def __xlog_install(self) -> dict:
        __xlog_data = self._base_payload()
        __xlog_params = self.__get_params()
        self.__alert_check()

        return json.loads(
            XLEncrypt().decrypt(
                requests.post(
                    url=(
                            "https://xlog-va.byteoversea.com/v2/r/?"
                            + __xlog_params
                    ),
                    data=bytes.fromhex(__xlog_data),
                    headers=self.__get_headers(__xlog_params, __xlog_data),
                    proxies=self.proxies
                ).content.hex()
            )
        )

    def __xlog_coldstart(self, num: int = 1) -> dict:
        if num == 1:
            __xlog_data = self._base_payload(
                extra="cold_start",
                slb=base64.b64encode(
                    "library:EpdgManager\nlibrary:SemAudioThumbnail\nlibrary:android.ext.shared\nlibrary:android.hidl.base-V1.0-java\nlibrary:android.hidl.manager-V1.0-java\nlibrary:android.net.ipsec.ike\nlibrary:android.test.base\nlibrary:android.test.mock\nlibrary:android.test.runner\nlibrary:com.android.future.usb.accessory\nlibrary:com.android.location.provider\nlibrary:com.android.media.remotedisplay\nlibrary:com.android.mediadrm.signer\nlibrary:com.google.android.gms\nlibrary:com.publicnfc\nlibrary:com.samsung.android.ibs.framework-v1\nlibrary:com.samsung.android.knox.analytics.sdk\nlibrary:com.samsung.android.knox.knoxsdk\nlibrary:com.samsung.android.nfc.rfcontrol\nlibrary:com.samsung.android.nfc.t4t\nlibrary:com.samsung.android.psitrackersdk.framework-v1\nlibrary:com.samsung.android.semtelephonesdk.framework-v1\nlibrary:com.samsung.android.spensdk.framework-v1\nlibrary:com.samsung.bbc\nlibrary:com.samsung.device.lite\nlibrary:com.sec.android.sdhmssdk.framework-v1\nlibrary:com.sec.esecomm\nlibrary:com.sec.smartcard.auth\nlibrary:imsmanager\nlibrary:javax.obex\nlibrary:org.apache.http.legacy\nlibrary:org.simalliance.openmobileapi\nlibrary:rcsopenapi\nlibrary:saiv\nlibrary:samsungkeystoreutils\nlibrary:scamera_sdk_util\nlibrary:sec_platform_library\nlibrary:secimaging\nlibrary:semextendedformat\nlibrary:semmediatranscoder\nlibrary:semsdrvideoconverter\nlibrary:sfeffect\nlibrary:stayrotation\nlibrary:vsimmanager\n".encode()).decode(),
                hdf=base64.b64encode(
                    "feature:reqGlEsVersion=0x30002\nfeature:android.hardware.audio.low_latency\nfeature:android.hardware.audio.output\nfeature:android.hardware.biometrics.face\nfeature:android.hardware.bluetooth\nfeature:android.hardware.bluetooth_le\nfeature:android.hardware.camera\nfeature:android.hardware.camera.any\nfeature:android.hardware.camera.autofocus\nfeature:android.hardware.camera.flash\nfeature:android.hardware.camera.front\nfeature:android.hardware.faketouch\nfeature:android.hardware.fingerprint\nfeature:android.hardware.location\nfeature:android.hardware.location.gps\nfeature:android.hardware.location.network\nfeature:android.hardware.microphone\nfeature:android.hardware.nfc\nfeature:android.hardware.nfc.any\nfeature:android.hardware.nfc.hce\nfeature:android.hardware.nfc.hcef\nfeature:android.hardware.nfc.uicc\nfeature:android.hardware.opengles.aep\nfeature:android.hardware.ram.normal\nfeature:android.hardware.screen.landscape\nfeature:android.hardware.screen.portrait\nfeature:android.hardware.se.omapi.uicc\nfeature:android.hardware.sensor.accelerometer\nfeature:android.hardware.sensor.proximity\nfeature:android.hardware.sensor.stepcounter\nfeature:android.hardware.sensor.stepdetector\nfeature:android.hardware.telephony\nfeature:android.hardware.telephony.gsm\nfeature:android.hardware.telephony.ims\nfeature:android.hardware.touchscreen\nfeature:android.hardware.touchscreen.multitouch\nfeature:android.hardware.touchscreen.multitouch.distinct\nfeature:android.hardware.touchscreen.multitouch.jazzhand\nfeature:android.hardware.usb.accessory\nfeature:android.hardware.usb.host\nfeature:android.hardware.vulkan.compute\nfeature:android.hardware.vulkan.level=1\nfeature:android.hardware.vulkan.version=4198400\nfeature:android.hardware.wifi\nfeature:android.hardware.wifi.direct\nfeature:android.hardware.wifi.passpoint\nfeature:android.software.activities_on_secondary_displays\nfeature:android.software.app_enumeration\nfeature:android.software.app_widgets\nfeature:android.software.autofill\nfeature:android.software.backup\nfeature:android.software.cant_save_state\nfeature:android.software.companion_device_setup\nfeature:android.software.connectionservice\nfeature:android.software.controls\nfeature:android.software.cts\nfeature:android.software.device_admin\nfeature:android.software.file_based_encryption\nfeature:android.software.freeform_window_management\nfeature:android.software.home_screen\nfeature:android.software.incremental_delivery\nfeature:android.software.input_methods\nfeature:android.software.ipsec_tunnels\nfeature:android.software.live_wallpaper\nfeature:android.software.managed_users\nfeature:android.software.midi\nfeature:android.software.picture_in_picture\nfeature:android.software.print\nfeature:android.software.secure_lock_screen\nfeature:android.software.securely_removes_users\nfeature:android.software.sip\nfeature:android.software.sip.voip\nfeature:android.software.verified_boot\nfeature:android.software.voice_recognizers\nfeature:android.software.vulkan.deqp.level=132383489\nfeature:android.software.webview\nfeature:com.google.android.feature.ACCESSIBILITY_PRELOAD\nfeature:com.google.android.feature.RU\nfeature:com.google.android.feature.TURBO_PRELOAD\nfeature:com.nxp.mifare\nfeature:com.samsung.android.api.version.2402\nfeature:com.samsung.android.api.version.2403\nfeature:com.samsung.android.api.version.2501\nfeature:com.samsung.android.api.version.2502\nfeature:com.samsung.android.api.version.2601\nfeature:com.samsung.android.api.version.2701\nfeature:com.samsung.android.api.version.2801\nfeature:com.samsung.android.api.version.2802\nfeature:com.samsung.android.api.version.2803\nfeature:com.samsung.android.api.version.2901\nfeature:com.samsung.android.api.version.2902\nfeature:com.samsung.android.api.version.2903\nfeature:com.samsung.android.api.version.3001\nfeature:com.samsung.android.bio.face\nfeature:com.samsung.android.knox.knoxsdk\nfeature:com.samsung.android.knox.knoxsdk.api.level.33\nfeature:com.samsung.android.sdk.camera.processor\nfeature:com.samsung.android.sdk.camera.processor.effect\nfeature:com.samsung.feature.SAMSUNG_EXPERIENCE\nfeature:com.samsung.feature.audio_listenback\nfeature:com.samsung.feature.clockpack_v08\nfeature:com.samsung.feature.device_category_phone\nfeature:com.samsung.feature.galaxyfinder_v7\nfeature:com.samsung.feature.samsung_experience_mobile_lite\nfeature:com.sec.android.secimaging\nfeature:com.sec.android.smartface.smart_stay\nfeature:com.sec.feature.cocktailpanel\nfeature:com.sec.feature.fingerprint_manager_service\nfeature:com.sec.feature.motionrecognition_service\nfeature:com.sec.feature.nsflp=530\nfeature:com.sec.feature.overlaymagnifier\nfeature:com.sec.feature.saccessorymanager\nfeature:com.sec.feature.sensorhub=41\nfeature:com.sec.feature.usb_authentication\n".encode()).decode()
            )
        if num == 2:
            __xlog_data = self._base_payload(
                extra="cold_start",
                acg_m=-127,
                rebuild=0,
                sg_s=1,
                sign=str(APP["sig_hash"]).upper()
            )

        __xlog_params = self.__get_params()

        return json.loads(
            XLEncrypt().decrypt(
                requests.post(
                    url=(
                            "https://xlog-va.byteoversea.com/v2/r/?" + __xlog_params
                    ),
                    data=bytes.fromhex(__xlog_data),
                    headers=self.__get_headers(__xlog_params, __xlog_data),
                    proxies=self.proxies
                ).content.hex()
            )
        )

    def validate_device(self) -> bool:
        while True:
            try:

                # if self.__get_xlog()['status'] == 0:
                #     print(Utils.sprint("*", 1, f"xlog {Col.blue}get{Col.reset} success"))
                #     pass

                if self.__xlog_install()['result'] == "success":
                    # print(Utils.sprint("*", 2, f'xlog post {Col.blue}install{Col.reset} success'))
                    pass

                # if self.__xlog_coldstart(1)['result'] == "success":
                #     # print(Utils.sprint("*", 3, f'xlog post 01 {Col.blue}"cold_start"{Col.reset} success'))
                #     pass

                # if self.__xlog_coldstart(2)['result'] == "success":
                #     # print(Utils.sprint("*", 4, f'xlog post 02 {Col.blue}"cold_start"{Col.reset} success'))
                #     pass

                url = f"https://applog.musical.ly/service/2/app_alert_check/?iid={self.__device['install_id']}&device_id={self.__device['device_id']}&version_code={APP['version_code']}"
                headers = {
                    "accept-encoding": "gzip",
                    "x-ss-req-ticket": str(int(time.time())) + "000",
                    "sdk-version": "1",
                    "user-agent": "okhttp/3.10.0.1",
                }

                response = requests.get(url, headers=headers, data={}, proxies=self.proxies)

                if response.json()["data"]["is_activated"] == 1:
                    # print(Utils.sprint("*", 5, f'Device {Col.blue}activated{Col.reset} !! | Execution time: {Col.blue}{round(time.time() - START, 1)}s'))
                    return self.__device
            except Exception as e:
                # print(e, "akm")
                self.__device = Applog(proxy=self.proxy).register_device()
                continue