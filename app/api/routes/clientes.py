from __future__ import annotations

from fastapi import APIRouter, Depends, Path

from app.api.dependencies import get_consultar_fatura
from app.api.presenters import cliente_fatura_response
from app.application.use_cases.consultar_fatura import ConsultarFatura
from app.schemas.responses import ClienteFaturaData, SuccessResponse

router = APIRouter(prefix="/clientes", tags=["Clientes e faturas"])


@router.get(
    "/{cpf}",
    response_model=SuccessResponse[ClienteFaturaData],
    summary="Consulta cliente e fatura",
    description="Valida o CPF e retorna os dados cadastrais e a fatura vigente associada.",
    responses={400: {"description": "CPF inválido"}, 404: {"description": "Cliente não encontrado"}},
)
def consultar(
    cpf: str = Path(..., min_length=1, max_length=20, examples=["123.456.789-09"]),
    use_case: ConsultarFatura = Depends(get_consultar_fatura),
) -> SuccessResponse[ClienteFaturaData]:
    invoice = use_case.execute(cpf)
    return SuccessResponse(data=cliente_fatura_response(invoice))
