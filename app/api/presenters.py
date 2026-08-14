from __future__ import annotations

from app.domain.entities.fatura import Fatura
from app.schemas.responses import ClienteFaturaData, ClienteResponse, FaturaResponse


def cliente_fatura_response(invoice: Fatura, *, mask_cpf: bool = True) -> ClienteFaturaData:
    cpf = invoice.cliente.cpf.masked() if mask_cpf else invoice.cliente.cpf.value
    return ClienteFaturaData(
        cliente=ClienteResponse(
            nome=invoice.cliente.nome,
            cpf=cpf,
            telefone=invoice.cliente.telefone,
            endereco=invoice.cliente.endereco,
            cidade=invoice.cliente.cidade,
            estado=invoice.cliente.estado,
            cep=invoice.cliente.cep,
        ),
        fatura=FaturaResponse(
            numero=invoice.numero,
            valor=invoice.valor.valor,
            vencimento=invoice.vencimento,
            status=invoice.status,
        ),
    )
