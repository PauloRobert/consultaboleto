from __future__ import annotations

from fastapi import APIRouter, Depends, Path

from app.api.dependencies import get_consultar_cliente_faturas
from app.api.presenters import cliente_boletos_response
from app.application.use_cases.consultar_cliente_faturas import ConsultarClienteFaturas
from app.schemas.responses import ClienteBoletosData, SuccessResponse

router = APIRouter(prefix="/clientes", tags=["Clientes e faturas"])


@router.get(
    "/{cpf}",
    response_model=SuccessResponse[ClienteBoletosData],
    summary="Consulta cliente e boletos",
    description=(
        "Valida o CPF e retorna o cadastro e todos os boletos associados. "
        "Clientes sem dívidas retornam quantidade_boletos igual a zero e uma lista vazia."
    ),
    responses={400: {"description": "CPF inválido"}, 404: {"description": "Cliente não encontrado"}},
)
def consultar(
    cpf: str = Path(..., min_length=1, max_length=20, examples=["123.456.789-09"]),
    use_case: ConsultarClienteFaturas = Depends(get_consultar_cliente_faturas),
) -> SuccessResponse[ClienteBoletosData]:
    record = use_case.execute(cpf)
    return SuccessResponse(data=cliente_boletos_response(record))
