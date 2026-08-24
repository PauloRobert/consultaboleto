from __future__ import annotations

from app.domain.entities.cliente import Cliente
from app.domain.entities.cliente_faturas import ClienteFaturas
from app.domain.entities.fatura import Fatura
from app.schemas.responses import ClienteBoletosData, ClienteResponse, FaturaResponse


def cliente_response(client: Cliente, *, mask_cpf: bool = True) -> ClienteResponse:
    cpf = client.cpf.masked() if mask_cpf else client.cpf.value
    return ClienteResponse(
        nome=client.nome,
        cpf=cpf,
        telefone=client.telefone,
        endereco=client.endereco,
        cidade=client.cidade,
        estado=client.estado,
        cep=client.cep,
    )


def fatura_response(invoice: Fatura) -> FaturaResponse:
    return FaturaResponse(
        numero=invoice.numero,
        valor=invoice.valor.valor,
        vencimento=invoice.vencimento,
        status=invoice.status,
    )


def cliente_boletos_response(record: ClienteFaturas, *, mask_cpf: bool = True) -> ClienteBoletosData:
    return ClienteBoletosData(
        cliente=cliente_response(record.cliente, mask_cpf=mask_cpf),
        quantidade_boletos=record.quantidade_boletos,
        boletos=[fatura_response(invoice) for invoice in record.faturas],
    )
