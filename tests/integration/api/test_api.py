from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_consulta_cliente() -> None:
    response = client.get("/api/v1/clientes/123.456.789-09")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["cliente"]["cpf"] == "***.***.***-09"
    assert body["data"]["fatura"]["valor"] == "129.90"


def test_erros_consistentes() -> None:
    invalid = client.get("/api/v1/clientes/00000000000")
    missing = client.get("/api/v1/clientes/98765432100")
    assert invalid.status_code == 400 and invalid.json()["error"]["code"] == "INVALID_CPF"
    assert missing.status_code == 404 and missing.json()["error"]["code"] == "CLIENT_NOT_FOUND"
    assert "00000000000" not in invalid.text


def test_pagamentos_e_pdf() -> None:
    boleto = client.get("/api/v1/clientes/12345678909/boleto")
    pix = client.get("/api/v1/clientes/12345678909/pix")
    pdf = client.get("/api/v1/clientes/12345678909/fatura/pdf")
    assert len(boleto.json()["data"]["linha_digitavel"]) == 47
    assert len(pix.json()["data"]["pix_copia_e_cola"]) > 100
    assert pdf.headers["content-type"] == "application/pdf"
    assert pdf.content.startswith(b"%PDF")
