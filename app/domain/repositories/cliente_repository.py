from __future__ import annotations

from typing import Protocol

from app.domain.entities.cliente import Cliente
from app.domain.entities.fatura import Fatura


class ClienteRepository(Protocol):
    def buscar_por_cpf(self, cpf: str) -> Cliente | None:
        """Busca cliente pelo CPF normalizado."""

    def buscar_fatura_por_cpf(self, cpf: str) -> Fatura | None:
        """Busca a fatura associada ao CPF normalizado."""
