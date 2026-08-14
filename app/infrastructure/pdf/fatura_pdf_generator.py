from __future__ import annotations

from io import BytesIO

import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.domain.entities.boleto import Boleto
from app.domain.entities.fatura import Fatura


class FaturaPdfGenerator:
    def gerar(self, fatura: Fatura, boleto: Boleto, pix_payload: str) -> bytes:
        output = BytesIO()
        document = SimpleDocTemplate(output, pagesize=A4, rightMargin=16 * mm, leftMargin=16 * mm)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("TELEFONIA EXEMPLO S.A.", styles["Title"]),
            Paragraph("Fatura de Telefonia", styles["Heading2"]),
            Paragraph(f"Fatura {fatura.numero} | Emissão: {fatura.data_emissao:%d/%m/%Y}", styles["Normal"]),
            Spacer(1, 8 * mm),
        ]
        client = fatura.cliente
        story.append(
            Table(
                [
                    [Paragraph("CLIENTE", styles["Heading3"]), Paragraph("PAGAMENTO", styles["Heading3"])],
                    [
                        f"{client.nome}\nCPF: {client.cpf.masked()}\nTelefone: {client.telefone}\n{client.endereco} - {client.cidade}/{client.estado} - CEP {client.cep}",
                        f"Valor: R$ {fatura.valor.valor:.2f}\nVencimento: {fatura.vencimento:%d/%m/%Y}\nStatus: {fatura.status}",
                    ],
                ],
                colWidths=[90 * mm, 85 * mm],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12304a")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b7c6d1")),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("PADDING", (0, 0), (-1, -1), 7),
                    ]
                ),
            )
        )
        story += [Spacer(1, 8 * mm), Paragraph("DETALHES DA COBRANÇA", styles["Heading3"])]
        story.append(
            Table(
                [
                    ["Descrição", "Valor"],
                    ["Plano de telefonia", "R$ 89,90"],
                    ["Internet", "R$ 49,90"],
                    ["Desconto promocional", "- R$ 9,90"],
                    ["Total", f"R$ {fatura.valor.valor:.2f}"],
                ],
                colWidths=[130 * mm, 45 * mm],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dce8ef")),
                        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                        ("PADDING", (0, 0), (-1, -1), 6),
                    ]
                ),
            )
        )
        story += [
            Spacer(1, 7 * mm),
            Paragraph("INFORMAÇÕES DE PAGAMENTO", styles["Heading3"]),
            Paragraph(f"Linha digitável: {boleto.linha_digitavel}", styles["Normal"]),
        ]
        barcode_buffer = BytesIO()
        Code128(boleto.codigo_barras, writer=ImageWriter()).write(barcode_buffer, {"write_text": False})
        barcode_buffer.seek(0)
        story.append(Image(barcode_buffer, width=150 * mm, height=18 * mm))
        qr = qrcode.make(pix_payload)
        qr_buffer = BytesIO()
        qr.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        story += [
            Paragraph("PIX Copia e Cola", styles["Normal"]),
            Image(qr_buffer, width=32 * mm, height=32 * mm),
            Paragraph("Documento demonstrativo. Não representa cobrança bancária registrada.", styles["Normal"]),
        ]
        document.build(story)
        return output.getvalue()
