from __future__ import annotations

from app.domain.entities.cliente import Cliente
from app.domain.exceptions.domain_exceptions import ClienteNaoEncontradoException
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.value_objects.cpf import CPF


class ConsultarCliente:
    def __init__(self, repository: ClienteRepository) -> None:
        self._repository = repository

    def execute(self, cpf: str) -> Cliente:
        normalized = CPF(cpf)
        client = self._repository.buscar_por_cpf(normalized.value)
        if client is None:
            raise ClienteNaoEncontradoException()
        return client
