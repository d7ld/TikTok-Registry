import binascii
import json

from pystyle import Col
from .ttencrypt import TTEncrypt
from .xlog import XLEncrypt
from .gorgon import Gorgon

class Utils:
    @staticmethod
    def _xor(string):
        encrypted = [hex(ord(c) ^ 5)[2:] for c in string]
        return "".join(encrypted)

    @staticmethod
    def _sig(params: str, body: str = None, cookie: str = None) -> dict:
        gorgon = Gorgon()
        return gorgon.calculate(params, cookie, body)

    @staticmethod
    def _ttencrypt(body: dict) -> str:
        ttencrypt = TTEncrypt()
        data_formated = json.dumps(body).replace(" ", "")
        return ttencrypt.encrypt(data_formated)

    @staticmethod
    def _xlencrypt(body: str) -> str:
        return XLEncrypt().encrypt(body)

    @staticmethod
    def _fch(xlog: str):
        xlog = xlog[0:len(xlog) - 21]
        fch_str = binascii.crc32(xlog.encode("utf-8"))
        fch_str = str(fch_str)

        for i in range(len(fch_str), 10):
            fch_str = '0' + fch_str

        return fch_str

    @staticmethod
    def sprint(x: str, num: int, msg: str) -> None:
        return '    %s{%s%s%s}%s %s %s[%s%s%s]%s' % (
            Col.purple, Col.reset,
            x,
            Col.purple, Col.reset,
            num,
            Col.blue, Col.reset,
            msg,
            Col.blue, Col.reset
        )