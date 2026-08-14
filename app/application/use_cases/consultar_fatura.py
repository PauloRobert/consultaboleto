from __future__ import annotations

from app.application.use_cases.consultar_cliente import ConsultarCliente
from app.domain.entities.fatura import Fatura
from app.domain.exceptions.domain_exceptions import FaturaNaoEncontradaException
from app.domain.repositories.cliente_repository import ClienteRepository


class ConsultarFatura:
    def __init__(self, repository: ClienteRepository) -> None:
        self._repository = repository
        self._consultar_cliente = ConsultarCliente(repository)

    def execute(self, cpf: str) -> Fatura:
        client = self._consultar_cliente.execute(cpf)
        invoice = self._repository.buscar_fatura_por_cpf(client.cpf.value)
        if invoice is None:
            raise FaturaNaoEncontradaException()
        return invoice
