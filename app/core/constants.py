"""Constantes de domínio e infraestrutura.

Centraliza "números mágicos" para evitar duplicação e facilitar manutenção.
Nenhum valor sensível/segredo deve residir aqui — segredos vêm de configuração
(variáveis de ambiente), ver :mod:`app.core.config`.
"""

from __future__ import annotations

from datetime import date

# --- CPF -----------------------------------------------------------------
CPF_LENGTH: int = 11
CPF_MAX_INPUT_LENGTH: int = 14  # "123.456.789-09"

# --- Boleto (padrão FEBRABAN) -------------------------------------------
BARCODE_LENGTH: int = 44
LINHA_DIGITAVEL_LENGTH: int = 47
CAMPO_LIVRE_LENGTH: int = 25
CURRENCY_CODE_REAL: str = "9"

# Fator de vencimento: base do ciclo vigente definido pela FEBRABAN após o
# "reset" de 22/02/2025 (fator 1000). Válido para vencimentos >= esta data.
FATOR_VENCIMENTO_BASE_DATE: date = date(2025, 2, 22)
FATOR_VENCIMENTO_BASE_VALUE: int = 1000
FATOR_VENCIMENTO_MAX: int = 9999

VALOR_CENTAVOS_LENGTH: int = 10
FATOR_VENCIMENTO_LENGTH: int = 4

# --- Módulo 10 / Módulo 11 ----------------------------------------------
MOD10_MULTIPLIERS = (2, 1)
MOD11_MIN_MULTIPLIER: int = 2
MOD11_MAX_MULTIPLIER: int = 9

# --- PIX / BR Code (EMV) -------------------------------------------------
PIX_PAYLOAD_FORMAT_INDICATOR: str = "01"
PIX_GUI_BR: str = "br.gov.bcb.pix"
PIX_MERCHANT_CATEGORY_CODE: str = "0000"
PIX_TRANSACTION_CURRENCY_BRL: str = "986"  # ISO 4217
PIX_COUNTRY_CODE: str = "BR"
CRC16_POLYNOMIAL: int = 0x1021
CRC16_INITIAL_VALUE: int = 0xFFFF
PIX_MERCHANT_NAME_MAX: int = 25
PIX_MERCHANT_CITY_MAX: int = 15
PIX_TXID_MAX: int = 25

# --- Limites de entrada / segurança -------------------------------------
MAX_CPF_PATH_LENGTH: int = 20  # limite defensivo no path param
