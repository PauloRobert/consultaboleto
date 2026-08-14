from __future__ import annotations

from fastapi import APIRouter, Depends, Path
from fastapi.responses import Response

from app.api.dependencies import get_gerar_pdf, get_obter_boleto, get_obter_pix
from app.application.use_cases.gerar_fatura_pdf import GerarFaturaPdf
from app.application.use_cases.obter_pagamentos import ObterBoleto, ObterPix
from app.schemas.responses import BoletoData, PixData, SuccessResponse

router = APIRouter(prefix="/clientes", tags=["Pagamentos"])


@router.get(
    "/{cpf}/boleto",
    response_model=SuccessResponse[BoletoData],
    summary="Obtém o boleto",
    description="Retorna a linha digitável e os dados derivados do boleto demonstrativo.",
    responses={400: {"description": "CPF inválido"}, 404: {"description": "Cliente não encontrado"}},
)
def boleto(
    cpf: str = Path(..., min_length=1, max_length=20), use_case: ObterBoleto = Depends(get_obter_boleto)
) -> SuccessResponse[BoletoData]:
    item = use_case.execute(cpf)
    return SuccessResponse(
        data=BoletoData(
            linha_digitavel=item.linha_digitavel,
            codigo_barras=item.codigo_barras,
            nosso_numero=item.nosso_numero,
            vencimento=item.vencimento,
            valor=item.valor,
        )
    )


@router.get(
    "/{cpf}/pix",
    response_model=SuccessResponse[PixData],
    summary="Obtém o PIX Copia e Cola",
    description="Retorna payload BR Code EMV com CRC16 válido.",
    responses={400: {"description": "CPF inválido"}, 404: {"description": "Cliente não encontrado"}},
)
def pix(
    cpf: str = Path(..., min_length=1, max_length=20), use_case: ObterPix = Depends(get_obter_pix)
) -> SuccessResponse[PixData]:
    return SuccessResponse(data=PixData(pix_copia_e_cola=use_case.execute(cpf)))


@router.get(
    "/{cpf}/fatura/pdf",
    response_class=Response,
    summary="Gera PDF da fatura",
    description="Gera dinamicamente a fatura com boleto e QR Code PIX.",
    responses={
        200: {"content": {"application/pdf": {}}},
        400: {"description": "CPF inválido"},
        404: {"description": "Cliente não encontrado"},
    },
)
def pdf(
    cpf: str = Path(..., min_length=1, max_length=20), use_case: GerarFaturaPdf = Depends(get_gerar_pdf)
) -> Response:
    content = use_case.execute(cpf)
    return Response(
        content=content, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=fatura.pdf"}
    )
