from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


@dataclass(frozen=True, slots=True)
class Dinheiro:
    valor: Decimal

    def __post_init__(self) -> None:
        amount = Decimal(str(self.valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if amount < 0:
            raise ValueError("O valor não pode ser negativo.")
        object.__setattr__(self, "valor", amount)

    @property
    def centavos(self) -> int:
        return int(self.valor * 100)
