from __future__ import annotations

from typing import Protocol

from app.domain.entities.boleto import Boleto
from app.domain.entities.fatura import Fatura


class BoletoGenerator(Protocol):
    def gerar(self, fatura: Fatura) -> Boleto: ...


class PixGenerator(Protocol):
    def gerar(self, fatura: Fatura) -> str: ...


class PdfGenerator(Protocol):
    def gerar(self, fatura: Fatura, boleto: Boleto, pix_payload: str) -> bytes: ...
