"""Configuração da aplicação via variáveis de ambiente.

Utiliza ``pydantic-settings`` para carregar e validar configuração a partir do
ambiente (e de um arquivo ``.env`` em desenvolvimento). Nenhum segredo é
"hardcoded"; todos os valores possuem defaults seguros para desenvolvimento e
devem ser sobrescritos em produção.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação carregadas do ambiente."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Aplicação -------------------------------------------------------
    app_name: str = Field(default="Telephone Invoice API")
    app_env: str = Field(default="development")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    log_json: bool = Field(default=True, description="Emitir logs em JSON.")

    # --- Fonte de dados --------------------------------------------------
    data_file: str = Field(default="dados/clientes.txt")
    cache_ttl_seconds: int = Field(
        default=60,
        ge=0,
        description="TTL do cache em memória da base de clientes (0 desativa).",
    )

    # --- CORS ------------------------------------------------------------
    cors_allow_origins: list[str] = Field(default_factory=lambda: ["*"])
    cors_allow_credentials: bool = Field(default=False)
    cors_allow_methods: list[str] = Field(default_factory=lambda: ["GET"])
    cors_allow_headers: list[str] = Field(default_factory=lambda: ["*"])

    # --- Beneficiário (emissor do boleto) --------------------------------
    beneficiario_nome: str = Field(default="Telefonia Exemplo S.A.")
    beneficiario_documento: str = Field(default="12345678000199")
    banco_codigo: str = Field(default="341", description="Código do banco (3 dígitos).")
    banco_nome: str = Field(default="Banco Exemplo")
    agencia: str = Field(default="1234")
    conta: str = Field(default="567890")
    carteira: str = Field(default="17")

    # --- PIX -------------------------------------------------------------
    pix_key: str = Field(default="pix@telefonia-exemplo.com.br")
    pix_merchant_name: str = Field(default="TELEFONIA EXEMPLO SA")
    pix_merchant_city: str = Field(default="SAO PAULO")

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() in {"production", "prod"}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Retorna instância única (cacheada) das configurações.

    O uso de ``lru_cache`` garante leitura única do ambiente e permite
    sobrescrita em testes via ``get_settings.cache_clear()``.
    """

    return Settings()
