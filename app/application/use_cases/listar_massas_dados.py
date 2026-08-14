from __future__ import annotations

from enum import StrEnum

from app.domain.entities.fatura import Fatura
from app.domain.repositories.cliente_repository import ClienteRepository


class StatusFatura(StrEnum):
    PENDENTE = "PENDENTE"
    PAGA = "PAGA"
    VENCIDA = "VENCIDA"
    CANCELADA = "CANCELADA"


class ListarMassasDados:
    def __init__(self, repository: ClienteRepository) -> None:
        self._repository = repository

    def execute(self, status: StatusFatura | None = None) -> tuple[Fatura, ...]:
        invoices = self._repository.listar_faturas()
        if status is None:
            return invoices
        return tuple(invoice for invoice in invoices if invoice.status == status.value)
