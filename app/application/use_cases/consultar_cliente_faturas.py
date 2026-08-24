from __future__ import annotations

from app.application.use_cases.consultar_cliente import ConsultarCliente
from app.domain.entities.cliente_faturas import ClienteFaturas
from app.domain.repositories.cliente_repository import ClienteRepository


class ConsultarClienteFaturas:
    def __init__(self, repository: ClienteRepository) -> None:
        self._repository = repository
        self._consultar_cliente = ConsultarCliente(repository)

    def execute(self, cpf: str) -> ClienteFaturas:
        client = self._consultar_cliente.execute(cpf)
        return ClienteFaturas(client, self._repository.buscar_faturas_por_cpf(client.cpf.value))
