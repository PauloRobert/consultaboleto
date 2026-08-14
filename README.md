# Consulta Boleto

API REST em Python/FastAPI para consultar clientes e faturas telefônicas por CPF, com geração dinâmica de boleto demonstrativo, PIX Copia e Cola e PDF.

## Decisões arquiteturais

- O domínio não depende de FastAPI: `CPF`, `Dinheiro`, cliente, fatura e boleto são entidades/objetos de valor imutáveis.
- Casos de uso dependem de `Protocol`, e `ClienteTxtRepository` é somente o adaptador da fonte JSON Lines.
- `dados/clientes.txt` usa uma linha JSON por cliente. O repositório valida cada linha e mantém cache em memória com TTL configurável.
- O boleto adota o layout de cobrança FEBRABAN de 44 dígitos: banco + moeda + fator + valor + campo livre de 25 dígitos. A linha digitável usa módulo 10 e o dígito geral usa módulo 11. É um boleto demonstrativo: não está registrado em banco, registradora ou provedor de cobrança.
- O PIX usa BR Code/EMV com Merchant Account Information, valor, txid e CRC16-CCITT.
- PDF é gerado em tempo de execução com ReportLab, Code128 e QR Code real.

Cada linha de `dados/clientes.txt` contém os dados cadastrais e a fatura associada: `cpf`, `nome`, `telefone`, `endereco`, `cidade`, `estado`, `cep`, `numero_fatura`, `valor`, `vencimento`, `status` e `data_emissao`. A base de demonstração possui mais de 100 registros e pode ser regenerada deterministicamente com:

```bash
python scripts/generate_sample_data.py
```

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
- `GET /api/v1/massadados` lista todas as massas sintéticas; aceite `status=PENDENTE`, `PAGA`, `VENCIDA` ou `CANCELADA` para filtrar.
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

Conforme a documentação oficial do Render, `PYTHON_VERSION` tem a maior precedência para selecionar o interpretador e deve conter uma versão completa. O arquivo `.python-version` fornece o fallback versionado no repositório. Ambos fixam Python 3.13.4, versão compatível com o `pydantic-core` utilizado pelo projeto.

Configure um Web Service com:

```text
Build Command: pip install -r requirements.txt
Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
Health Check Path: /health
```

Configure no painel do Render, antes do deploy:

```text
PYTHON_VERSION=3.13.4
```

O diretório raiz deve ser a raiz deste repositório. Cadastre a variável antes de iniciar o deploy e use **Clear build cache & deploy** para descartar o ambiente virtual criado anteriormente com Python 3.14.

Referências oficiais: [versão do Python](https://render.com/docs/python-version) e [deploy de FastAPI](https://render.com/docs/deploy-fastapi).

## Segurança e operação

Há validação rigorosa de CPF e comprimento de entrada, caminho de dados resolvido pelo adaptador, mensagens internas ocultas, request ID, CORS configurável e headers básicos de segurança. O rate limiting e autenticação estão preparados como pontos de extensão, mas não são ativados sem uma política de infraestrutura definida.

Nenhum payload de PIX, linha digitável ou CPF completo deve ser registrado em logs. O boleto e o PIX desta aplicação são adequados para demonstração/testes de integração; uma cobrança real requer integração contratada com banco, registradora ou PSP.