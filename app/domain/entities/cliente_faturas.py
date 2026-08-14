from __future__ import annotations

from dataclasses import dataclass

from app.domain.entities.cliente import Cliente
from app.domain.entities.fatura import Fatura


@dataclass(frozen=True, slots=True)
class ClienteFaturas:
    cliente: Cliente
    faturas: tuple[Fatura, ...]

    @property
    def quantidade_boletos(self) -> int:
        return len(self.faturas)
