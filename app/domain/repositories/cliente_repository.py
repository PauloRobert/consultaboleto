from __future__ import annotations

from typing import Protocol

from app.domain.entities.cliente import Cliente


class ClienteRepository(Protocol):
    def buscar_por_cpf(self, cpf: str) -> Cliente | None:
        """Busca cliente pelo CPF normalizado."""
