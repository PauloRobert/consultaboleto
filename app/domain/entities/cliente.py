from __future__ import annotations

from dataclasses import dataclass

from app.domain.value_objects.cpf import CPF


@dataclass(frozen=True, slots=True)
class Cliente:
    cpf: CPF
    nome: str
    telefone: str
    endereco: str
    cidade: str
    estado: str
    cep: str
