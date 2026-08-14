from __future__ import annotations

import json
import logging
from datetime import date
from decimal import Decimal
from pathlib import Path
from threading import RLock
from time import monotonic

from app.domain.entities.cliente import Cliente
from app.domain.entities.fatura import Fatura
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.value_objects.cpf import CPF
from app.domain.value_objects.dinheiro import Dinheiro

logger = logging.getLogger(__name__)


class ClienteTxtRepository(ClienteRepository):
    """Adaptador JSON Lines. O restante da aplicação desconhece o formato."""

    def __init__(self, file_path: str, cache_ttl_seconds: int = 60) -> None:
        self._path = Path(file_path).resolve()
        self._ttl = cache_ttl_seconds
        self._cache: dict[str, Cliente] | None = None
        self._invoice_cache: dict[str, Fatura] | None = None
        self._loaded_at = 0.0
        self._lock = RLock()

    def buscar_por_cpf(self, cpf: str) -> Cliente | None:
        normalized = CPF.normalize(cpf)
        records, _ = self._records()
        return records.get(normalized)

    def buscar_fatura_por_cpf(self, cpf: str) -> Fatura | None:
        normalized = CPF.normalize(cpf)
        _, invoices = self._records()
        return invoices.get(normalized)

    def _records(self) -> tuple[dict[str, Cliente], dict[str, Fatura]]:
        with self._lock:
            if (
                self._cache is not None
                and self._invoice_cache is not None
                and (self._ttl == 0 or monotonic() - self._loaded_at < self._ttl)
            ):
                return self._cache, self._invoice_cache
            if not self._path.is_file():
                raise FileNotFoundError("Base de clientes não encontrada.")
            records: dict[str, Cliente] = {}
            invoices: dict[str, Fatura] = {}
            with self._path.open("r", encoding="utf-8") as source:
                for line_number, line in enumerate(source, start=1):
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        client = Cliente(
                            cpf=CPF(str(data["cpf"])),
                            nome=str(data["nome"]),
                            telefone=str(data["telefone"]),
                            endereco=str(data["endereco"]),
                            cidade=str(data["cidade"]),
                            estado=str(data["estado"]),
                            cep=str(data["cep"]),
                        )
                        records[client.cpf.value] = client
                        invoices[client.cpf.value] = Fatura(
                            cliente=client,
                            numero=str(data.get("numero_fatura", f"FAT-{client.cpf.value[-8:]}")),
                            valor=Dinheiro(Decimal(str(data["valor"]))),
                            vencimento=date.fromisoformat(str(data["vencimento"])),
                            status=str(data["status"]),
                            data_emissao=date.fromisoformat(str(data["data_emissao"])),
                        )
                    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                        logger.warning("Linha inválida na base de clientes: %s", line_number)
                        raise ValueError("Base de clientes contém uma linha inválida.") from exc
            self._cache = records
            self._invoice_cache = invoices
            self._loaded_at = monotonic()
            return records, invoices
