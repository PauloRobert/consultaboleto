from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_listar_massas_dados
from app.api.presenters import cliente_boletos_response
from app.application.use_cases.listar_massas_dados import ListarMassasDados, StatusFatura
from app.schemas.responses import MassaDadosResponse, SuccessResponse

router = APIRouter(prefix="/massadados", tags=["Massa de dados"])


@router.get(
    "",
    response_model=SuccessResponse[MassaDadosResponse],
    summary="Lista as massas de dados",
    description=(
        "Retorna todos os clientes e boletos sintéticos disponíveis para testes. "
        "Os filtros opcionais selecionam clientes por status ou quantidade exata de boletos."
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
    quantidade_boletos: int | None = Query(
        default=None,
        ge=0,
        le=20,
        description="Filtra clientes pela quantidade exata de boletos, incluindo zero.",
        examples=[2],
    ),
    use_case: ListarMassasDados = Depends(get_listar_massas_dados),
) -> SuccessResponse[MassaDadosResponse]:
    clients = use_case.execute(status, quantidade_boletos)
    records = [cliente_boletos_response(record, mask_cpf=False) for record in clients]
    return SuccessResponse(
        data=MassaDadosResponse(
            total=len(records),
            status_filtro=status.value if status else None,
            quantidade_boletos_filtro=quantidade_boletos,
            registros=records,
        )
    )
