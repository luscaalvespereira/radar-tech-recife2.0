import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do .env localizado na raiz do projeto
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Configurações do Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

# Configurações do RSSHub / Agregadores
RSSHUB_BASE = os.getenv("RSSHUB_BASE", "https://rsshub.app").rstrip("/")
INSTAGRAM_COOKIE = os.getenv("INSTAGRAM_COOKIE", "").strip()

# Banco de dados e Operação
DB_PATH = os.getenv("DB_PATH", "data/radar.db")
POLL_INTERVAL_MINUTES = int(os.getenv("POLL_INTERVAL_MINUTES", "30"))

# User-Agent para requisições web legítimas e resilientes
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36 (RadarTechRecife/1.0; +https://github.com/lucas)"
)

# ------------------------------------------------------------------------------
# FONTES E FEEDS DE MONITORAMENTO (Recife, PE)
# ------------------------------------------------------------------------------
FEEDS = [
    {
        "name": "Porto Digital — Eventos",
        "url": "https://portodigital.org/eventos/",
        "type": "html",
    },
    {
        "name": "Porto Digital — Notícias & Editais",
        "url": "https://portodigital.org/noticias/",
        "type": "html",
    },
    {
        "name": "CESAR — Notícias e Eventos",
        "url": "https://www.cesar.org.br/noticias-e-eventos",
        "type": "html",
    },
    {
        "name": "Edifício O NERD — Ecossistema Porto Digital",
        "url": "https://nerd.portodigital.org/",
        "type": "html",
    },
    {
        "name": "Sympla — Tecnologia Recife",
        "url": "https://www.sympla.com.br/eventos/recife-pe/tecnologia",
        "type": "html",
    },
    {
        "name": "SECTI PE — Notícias e Editais",
        "url": "https://www.secti.pe.gov.br/",
        "type": "html",
    },
]

# Contas públicas do Instagram monitoradas via RSSHub
# (Formato no RSSHub: /instagram/user/<username>)
INSTAGRAM_ACCOUNTS = [
    "Porto_Digital",
    "inovacao_cesar",
    "cesarschool",
    "onerd.recife",
    "sectipe",
]

# ------------------------------------------------------------------------------
# TAXONOMIA SEMÂNTICA E SISTEMA DE PONTUAÇÃO (SCORE HEURÍSTICO)
# ------------------------------------------------------------------------------

# Termos que representam janelas ativas de oportunidade e ação imediata (+4 pontos cada)
HIGH_PRIORITY = [
    "inscrição",
    "inscricao",
    "inscrições",
    "inscricoes",
    "edital",
    "chamada",
    "chamada pública",
    "vaga",
    "vagas",
    "programa",
    "hackathon",
    "ideathon",
    "curso",
    "workshop",
    "bootcamp",
    "startup",
    "residência",
    "residencia",
    "bolsa",
    "gratuito",
    "abertas",
    "aberto",
    "embarque digital",
    "mina d'água",
    "pitch",
    "demoday",
    "demo day",
    "seleção",
    "selecao",
    "capacitação",
    "capacitacao",
]

# Termos que indicam eventos já consumados, notícias passadas ou baixo valor prático (-3 pontos cada)
LOW_PRIORITY = [
    "resultado",
    "vencedor",
    "vencedores",
    "retrospectiva",
    "cobertura",
    "entrevista",
    "podcast",
    "encerrado",
    "encerradas",
    "finalizado",
    "galeria de fotos",
    "memória",
]

# Termos geográficos e contextuais do ecossistema (+2 pontos cada)
RELEVANT = [
    "recife",
    "pernambuco",
    "porto digital",
    "cesar",
    "cesar school",
    "nerd",
    "bairro do recife",
    "antigo recife",
    "cais do apolo",
    "rua do bom jesus",
    "rua dona maria césar",
    "marco zero",
    "tecnologia",
    "inovação",
    "inovacao",
    "inteligência artificial",
    "ia",
    "software",
    "desenvolvedor",
    "dados",
    "startup",
]

