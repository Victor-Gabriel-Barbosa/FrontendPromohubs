# 🛍️ PromoHubs Bot (Frontend)

Bot do Telegram do ecossistema **PromoHubs**, responsável pela camada de interação com o usuário. Ele funciona como o "frontend" do sistema: recebe comandos e imagens dos usuários no Telegram, consome uma **API PromoHubs** externa para buscar produtos, cupons e promoções, e ainda faz **leitura automática de notas fiscais (OCR)** a partir de fotos.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-26A5E4)

## Índice

- [Sobre o projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Executando o bot](#-executando-o-bot)
- [Estrutura de pastas](#-estrutura-de-pastas)
- [Integração com a API](#-integração-com-a-api)
- [Licença](#-licença)
- [Autor](#-autor)

## 📌 Sobre o projeto

O **PromoHubs** ajuda usuários a encontrar promoções, ofertas e cupons de desconto direto pelo Telegram. Este repositório contém apenas a camada de **bot/frontend**, construída em Python com [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI). Todos os dados (produtos, cupons, ofertas da Kabum, promoções da Steam e notas fiscais salvas) são obtidos e enviados através de uma **API backend** própria, acessada via `API_URL`, que não faz parte deste repositório.

## ✨ Funcionalidades

### Comandos disponíveis

| Comando | Descrição |
|---|---|
| `/start` | Mensagem de boas-vindas com a lista de comandos |
| `/ajuda` | Mostra a mensagem de ajuda |
| `/produtos` | Filtra ofertas por categoria (Smartphone, Notebook, Teclado, Mouse, Controle, Fone de Ouvido, Microfone, Monitor, Console, Cadeira, Memória RAM, SSD, HD ou Ver Todos) |
| `/cupons` | Cupons de desconto por loja (Shopee, Amazon, Mercado Livre, AliExpress ou Ver Todos) |
| `/kabum` | Ofertas da Kabum filtradas por faixa de preço (até R$ 100, R$ 100–500, acima de R$ 500 ou Todas) |
| `/steam` | Promoções da Steam filtradas por faixa de preço (até R$ 20, R$ 20–50, acima de R$ 50 ou Todas) |
| `/contato` | Menu para falar com Suporte, Vendas ou Outros assuntos |

Cada comando de listagem (`/produtos`, `/cupons`, `/kabum`, `/steam`) exibe um teclado inline; ao escolher uma opção, o bot busca os dados na API, filtra o resultado e envia uma mensagem (com foto, quando disponível) para cada item encontrado.

### 📸 Leitura automática de notas fiscais (OCR)

Ao enviar uma **foto**, o bot:

1. Baixa a imagem em maior resolução enviada pelo usuário;
2. Corrige a rotação e melhora o contraste da imagem com OpenCV;
3. Extrai o texto com Tesseract OCR (idioma português);
4. Usa correspondência aproximada (RapidFuzz) para localizar a linha de "TOTAL" / "VALOR À PAGAR", ignorando linhas como "SUBTOTAL" ou "DESCONTO";
5. Responde ao usuário com o valor total identificado;
6. Envia o resultado (texto extraído + valor) para a API via `POST /notas-fiscais`.

## 🏗️ Arquitetura

```
main.py
 ├─ importa bot_instance.py      → cria a instância única do bot (telebot.TeleBot)
 ├─ importa handlers/*           → cada módulo registra seus handlers no bot compartilhado
 └─ bot.infinity_polling()       → inicia o long polling com o Telegram
```

- **`handlers/`** — um arquivo por comando (`@bot.message_handler`) e, quando aplicável, um arquivo `*_callbacks.py` irmão para tratar os cliques nos teclados inline (`@bot.callback_query_handler`). A maioria dos callbacks consulta a API (`API_URL`) e formata a resposta enviada ao usuário.
- **`services/`** — regras de negócio desacopladas dos handlers:
  - `ocr_service.py`: pré-processamento de imagem e extração do valor total via OCR;
  - `nota_fiscal_service.py`: envia o resultado do OCR para a API backend.
- **`config.py`** — carrega variáveis de ambiente (`TEL_TOKEN`, `API_URL`) a partir de um arquivo `.env`.
- **`bot_instance.py`** — instancia o `TeleBot` uma única vez, compartilhado por todos os handlers.

## 🧰 Tecnologias

- [Python](https://www.python.org/)
- [pyTelegramBotAPI (telebot)](https://pypi.org/project/pyTelegramBotAPI/) — integração com a API do Telegram
- [Requests](https://pypi.org/project/requests/) — chamadas HTTP à API PromoHubs
- [python-dotenv](https://pypi.org/project/python-dotenv/) — variáveis de ambiente
- [OpenCV (opencv-python)](https://pypi.org/project/opencv-python/) — pré-processamento de imagem
- [pytesseract](https://pypi.org/project/pytesseract/) + [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) — extração de texto de imagens
- [RapidFuzz](https://pypi.org/project/RapidFuzz/) — correspondência aproximada de texto (fuzzy matching)
- [Pillow](https://pypi.org/project/pillow/) e [NumPy](https://pypi.org/project/numpy/) — suporte ao processamento de imagem

## ✅ Pré-requisitos

- Python 3.11 ou superior
- **Tesseract OCR** instalado no sistema operacional, com o pacote de idioma **português (`por`)**:
  - Ubuntu/Debian: `sudo apt install tesseract-ocr tesseract-ocr-por`
  - Windows: instalar em `C:/Program Files/Tesseract-OCR/` ([instalador oficial](https://github.com/UB-Mannheim/tesseract/wiki)) — esse é o caminho já esperado pelo código em `services/ocr_service.py`
  - macOS: `brew install tesseract tesseract-lang`
- Um token de bot do Telegram, criado com o [@BotFather](https://t.me/BotFather)
- A **API PromoHubs** (backend) em execução, expondo os endpoints listados em [Integração com a API](#-integração-com-a-api)

## 📥 Instalação

```bash
# Clone o repositório
git clone https://github.com/<seu-usuario>/FrontendPromohubs.git
cd FrontendPromohubs

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Instale as dependências
pip install -r requirements.txt
```

> ⚠️ **Nota:** o arquivo `requirements.txt` deste repositório está salvo em UTF-16. Se o `pip install -r requirements.txt` falhar por erro de codificação, converta o arquivo para UTF-8 antes de instalar, por exemplo:
> ```bash
> iconv -f UTF-16LE -t UTF-8 requirements.txt -o requirements.txt
> ```

## ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
TEL_TOKEN=seu_token_do_bot_aqui
API_URL=https://sua-api-promohubs.com
```

| Variável | Descrição |
|---|---|
| `TEL_TOKEN` | Token do bot gerado pelo @BotFather no Telegram |
| `API_URL` | URL base da API PromoHubs (backend) que fornece produtos, cupons, ofertas e recebe as notas fiscais |

## ▶️ Executando o bot

```bash
python main.py
```

Se tudo estiver configurado corretamente, o terminal exibirá `Bot iniciado...` e o bot passará a responder no Telegram via *long polling*.

## 📂 Estrutura de pastas

```
FrontendPromohubs/
├── bot_instance.py                    # Instância compartilhada do TeleBot
├── config.py                          # Carregamento das variáveis de ambiente
├── main.py                            # Ponto de entrada da aplicação
├── requirements.txt                   # Dependências do projeto
├── handlers/
│   ├── start.py                       # /start
│   ├── ajuda.py                       # /ajuda
│   ├── produtos.py                    # /produtos (menu)
│   ├── produtos_callbacks.py          # /produtos (filtro + resposta)
│   ├── cupons.py                      # /cupons (menu)
│   ├── cupons_callbacks.py            # /cupons (filtro + resposta)
│   ├── ofertas_kabum.py               # /kabum (menu)
│   ├── ofertas_kabum_callbacks.py     # /kabum (filtro + resposta)
│   ├── promocoes_steam.py             # /steam (menu)
│   ├── promocoes_steam_callbacks.py   # /steam (filtro + resposta)
│   ├── contato.py                     # /contato (menu)
│   ├── contato_callbacks.py           # /contato (resposta)
│   └── nota_fiscal.py                 # Recebimento de fotos e OCR
└── services/
    ├── ocr_service.py                 # Pré-processamento de imagem + OCR
    └── nota_fiscal_service.py         # Envio do resultado do OCR à API
```

## 🔌 Integração com a API

O bot consome os seguintes endpoints da API PromoHubs (definida em `API_URL`):

| Método | Endpoint | Usado por | Descrição |
|---|---|---|---|
| `GET` | `/produtos` | `/produtos` | Lista de produtos/ofertas gerais |
| `GET` | `/cupons` | `/cupons` | Lista de cupons de desconto por loja |
| `GET` | `/kabum` | `/kabum` | Lista de ofertas da Kabum |
| `GET` | `/promocoes` | `/steam` | Lista de promoções da Steam |
| `POST` | `/notas-fiscais` | Upload de foto | Salva o resultado do OCR de uma nota fiscal |

Cada item retornado por `/produtos`, `/cupons` e `/kabum` só é exibido ao usuário se tiver o campo `publicado: true`.

## 📄 Licença

Distribuído sob a licença **MIT**. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.
