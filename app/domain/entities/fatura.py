from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from app.domain.entities.cliente import Cliente
from app.domain.value_objects.dinheiro import Dinheiro


@dataclass(frozen=True, slots=True)
class Fatura:
    cliente: Cliente
    numero: str
    valor: Dinheiro
    vencimento: date
    status: str = "PENDENTE"
    data_emissao: date = field(default_factory=date.today)

    @property
    def valor_decimal(self) -> Decimal:
        return self.valor.valor
