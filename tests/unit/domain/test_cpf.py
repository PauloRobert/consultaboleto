import pytest

from app.domain.exceptions.domain_exceptions import CpfInvalidoException
from app.domain.value_objects.cpf import CPF


@pytest.mark.parametrize("value", ["12345678909", "123.456.789-09", "52998224725"])
def test_cpf_valido_e_normalizado(value: str) -> None:
    assert CPF(value).value in {"12345678909", "52998224725"}


@pytest.mark.parametrize("value", ["00000000000", "12345678900", "123", "abc12345678", "111.111.111-11"])
def test_cpf_invalido(value: str) -> None:
    with pytest.raises(CpfInvalidoException):
        CPF(value)


def test_cpf_mascarado_nao_expoe_dados() -> None:
    assert CPF("12345678909").masked() == "***.***.***-09"
