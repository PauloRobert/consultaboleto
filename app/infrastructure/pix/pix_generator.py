from __future__ import annotations

from app.core.config import Settings
from app.core.constants import (
    CRC16_INITIAL_VALUE,
    CRC16_POLYNOMIAL,
    PIX_COUNTRY_CODE,
    PIX_GUI_BR,
    PIX_MERCHANT_CATEGORY_CODE,
    PIX_MERCHANT_CITY_MAX,
    PIX_MERCHANT_NAME_MAX,
    PIX_PAYLOAD_FORMAT_INDICATOR,
    PIX_TRANSACTION_CURRENCY_BRL,
    PIX_TXID_MAX,
)
from app.domain.entities.fatura import Fatura


def crc16_ccitt(payload: str) -> str:
    crc = CRC16_INITIAL_VALUE
    for byte in payload.encode("utf-8"):
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ CRC16_POLYNOMIAL) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return f"{crc:04X}"


def emv_field(tag: str, value: str) -> str:
    return f"{tag}{len(value):02d}{value}"


class PixGeneratorService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def gerar(self, fatura: Fatura) -> str:
        name = self._settings.pix_merchant_name.upper()[:PIX_MERCHANT_NAME_MAX]
        city = self._settings.pix_merchant_city.upper()[:PIX_MERCHANT_CITY_MAX]
        txid = fatura.numero[-PIX_TXID_MAX:]
        merchant_account = emv_field("00", PIX_GUI_BR) + emv_field("01", self._settings.pix_key)
        additional = emv_field("05", txid)
        payload = (
            emv_field("00", PIX_PAYLOAD_FORMAT_INDICATOR)
            + emv_field("01", "12")
            + emv_field("26", merchant_account)
            + emv_field("52", PIX_MERCHANT_CATEGORY_CODE)
            + emv_field("53", PIX_TRANSACTION_CURRENCY_BRL)
            + emv_field("54", f"{fatura.valor.valor:.2f}")
            + emv_field("58", PIX_COUNTRY_CODE)
            + emv_field("59", name)
            + emv_field("60", city)
            + emv_field("62", additional)
        )
        return payload + "6304" + crc16_ccitt(payload + "6304")
