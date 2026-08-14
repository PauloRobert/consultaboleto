from __future__ import annotations

from functools import lru_cache

from app.application.use_cases.consultar_fatura import ConsultarFatura
from app.application.use_cases.gerar_fatura_pdf import GerarFaturaPdf
from app.application.use_cases.obter_pagamentos import ObterBoleto, ObterPix
from app.core.config import get_settings
from app.infrastructure.boleto.boleto_generator import BoletoGeneratorService
from app.infrastructure.pdf.fatura_pdf_generator import FaturaPdfGenerator
from app.infrastructure.pix.pix_generator import PixGeneratorService
from app.infrastructure.repositories.cliente_txt_repository import ClienteTxtRepository


@lru_cache(maxsize=1)
def get_repository() -> ClienteTxtRepository:
    settings = get_settings()
    return ClienteTxtRepository(settings.data_file, settings.cache_ttl_seconds)


def get_consultar_fatura() -> ConsultarFatura:
    return ConsultarFatura(get_repository())


def get_obter_boleto() -> ObterBoleto:
    settings = get_settings()
    return ObterBoleto(get_consultar_fatura(), BoletoGeneratorService(settings))


def get_obter_pix() -> ObterPix:
    settings = get_settings()
    return ObterPix(get_consultar_fatura(), PixGeneratorService(settings))


def get_gerar_pdf() -> GerarFaturaPdf:
    settings = get_settings()
    return GerarFaturaPdf(
        get_consultar_fatura(),
        BoletoGeneratorService(settings),
        PixGeneratorService(settings),
        FaturaPdfGenerator(),
    )
