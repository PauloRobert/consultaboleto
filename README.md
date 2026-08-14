# Telephone Invoice API

API REST em Python/FastAPI para consultar clientes e faturas telefônicas por CPF, com geração dinâmica de boleto demonstrativo, PIX Copia e Cola e PDF.

## Decisões arquiteturais

- O domínio não depende de FastAPI: `CPF`, `Dinheiro`, cliente, fatura e boleto são entidades/objetos de valor imutáveis.
- Casos de uso dependem de `Protocol`, e `ClienteTxtRepository` é somente o adaptador da fonte JSON Lines.
- `dados/clientes.txt` usa uma linha JSON por cliente. O repositório valida cada linha e mantém cache em memória com TTL configurável.
- O boleto adota o layout de cobrança FEBRABAN de 44 dígitos: banco + moeda + fator + valor + campo livre de 25 dígitos. A linha digitável usa módulo 10 e o dígito geral usa módulo 11. É um boleto demonstrativo: não está registrado em banco, registradora ou provedor de cobrança.
- O PIX usa BR Code/EMV com Merchant Account Information, valor, txid e CRC16-CCITT.
- PDF é gerado em tempo de execução com ReportLab, Code128 e QR Code real.

## Estrutura

`app/domain` contém regras do domínio; `app/application` contém casos de uso; `app/infrastructure` contém adaptadores TXT, boleto, PIX e PDF; `app/api` contém composição HTTP e `app/schemas` contém contratos Pydantic.

## Execução local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
```

Documentação Swagger: http://localhost:8000/docs. ReDoc: http://localhost:8000/redoc. OpenAPI: http://localhost:8000/openapi.json.

## Endpoints

- `GET /api/v1/clientes/{cpf}` consulta cliente e fatura.
- `GET /api/v1/clientes/{cpf}/boleto` retorna linha digitável e dados derivados.
- `GET /api/v1/clientes/{cpf}/pix` retorna o payload PIX Copia e Cola.
- `GET /api/v1/clientes/{cpf}/fatura/pdf` gera o PDF.
- `GET /health` verifica a saúde da API.

CPF pode ser informado com ou sem máscara. Logs e respostas não expõem o CPF completo.

## Testes, cobertura e qualidade

```bash
pytest
pytest --cov=app --cov-report=term-missing
ruff check .
```

A suíte cobre domínio, repositório, geradores de pagamento, PDF e os endpoints HTTP. O objetivo configurado é 90%; a suíte atual atinge mais de 97%.

## Docker

```bash
docker compose up --build
```

O Compose usa `.env.example` por padrão para permitir a primeira execução. Em produção, crie `.env` fora do versionamento e configure valores próprios, especialmente chave PIX, CORS e fonte de dados.

## Deploy no Render

O arquivo `runtime.txt` fixa Python 3.13.4. Essa versão é necessária para que o `pydantic-core` utilize um wheel pré-compilado, evitando a compilação Rust incompatível com Python 3.14.

Configure um Web Service com:

```text
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Health Check Path: /health
```

O diretório raiz deve ser a raiz deste repositório. Depois de adicionar `runtime.txt`, faça um novo deploy com cache limpo no Render se a plataforma ainda exibir Python 3.14 nos logs.

## Segurança e operação

Há validação rigorosa de CPF e comprimento de entrada, caminho de dados resolvido pelo adaptador, mensagens internas ocultas, request ID, CORS configurável e headers básicos de segurança. O rate limiting e autenticação estão preparados como pontos de extensão, mas não são ativados sem uma política de infraestrutura definida.

Nenhum payload de PIX, linha digitável ou CPF completo deve ser registrado em logs. O boleto e o PIX desta aplicação são adequados para demonstração/testes de integração; uma cobrança real requer integração contratada com banco, registradora ou PSP.