from __future__ import annotations

from app.application.use_cases.consultar_fatura import ConsultarFatura
from app.domain.entities.boleto import Boleto
from app.domain.services.payment_ports import BoletoGenerator, PixGenerator


class ObterBoleto:
    def __init__(self, consultar_fatura: ConsultarFatura, generator: BoletoGenerator) -> None:
        self._consultar_fatura = consultar_fatura
        self._generator = generator

    def execute(self, cpf: str) -> Boleto:
        return self._generator.gerar(self._consultar_fatura.execute(cpf))


class ObterPix:
    def __init__(self, consultar_fatura: ConsultarFatura, generator: PixGenerator) -> None:
        self._consultar_fatura = consultar_fatura
        self._generator = generator

    def execute(self, cpf: str) -> str:
        return self._generator.gerar(self._consultar_fatura.execute(cpf))
