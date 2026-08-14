import json

import pytest

from app.infrastructure.repositories.cliente_txt_repository import ClienteTxtRepository


def test_repository_encontra_e_cacheia_clientes(tmp_path) -> None:
    path = tmp_path / "clientes.txt"
    path.write_text(
        json.dumps(
            {
                "cpf": "12345678909",
                "nome": "A",
                "telefone": "1",
                "endereco": "Rua",
                "cidade": "SP",
                "estado": "SP",
                "cep": "01000000",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    repository = ClienteTxtRepository(str(path), cache_ttl_seconds=60)
    assert repository.buscar_por_cpf("12345678909").nome == "A"
    path.write_text("{malformed\n", encoding="utf-8")
    assert repository.buscar_por_cpf("12345678909").nome == "A"
    assert repository.buscar_por_cpf("52998224725") is None


def test_repository_rejeita_arquivo_ausente(tmp_path) -> None:
    with pytest.raises(FileNotFoundError):
        ClienteTxtRepository(str(tmp_path / "missing.txt")).buscar_por_cpf("12345678909")


def test_repository_rejeita_linha_malformada(tmp_path) -> None:
    path = tmp_path / "clientes.txt"
    path.write_text("{malformed\n", encoding="utf-8")
    with pytest.raises(ValueError, match="linha inválida"):
        ClienteTxtRepository(str(path)).buscar_por_cpf("12345678909")
