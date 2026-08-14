from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.logging import request_id
from app.domain.exceptions.domain_exceptions import (
    ClienteNaoEncontradoException,
    CpfInvalidoException,
    FaturaNaoEncontradaException,
    SelecaoFaturaObrigatoriaException,
)
from app.schemas.responses import ErrorData, ErrorResponse


def error_response(request: Request, status_code: int, code: str, message: str) -> JSONResponse:
    body = ErrorResponse(error=ErrorData(code=code, message=message, request_id=request_id(request))).model_dump(
        mode="json"
    )
    return JSONResponse(status_code=status_code, content=body)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(CpfInvalidoException)
    async def invalid_cpf(request: Request, _exception: CpfInvalidoException) -> JSONResponse:
        return error_response(request, 400, "INVALID_CPF", "O CPF informado é inválido.")

    @app.exception_handler(ClienteNaoEncontradoException)
    async def missing_client(request: Request, _exception: ClienteNaoEncontradoException) -> JSONResponse:
        return error_response(request, 404, "CLIENT_NOT_FOUND", "Não foi encontrado cliente para o CPF informado.")

    @app.exception_handler(FaturaNaoEncontradaException)
    async def missing_invoice(request: Request, _exception: FaturaNaoEncontradaException) -> JSONResponse:
        return error_response(request, 404, "INVOICE_NOT_FOUND", "Não foi encontrada fatura para o cliente informado.")

    @app.exception_handler(SelecaoFaturaObrigatoriaException)
    async def invoice_selection_required(
        request: Request, _exception: SelecaoFaturaObrigatoriaException
    ) -> JSONResponse:
        return error_response(
            request,
            409,
            "INVOICE_SELECTION_REQUIRED",
            "O cliente possui mais de uma fatura. Informe o número da fatura desejada.",
        )

    @app.exception_handler(Exception)
    async def internal_error(request: Request, _exception: Exception) -> JSONResponse:
        return error_response(request, 500, "INTERNAL_ERROR", "Ocorreu um erro interno ao processar a solicitação.")
