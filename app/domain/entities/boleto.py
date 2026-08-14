from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Boleto:
    beneficiario: str
    pagador: str
    cpf: str
    valor: Decimal
    vencimento: date
    data_emissao: date
    nosso_numero: str
    numero_documento: str
    carteira: str
    banco_codigo: str
    banco_nome: str
    codigo_barras: str
    linha_digitavel: str
    instrucoes: tuple[str, ...]
