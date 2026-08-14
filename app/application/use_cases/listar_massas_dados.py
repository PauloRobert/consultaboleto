from __future__ import annotations

from enum import StrEnum

from app.domain.entities.cliente_faturas import ClienteFaturas
from app.domain.repositories.cliente_repository import ClienteRepository


class StatusFatura(StrEnum):
    PENDENTE = "PENDENTE"
    PAGA = "PAGA"
    VENCIDA = "VENCIDA"
    CANCELADA = "CANCELADA"


class ListarMassasDados:
    def __init__(self, repository: ClienteRepository) -> None:
        self._repository = repository

    def execute(
        self, status: StatusFatura | None = None, quantidade_boletos: int | None = None
    ) -> tuple[ClienteFaturas, ...]:
        records = self._repository.listar_clientes_com_faturas()
        if status is not None:
            records = tuple(
                record for record in records if any(invoice.status == status.value for invoice in record.faturas)
            )
        if quantidade_boletos is not None:
            records = tuple(record for record in records if record.quantidade_boletos == quantidade_boletos)
        return records
