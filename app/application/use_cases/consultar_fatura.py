from __future__ import annotations

from datetime import date

from app.application.use_cases.consultar_cliente import ConsultarCliente
from app.domain.entities.fatura import Fatura
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.value_objects.dinheiro import Dinheiro


class ConsultarFatura:
    def __init__(self, repository: ClienteRepository) -> None:
        self._consultar_cliente = ConsultarCliente(repository)

    def execute(self, cpf: str) -> Fatura:
        cliente = self._consultar_cliente.execute(cpf)
        # A fonte inicial representa uma fatura vigente por cliente.
        return Fatura(
            cliente=cliente,
            numero=f"FAT-{cliente.cpf.value[-8:]}",
            valor=Dinheiro("129.90"),
            vencimento=date(2026, 9, 10),
            status="PENDENTE",
            data_emissao=date(2026, 8, 1),
        )
