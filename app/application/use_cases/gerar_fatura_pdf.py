from __future__ import annotations

from app.application.use_cases.consultar_fatura import ConsultarFatura
from app.domain.services.payment_ports import BoletoGenerator, PdfGenerator, PixGenerator


class GerarFaturaPdf:
    def __init__(
        self,
        consultar_fatura: ConsultarFatura,
        boleto_generator: BoletoGenerator,
        pix_generator: PixGenerator,
        pdf_generator: PdfGenerator,
    ) -> None:
        self._consultar_fatura = consultar_fatura
        self._boleto = boleto_generator
        self._pix = pix_generator
        self._pdf = pdf_generator

    def execute(self, cpf: str) -> bytes:
        invoice = self._consultar_fatura.execute(cpf)
        return self._pdf.gerar(invoice, self._boleto.gerar(invoice), self._pix.gerar(invoice))
