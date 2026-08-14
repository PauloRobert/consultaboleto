from __future__ import annotations

import hashlib
from datetime import date

from app.core.config import Settings
from app.core.constants import (
    BARCODE_LENGTH,
    CAMPO_LIVRE_LENGTH,
    CURRENCY_CODE_REAL,
    FATOR_VENCIMENTO_BASE_DATE,
    FATOR_VENCIMENTO_BASE_VALUE,
    FATOR_VENCIMENTO_MAX,
    LINHA_DIGITAVEL_LENGTH,
)
from app.domain.entities.boleto import Boleto
from app.domain.entities.fatura import Fatura


def modulo10(value: str) -> int:
    total = 0
    multiplier = 2
    for digit in reversed(value):
        product = int(digit) * multiplier
        total += product // 10 + product % 10
        multiplier = 1 if multiplier == 2 else 2
    return (10 - total % 10) % 10


def modulo11_barcode(value: str) -> int:
    total = 0
    multiplier = 2
    for digit in reversed(value):
        total += int(digit) * multiplier
        multiplier = multiplier + 1 if multiplier < 9 else 2
    remainder = total % 11
    return 1 if remainder in (0, 10, 11) else 11 - remainder


def fator_vencimento(due_date: date) -> str:
    factor = FATOR_VENCIMENTO_BASE_VALUE + (due_date - FATOR_VENCIMENTO_BASE_DATE).days
    if not 0 <= factor <= FATOR_VENCIMENTO_MAX:
        raise ValueError("Data de vencimento fora do padrão FEBRABAN adotado.")
    return f"{factor:04d}"


class BoletoGeneratorService:
    """Gera boleto bancário de cobrança FEBRABAN em modo demonstrativo.

    O código de barras segue o layout livre de 25 posições (banco, moeda,
    fator, valor e campo livre). Não representa liquidação em banco real.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def gerar(self, fatura: Fatura) -> Boleto:
        identifiers = hashlib.sha256(f"{fatura.cliente.cpf.value}:{fatura.numero}".encode("utf-8")).hexdigest()[:17]
        nosso_numero = str(int(identifiers, 16) % 10**17).zfill(17)
        numero_documento = fatura.numero[-12:].zfill(12)
        free_field = (
            self._settings.agencia.zfill(4)[-4:]
            + self._settings.conta.zfill(6)[-6:]
            + self._settings.carteira.zfill(2)[-2:]
            + nosso_numero[-13:]
        )[:CAMPO_LIVRE_LENGTH]
        value = f"{fatura.valor.centavos:010d}"
        without_dv = (
            self._settings.banco_codigo.zfill(3)
            + CURRENCY_CODE_REAL
            + fator_vencimento(fatura.vencimento)
            + value
            + free_field
        )
        general_dv = str(modulo11_barcode(without_dv[:4] + without_dv[5:]))
        barcode = without_dv[:4] + general_dv + without_dv[4:]
        if len(barcode) != BARCODE_LENGTH:
            raise ValueError("Código de barras com comprimento inválido.")
        field_one = barcode[:4] + barcode[19:24]
        field_two = barcode[24:34]
        field_three = barcode[34:44]
        linha = (
            field_one
            + str(modulo10(field_one))
            + field_two
            + str(modulo10(field_two))
            + field_three
            + str(modulo10(field_three))
            + barcode[4]
            + barcode[5:19]
        )
        if len(linha) != LINHA_DIGITAVEL_LENGTH:
            raise ValueError("Linha digitável com comprimento inválido.")
        return Boleto(
            beneficiario=self._settings.beneficiario_nome,
            pagador=fatura.cliente.nome,
            cpf=fatura.cliente.cpf.value,
            valor=fatura.valor.valor,
            vencimento=fatura.vencimento,
            data_emissao=fatura.data_emissao,
            nosso_numero=nosso_numero,
            numero_documento=numero_documento,
            carteira=self._settings.carteira,
            banco_codigo=self._settings.banco_codigo,
            banco_nome=self._settings.banco_nome,
            codigo_barras=barcode,
            linha_digitavel=linha,
            instrucoes=("Não receber após o vencimento.", "Boleto demonstrativo sem valor de liquidação bancária."),
        )
