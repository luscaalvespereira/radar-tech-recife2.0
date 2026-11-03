import argparse
import hashlib
import html
import os
import re
import sqlite3
import sys
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse

# Assegura suporte universal a UTF-8 no console Windows (evita charmap UnicodeEncodeError)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import feedparser
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

# Tenta importar BeautifulSoup para parsing HTML refinado com fallback transparente para regex
try:
    from bs4 import BeautifulSoup

    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

from config import (
    DB_PATH,
    FEEDS,
    HIGH_PRIORITY,
    INSTAGRAM_ACCOUNTS,
    LOW_PRIORITY,
    POLL_INTERVAL_MINUTES,
    RELEVANT,
    RSSHUB_BASE,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    USER_AGENT,
)


def ensure_directories():
    """Garante a existência das pastas necessárias para o banco e dados locais."""
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)


def init_db():
    """Inicializa o esquema do banco de dados SQLite com índices para consultas rápidas."""
    ensure_directories()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            link TEXT NOT NULL,
            published TEXT,
            score INTEGER NOT NULL,
            priority TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute("CREATE INDEX IF NOT EXISTS idx_items_score ON items(score);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_items_created ON items(created_at);")
    con.commit()
    con.close()


def stable_id(source: str, link: str, title: str) -> str:
    """Gera um hash SHA-256 único e determinístico para deduplicação perpétua."""
    raw = f"{source.strip()}|{link.strip()}|{title.strip()}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def normalize(text: str) -> str:
    """Limpa e normaliza textos removendo tags, quebras excessivas e padronizando em minúsculas."""
    text = html.unescape(text or "")
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def score_item(title: str, summary: str) -> int:
    """
    Motor Heurístico de Classificação Semântica:
    - Palavras de Ação Imediata/Edital (HIGH_PRIORITY): +4 pts
    - Palavras Territoriais/Ecosistema (RELEVANT): +2 pts
    - Palavras de Evento Expirado/Ruído (LOW_PRIORITY): -3 pts
    - Bônus Geográfico Estratégico (Recife, Porto Digital, CESAR, NERD): +2 a +3 pts
    """
    text = normalize(f"{title} {summary}")
    score = 0

    for word in RELEVANT:
        if word in text:
            score += 2

    for word in HIGH_PRIORITY:
        if word in text:
            score += 4

    for word in LOW_PRIORITY:
        if word in text:
            score -= 3

    if "recife" in text:
        score += 3

    if "porto digital" in text or "cesar" in text or "nerd" in text:
        score += 2

    return score


def priority_label(score: int) -> str:
    """Converte o score numérico em etiqueta visual de urgência."""
    if score >= 8:
        return "🔥 ALTA"
    if score >= 4:
        return "⚡ MÉDIA"
    return "👀 BAIXA"


def extract_links_from_html(url: str):
    """
    Extrai links de páginas HTML públicas utilizando BeautifulSoup quando disponível,
    com fallback seguro em Expressões Regulares compiladas.
    """
    try:
        response = requests.get(
            url,
            timeout=25,
            headers={"User-Agent": USER_AGENT},
        )
        response.raise_for_status()
    except Exception as error:
        print(f"[ERRO REDE] Não foi possível acessar {url}: {error}")
        return []

    items = {}

    if HAS_BS4:
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"].strip()
                title = a_tag.get_text(separator=" ", strip=True)

                if not title or len(title) < 12:
                    continue

                full_url = urljoin(url, href)
                parsed = urlparse(full_url)
                if parsed.scheme not in ("http", "https"):
                    continue

                if full_url not in items:
                    items[full_url] = {
                        "title": title,
                        "link": full_url,
                        "summary": title,
                    }
        except Exception as parse_err:
            print(f"[AVISO PARSER] Falha no BeautifulSoup, usando fallback regex: {parse_err}")

    # Fallback ou execução se BeautifulSoup não capturou itens
    if not items:
        links = re.findall(
            r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
            response.text,
            re.IGNORECASE | re.DOTALL,
        )
        for href, raw_title in links:
            title = re.sub(r"<[^>]+>", "", raw_title)
            title = html.unescape(title).strip()
            if not title or len(title) < 12:
                continue

            full_url = urljoin(url, href.strip())
            parsed = urlparse(full_url)
            if parsed.scheme not in ("http", "https"):
                continue

            if full_url not in items:
                items[full_url] = {
                    "title": title,
                    "link": full_url,
                    "summary": title,
                }

    return list(items.values())[:40]


def fetch_feed(source: dict):
    """Encaminha a extração conforme o tipo configurado (HTML Scraper ou RSS Parser)."""
    if source.get("type") == "html":
        return extract_links_from_html(source["url"])

    # Se for feed RSS/Atom (ex: RSSHub)
    try:
        parsed = feedparser.parse(source["url"])
        items = []
        for entry in parsed.entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            summary = entry.get("summary", "") or entry.get("description", "")
            if title and link:
                items.append({
                    "title": title,
                    "link": link,
                    "summary": summary,
                })
        return items
    except Exception as error:
        print(f"[ERRO RSS] Falha ao processar feed {source['name']}: {error}")
        return []


def send_telegram(message: str) -> bool:
    """Envia alerta formatado para o canal ou chat configurado no Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[AVISO] Telegram não configurado no .env. Item gravado apenas no banco de dados.")
        return False

    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }

    try:
        response = requests.post(api_url, data=payload, timeout=20)
        if response.status_code != 200:
            print(f"[ERRO TELEGRAM HTTP {response.status_code}] {response.text}")
            return False
        return True
    except Exception as error:
        print(f"[ERRO TELEGRAM DISPATCH] {error}")
        return False


def already_saved(item_id: str) -> bool:
    """Consulta se o hash do item já existe no banco de dados SQLite."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT 1 FROM items WHERE id = ?", (item_id,))
    found = cur.fetchone() is not None
    con.close()
    return found


def save_item(item: dict) -> bool:
    """Salva atomicamente uma nova oportunidade no banco de dados."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        """
        INSERT OR IGNORE INTO items (id, source, title, link, published, score, priority, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            item["id"],
            item["source"],
            item["title"],
            item["link"],
            item["published"],
            item["score"],
            item["priority"],
            datetime.now().isoformat(),
        ),
    )
    inserted = cur.rowcount > 0
    con.commit()
    con.close()
    return inserted


def build_message(item: dict) -> str:
    """Formata a mensagem para o Telegram com escaping seguro contra tags quebradas."""
    safe_priority = html.escape(item["priority"])
    safe_source = html.escape(item["source"])
    safe_title = html.escape(item["title"])
    safe_link = html.escape(item["link"])
    safe_date = html.escape(item["published"])
    score_val = item["score"]

    return (
        f"<b>{safe_priority} — {safe_source}</b>\n\n"
        f"📌 <b>{safe_title}</b>\n\n"
        f"📅 <i>Detectado:</i> {safe_date}\n"
        f"🎯 <i>Score de Relevância:</i> {score_val}\n\n"
        f"🔗 <a href=\"{safe_link}\">Abrir e verificar inscrição oficial</a>"
    )


def run_radar():
    """Varre todas as fontes cadastradas, filtra por score, deduplica e despacha alertas."""
    print(f"\n[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] 🚀 Executando varredura do RADAR TECH RECIFE...")

    sources = list(FEEDS)

    # Injeta rotas do Instagram via RSSHub se configurado
    for username in INSTAGRAM_ACCOUNTS:
        sources.append({
            "name": f"Instagram — @{username}",
            "url": f"{RSSHUB_BASE}/instagram/user/{username}",
            "type": "rss",
        })

    novas_capturas = 0

    for source in sources:
        source_name = source["name"]
        try:
            entries = fetch_feed(source)
        except Exception as error:
            print(f"[FALHA FONTE] {source_name}: {error}")
            continue

        for entry in entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            summary = entry.get("summary", "").strip()

            if not title or not link:
                continue

            item_id = stable_id(source_name, link, title)
            if already_saved(item_id):
                continue

            score = score_item(title, summary)

            # Filtro de corte: descarta ruído abaixo de 4 pontos
            if score < 4:
                continue

            item = {
                "id": item_id,
                "source": source_name,
                "title": title,
                "link": link,
                "published": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "score": score,
                "priority": priority_label(score),
            }

            if save_item(item):
                novas_capturas += 1
                msg = build_message(item)
                if send_telegram(msg):
                    print(f"  [ENVIADO TELEGRAM] {item['priority']} | {source_name} -> {title[:60]}...")
                else:
                    print(f"  [SALVO NO BANCO] {item['priority']} | {source_name} -> {title[:60]}...")
                time.sleep(0.5)

    print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] ✅ Varredura finalizada. Novas oportunidades salvas: {novas_capturas}")


def test_telegram_connection():
    """Envia uma mensagem de teste para validar o BOT_TOKEN e CHAT_ID informados."""
    print("\n🔍 Testando conectividade com o Telegram Bot...")
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ ERRO: TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não estão preenchidos no arquivo .env!")
        return False

    test_msg = (
        "🤖 <b>RADAR TECH RECIFE — Teste de Comunicação</b>\n\n"
        "✅ O bot está conectado e configurado com sucesso.\n"
        f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        "📍 Ecossistema: Porto Digital, CESAR, O NERD e Recife Tech."
    )
    ok = send_telegram(test_msg)
    if ok:
        print("✅ Mensagem enviada com sucesso ao Telegram! Verifique seu canal ou conversa.")
    else:
        print("❌ Falha no envio ao Telegram. Verifique seu token, chat_id e permissões de administrador do bot.")
    return ok


def main():
    parser = argparse.ArgumentParser(description="RADAR TECH RECIFE — Monitor Autônomo de Oportunidades")
    parser.add_argument("--once", action="store_true", help="Executa uma única varredura e finaliza.")
    parser.add_argument("--test-telegram", action="store_true", help="Testa as credenciais do Telegram e envia um ping.")
    parser.add_argument("--daemon", action="store_true", help="Roda continuamente via Scheduler no intervalo configurado.")

    args = parser.parse_args()

    init_db()

    if args.test_telegram:
        test_telegram_connection()
        return

    if args.once:
        run_radar()
        return

    # Modo padrão: executa a primeira vez imediatamente e entra em agendamento cíclico
    run_radar()

    scheduler = BlockingScheduler()
    scheduler.add_job(run_radar, "interval", minutes=POLL_INTERVAL_MINUTES)
    print(f"\n📡 RADAR TECH RECIFE ativo em modo contínuo (Executando a cada {POLL_INTERVAL_MINUTES} minutos).")
    print("Pressione Ctrl+C para encerrar com segurança.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Encerrando RADAR TECH RECIFE de forma ordenada.")


if __name__ == "__main__":
    main()
