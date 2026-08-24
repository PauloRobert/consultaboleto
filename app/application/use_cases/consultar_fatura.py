from __future__ import annotations

from app.application.use_cases.consultar_cliente import ConsultarCliente
from app.domain.entities.fatura import Fatura
from app.domain.exceptions.domain_exceptions import FaturaNaoEncontradaException, SelecaoFaturaObrigatoriaException
from app.domain.repositories.cliente_repository import ClienteRepository


class ConsultarFatura:
    def __init__(self, repository: ClienteRepository) -> None:
        self._repository = repository
        self._consultar_cliente = ConsultarCliente(repository)

    def execute(self, cpf: str, numero_fatura: str | None = None) -> Fatura:
        client = self._consultar_cliente.execute(cpf)
        invoices = self._repository.buscar_faturas_por_cpf(client.cpf.value)
        if not invoices:
            raise FaturaNaoEncontradaException()
        if numero_fatura is not None:
            invoice = next((item for item in invoices if item.numero == numero_fatura), None)
            if invoice is None:
                raise FaturaNaoEncontradaException()
            return invoice
        if len(invoices) > 1:
            raise SelecaoFaturaObrigatoriaException()
        return invoices[0]
