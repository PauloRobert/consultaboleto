from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_listar_massas_dados
from app.api.presenters import cliente_fatura_response
from app.application.use_cases.listar_massas_dados import ListarMassasDados, StatusFatura
from app.schemas.responses import MassaDadosResponse, SuccessResponse

router = APIRouter(prefix="/massadados", tags=["Massa de dados"])


@router.get(
    "",
    response_model=SuccessResponse[MassaDadosResponse],
    summary="Lista as massas de dados",
    description=(
        "Retorna todos os clientes e faturas sintéticos disponíveis para testes. "
        "O filtro opcional permite selecionar registros por status da fatura."
    ),
    responses={
        200: {"description": "Massas de dados retornadas com sucesso"},
        422: {"description": "Status informado não é válido"},
    },
)
def listar_massas(
    status: StatusFatura | None = Query(
        default=None,
        description="Filtra pelo status da fatura.",
        examples=[StatusFatura.PENDENTE],
    ),
    use_case: ListarMassasDados = Depends(get_listar_massas_dados),
) -> SuccessResponse[MassaDadosResponse]:
    invoices = use_case.execute(status)
    records = [cliente_fatura_response(invoice, mask_cpf=False) for invoice in invoices]
    return SuccessResponse(
        data=MassaDadosResponse(
            total=len(records),
            status_filtro=status.value if status else None,
            registros=records,
        )
    )
