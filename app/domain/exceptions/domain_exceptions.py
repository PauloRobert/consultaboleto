from __future__ import annotations


class DomainError(Exception):
    """Base para erros esperados do domínio."""


class CpfInvalidoException(DomainError):
    pass


class ClienteNaoEncontradoException(DomainError):
    pass


class FaturaNaoEncontradaException(DomainError):
    pass


class SelecaoFaturaObrigatoriaException(DomainError):
    pass


class BoletoGenerationException(DomainError):
    pass


class PixGenerationException(DomainError):
    pass


class PdfGenerationException(DomainError):
    pass
