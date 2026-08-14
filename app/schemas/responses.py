from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ClienteResponse(BaseModel):
    nome: str
    cpf: str
    telefone: str
    endereco: str
    cidade: str
    estado: str
    cep: str


class FaturaResponse(BaseModel):
    numero: str
    valor: Decimal
    vencimento: date
    status: str


class ClienteFaturaData(BaseModel):
    cliente: ClienteResponse
    fatura: FaturaResponse


class BoletoData(BaseModel):
    linha_digitavel: str
    codigo_barras: str
    nosso_numero: str
    vencimento: date
    valor: Decimal


class PixData(BaseModel):
    pix_copia_e_cola: str


class ErrorData(BaseModel):
    code: str
    message: str
    request_id: str | None = None


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorData


class HealthResponse(BaseModel):
    status: str
    version: str
