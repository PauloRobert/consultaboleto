from __future__ import annotations

from typing import Protocol

from app.domain.entities.cliente import Cliente
from app.domain.entities.cliente_faturas import ClienteFaturas
from app.domain.entities.fatura import Fatura


class ClienteRepository(Protocol):
    def buscar_por_cpf(self, cpf: str) -> Cliente | None:
        """Busca cliente pelo CPF normalizado."""

    def buscar_faturas_por_cpf(self, cpf: str) -> tuple[Fatura, ...]:
        """Busca todas as faturas associadas ao CPF normalizado."""

    def listar_clientes_com_faturas(self) -> tuple[ClienteFaturas, ...]:
        """Lista clientes, inclusive aqueles sem faturas."""
