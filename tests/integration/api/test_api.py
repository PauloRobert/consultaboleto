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


def test_lista_todas_as_massas_de_dados() -> None:
    response = client.get("/api/v1/massadados")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] == 122
    assert data["status_filtro"] is None
    assert len(data["registros"]) == 122
    assert data["registros"][0]["cliente"]["cpf"] == "12345678909"


def test_filtra_massas_por_status() -> None:
    expected_totals = {"PENDENTE": 31, "PAGA": 31, "VENCIDA": 30, "CANCELADA": 30}

    for status, expected_total in expected_totals.items():
        response = client.get("/api/v1/massadados", params={"status": status})
        data = response.json()["data"]
        assert response.status_code == 200
        assert data["total"] == expected_total
        assert data["status_filtro"] == status
        assert all(record["fatura"]["status"] == status for record in data["registros"])


def test_rejeita_status_invalido_na_massa_de_dados() -> None:
    response = client.get("/api/v1/massadados", params={"status": "INVALIDO"})

    assert response.status_code == 422


def test_openapi_expoe_nome_e_filtro_de_status() -> None:
    schema = client.get("/openapi.json").json()

    assert schema["info"]["title"] == "Consulta Boleto"
    operation = schema["paths"]["/api/v1/massadados"]["get"]
    assert operation["summary"] == "Lista as massas de dados"
    assert operation["parameters"][0]["name"] == "status"
    assert schema["components"]["schemas"]["StatusFatura"]["enum"] == [
        "PENDENTE",
        "PAGA",
        "VENCIDA",
        "CANCELADA",
    ]
