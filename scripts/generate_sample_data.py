from __future__ import annotations

import json
import random
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

TOTAL_GENERATED_RECORDS = 120
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "dados" / "clientes.txt"

FIRST_NAMES = (
    "Ana",
    "Bruno",
    "Carla",
    "Daniel",
    "Eduarda",
    "Felipe",
    "Gabriela",
    "Henrique",
    "Isabela",
    "João",
    "Larissa",
    "Marcos",
    "Natália",
    "Otávio",
    "Patrícia",
    "Rafael",
    "Sabrina",
    "Thiago",
    "Vanessa",
    "William",
)
LAST_NAMES = (
    "Almeida",
    "Barbosa",
    "Cardoso",
    "Dias",
    "Esteves",
    "Ferreira",
    "Gomes",
    "Lima",
    "Martins",
    "Nascimento",
    "Oliveira",
    "Pereira",
    "Rocha",
    "Santos",
    "Silva",
    "Souza",
)
LOCATIONS = (
    ("São Paulo", "SP", "01000"),
    ("Rio de Janeiro", "RJ", "20000"),
    ("Belo Horizonte", "MG", "30000"),
    ("Curitiba", "PR", "80000"),
    ("Porto Alegre", "RS", "90000"),
    ("Salvador", "BA", "40000"),
    ("Recife", "PE", "50000"),
    ("Fortaleza", "CE", "60000"),
    ("Brasília", "DF", "70000"),
    ("Goiânia", "GO", "74000"),
    ("Manaus", "AM", "69000"),
    ("Florianópolis", "SC", "88000"),
)
STATUSES = ("PENDENTE", "PAGA", "VENCIDA", "CANCELADA")


def cpf_from_base(base: int) -> str:
    first_nine = f"{base:09d}"
    digits = [int(digit) for digit in first_nine]
    first = (sum(digit * (10 - index) for index, digit in enumerate(digits)) * 10 % 11) % 10
    digits.append(first)
    second = (sum(digit * (11 - index) for index, digit in enumerate(digits)) * 10 % 11) % 10
    return first_nine + str(first) + str(second)


def generated_record(index: int, randomizer: random.Random) -> dict[str, str]:
    city, state, cep_prefix = LOCATIONS[index % len(LOCATIONS)]
    status = STATUSES[index % len(STATUSES)]
    if status == "PENDENTE":
        issue_date = date(2026, 8, 1) + timedelta(days=index % 14)
    elif status == "VENCIDA":
        issue_date = date(2026, 4, 1) + timedelta(days=index % 75)
    else:
        issue_date = date(2026, 5, 1) + timedelta(days=index % 90)
    due_date = issue_date + timedelta(days=30)
    amount = Decimal("39.90") + Decimal(index % 24) * Decimal("17.35") + Decimal(index % 7)
    return {
        "cpf": cpf_from_base(100000001 + index),
        "nome": f"{FIRST_NAMES[index % len(FIRST_NAMES)]} {LAST_NAMES[(index * 3) % len(LAST_NAMES)]}",
        "telefone": f"{11 + index % 79:02d}9{randomizer.randint(10000000, 99999999)}",
        "endereco": f"Rua {LAST_NAMES[(index * 5) % len(LAST_NAMES)]}, {100 + index * 7}",
        "cidade": city,
        "estado": state,
        "cep": f"{cep_prefix}{index % 1000:03d}",
        "numero_fatura": f"FAT-2026-{index + 3:05d}",
        "valor": f"{amount:.2f}",
        "vencimento": due_date.isoformat(),
        "status": status,
        "data_emissao": issue_date.isoformat(),
    }


def main() -> None:
    randomizer = random.Random(20260814)
    records = [
        {
            "cpf": "12345678909",
            "nome": "João da Silva",
            "telefone": "11999999999",
            "endereco": "Rua Exemplo, 100",
            "cidade": "São Paulo",
            "estado": "SP",
            "cep": "01000000",
            "numero_fatura": "FAT-2026-00001",
            "valor": "129.90",
            "vencimento": "2026-09-10",
            "status": "PENDENTE",
            "data_emissao": "2026-08-01",
        },
        {
            "cpf": "52998224725",
            "nome": "Maria Oliveira",
            "telefone": "11988887777",
            "endereco": "Avenida Central, 250",
            "cidade": "São Paulo",
            "estado": "SP",
            "cep": "01310000",
            "numero_fatura": "FAT-2026-00002",
            "valor": "245.70",
            "vencimento": "2026-07-20",
            "status": "PAGA",
            "data_emissao": "2026-06-20",
        },
    ]
    records.extend(generated_record(index, randomizer) for index in range(TOTAL_GENERATED_RECORDS))
    OUTPUT_PATH.write_text(
        "".join(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n" for record in records),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
