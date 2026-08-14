from __future__ import annotations

import json
import logging
from pathlib import Path
from threading import RLock
from time import monotonic

from app.domain.entities.cliente import Cliente
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.value_objects.cpf import CPF

logger = logging.getLogger(__name__)


class ClienteTxtRepository(ClienteRepository):
    """Adaptador JSON Lines. O restante da aplicação desconhece o formato."""

    def __init__(self, file_path: str, cache_ttl_seconds: int = 60) -> None:
        self._path = Path(file_path).resolve()
        self._ttl = cache_ttl_seconds
        self._cache: dict[str, Cliente] | None = None
        self._loaded_at = 0.0
        self._lock = RLock()

    def buscar_por_cpf(self, cpf: str) -> Cliente | None:
        normalized = CPF.normalize(cpf)
        records = self._records()
        return records.get(normalized)

    def _records(self) -> dict[str, Cliente]:
        with self._lock:
            if self._cache is not None and (self._ttl == 0 or monotonic() - self._loaded_at < self._ttl):
                return self._cache
            if not self._path.is_file():
                raise FileNotFoundError("Base de clientes não encontrada.")
            records: dict[str, Cliente] = {}
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
                    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                        logger.warning("Linha inválida na base de clientes: %s", line_number)
                        raise ValueError("Base de clientes contém uma linha inválida.") from exc
            self._cache = records
            self._loaded_at = monotonic()
            return records
