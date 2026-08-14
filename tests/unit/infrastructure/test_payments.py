from app.application.use_cases.consultar_fatura import ConsultarFatura
from app.core.config import Settings
from app.infrastructure.boleto.boleto_generator import BoletoGeneratorService, modulo10
from app.infrastructure.pix.pix_generator import PixGeneratorService, crc16_ccitt
from app.infrastructure.repositories.cliente_txt_repository import ClienteTxtRepository


def invoice():
    return ConsultarFatura(ClienteTxtRepository("dados/clientes.txt")).execute("12345678909")


def test_boleto_tem_digitos_e_campos_consistentes() -> None:
    boleto = BoletoGeneratorService(Settings()).gerar(invoice())
    assert len(boleto.codigo_barras) == 44
    assert len(boleto.linha_digitavel) == 47
    assert modulo10(boleto.linha_digitavel[:9]) == int(boleto.linha_digitavel[9])
    assert modulo10(boleto.linha_digitavel[10:20]) == int(boleto.linha_digitavel[20])
    assert modulo10(boleto.linha_digitavel[21:31]) == int(boleto.linha_digitavel[31])
    assert boleto.codigo_barras[5:19] == boleto.linha_digitavel[33:47]


def test_boleto_e_deterministico() -> None:
    service = BoletoGeneratorService(Settings())
    assert service.gerar(invoice()).nosso_numero == service.gerar(invoice()).nosso_numero


def test_pix_tem_crc_valido_e_campos_emv() -> None:
    payload = PixGeneratorService(Settings()).gerar(invoice())
    assert payload.startswith("000201")
    assert "br.gov. bcb.pix" not in payload
    assert payload[-4:] == crc16_ccitt(payload[:-4])
