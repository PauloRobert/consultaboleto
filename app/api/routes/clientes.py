from __future__ import annotations

from fastapi import APIRouter, Depends, Path

from app.api.dependencies import get_consultar_fatura
from app.application.use_cases.consultar_fatura import ConsultarFatura
from app.schemas.responses import ClienteFaturaData, ClienteResponse, FaturaResponse, SuccessResponse

router = APIRouter(prefix="/clientes", tags=["Clientes e faturas"])


@router.get("/{cpf}", response_model=SuccessResponse[ClienteFaturaData], summary="Consulta cliente e fatura", description="Valida o CPF e retorna os dados cadastrais e a fatura vigente associada.", responses={400: {"description": "CPF inválido"}, 404: {"description": "Cliente não encontrado"}})
def consultar(cpf: str = Path(..., min_length=1, max_length=20, examples=["123.456.789-09"]), use_case: ConsultarFatura = Depends(get_consultar_fatura)) -> SuccessResponse[ClienteFaturaData]:
    invoice = use_case.execute(cpf)
    return SuccessResponse(data=ClienteFaturaData(cliente=ClienteResponse(nome=invoice.cliente.nome, cpf=invoice.cliente.cpf.masked(), telefone=invoice.cliente.telefone, endereco=invoice.cliente.endereco, cidade=invoice.cliente.cidade, estado=invoice.cliente.estado, cep=invoice.cliente.cep), fatura=FaturaResponse(numero=invoice.numero, valor=invoice.valor.valor, vencimento=invoice.vencimento, status=invoice.status)))
