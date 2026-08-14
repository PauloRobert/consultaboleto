from __future__ import annotations

import re
from dataclasses import dataclass

from app.core.constants import CPF_LENGTH, CPF_MAX_INPUT_LENGTH
from app.domain.exceptions.domain_exceptions import CpfInvalidoException

_DIGITS = re.compile(r"^\d{11}$")


@dataclass(frozen=True, slots=True)
class CPF:
    value: str

    def __post_init__(self) -> None:
        normalized = self.normalize(self.value)
        if not self.is_valid(normalized):
            raise CpfInvalidoException("O CPF informado é inválido.")
        object.__setattr__(self, "value", normalized)

    @staticmethod
    def normalize(value: str) -> str:
        if not isinstance(value, str) or len(value) > CPF_MAX_INPUT_LENGTH:
            raise CpfInvalidoException("O CPF informado é inválido.")
        normalized = re.sub(r"[.\-\s]", "", value)
        if not _DIGITS.fullmatch(normalized):
            raise CpfInvalidoException("O CPF informado é inválido.")
        return normalized

    @staticmethod
    def is_valid(value: str) -> bool:
        if len(value) != CPF_LENGTH or not value.isdigit() or len(set(value)) == 1:
            return False
        digits = [int(digit) for digit in value]
        first = sum(digit * (10 - index) for index, digit in enumerate(digits[:9]))
        first_check = (first * 10 % 11) % 10
        if first_check != digits[9]:
            return False
        second = sum(digit * (11 - index) for index, digit in enumerate(digits[:10]))
        second_check = (second * 10 % 11) % 10
        return second_check == digits[10]

    def masked(self) -> str:
        return f"***.***.***-{self.value[-2:]}"

    def __str__(self) -> str:
        return self.value
