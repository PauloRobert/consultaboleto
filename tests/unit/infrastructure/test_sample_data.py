import json
from datetime import date
from pathlib import Path

from app.domain.value_objects.cpf import CPF


def test_sample_data_is_large_valid_and_varied() -> None:
    data_file = Path(__file__).resolve().parents[3] / "dados" / "clientes.txt"
    records = [json.loads(line) for line in data_file.read_text(encoding="utf-8").splitlines()]

    assert len(records) > 100
    assert len({record["cpf"] for record in records}) == len(records)
    assert all(CPF.is_valid(record["cpf"]) for record in records)
    invoices = [invoice for record in records for invoice in record["faturas"]]
    assert {len(record["faturas"]) for record in records} == {0, 1, 2, 3}
    assert sum(not record["faturas"] for record in records) == 13
    assert {invoice["status"] for invoice in invoices} == {"PENDENTE", "PAGA", "VENCIDA", "CANCELADA"}
    assert len({invoice["valor"] for invoice in invoices}) > 20
    assert len({record["estado"] for record in records}) >= 10

    reference_date = date(2026, 8, 14)
    assert all(
        date.fromisoformat(invoice["vencimento"]) < reference_date
        for invoice in invoices
        if invoice["status"] == "VENCIDA"
    )
    assert all(
        date.fromisoformat(invoice["vencimento"]) > reference_date
        for invoice in invoices
        if invoice["status"] == "PENDENTE"
    )
