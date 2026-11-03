import argparse
import csv
import json
import os
import sqlite3
import sys
from datetime import datetime

# Assegura suporte universal a UTF-8 no console Windows (evita charmap UnicodeEncodeError)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from config import DB_PATH


def get_connection():
    if not os.path.exists(DB_PATH):
        print(f"❌ Banco de dados não encontrado em '{DB_PATH}'. Execute o radar primeiro.")
        sys.exit(1)
    return sqlite3.connect(DB_PATH)


def show_stats():
    con = get_connection()
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM items")
    total = cur.fetchone()[0]

    cur.execute("SELECT priority, COUNT(*) FROM items GROUP BY priority ORDER BY COUNT(*) DESC")
    by_priority = cur.fetchall()

    cur.execute("SELECT source, COUNT(*) FROM items GROUP BY source ORDER BY COUNT(*) DESC")
    by_source = cur.fetchall()

    print("\n" + "=" * 65)
    print("📊 ESTATÍSTICAS DO RADAR TECH RECIFE")
    print("=" * 65)
    print(f"Total de Oportunidades Capturadas: {total}")
    print("\nPor Prioridade:")
    for prio, count in by_priority:
        print(f"  • {prio}: {count}")

    print("\nPor Fonte:")
    for src, count in by_source:
        print(f"  • {src}: {count}")
    print("=" * 65 + "\n")
    con.close()


def list_items(limit=30, priority=None, search=None, export_csv=None, export_json=None):
    con = get_connection()
    cur = con.cursor()

    query = "SELECT priority, score, source, title, link, published, created_at FROM items WHERE 1=1"
    params = []

    if priority:
        query += " AND priority LIKE ?"
        params.append(f"%{priority}%")

    if search:
        query += " AND (title LIKE ? OR source LIKE ?)"
        params.append(f"%{search}%")
        params.append(f"%{search}%")

    query += " ORDER BY score DESC, created_at DESC LIMIT ?"
    params.append(limit)

    cur.execute(query, params)
    rows = cur.fetchall()
    con.close()

    if not rows:
        print("ℹ️ Nenhuma oportunidade encontrada com os filtros informados.")
        return

    if export_csv:
        with open(export_csv, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Prioridade", "Score", "Fonte", "Título", "Link", "Data Coleta", "Data Criação"])
            writer.writerows(rows)
        print(f"✅ Exportado com sucesso para '{export_csv}'.")
        return

    if export_json:
        data = [
            {
                "priority": r[0],
                "score": r[1],
                "source": r[2],
                "title": r[3],
                "link": r[4],
                "published": r[5],
                "created_at": r[6],
            }
            for r in rows
        ]
        with open(export_json, mode="w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Exportado com sucesso para '{export_json}'.")
        return

    print("\n" + "=" * 90)
    print(f"🎯 OPORTUNIDADES CAPTURADAS ({len(rows)} exibidas ordenadas por Score)")
    print("=" * 90)
    for r in rows:
        prio, score, src, title, link, pub, _ = r
        print(f"[{prio} | Score: {score:>2}] {src}")
        print(f"  📌 {title}")
        print(f"  🔗 {link}")
        print(f"  📅 {pub}")
        print("-" * 90)


def main():
    parser = argparse.ArgumentParser(description="Consulta de Oportunidades do RADAR TECH RECIFE")
    parser.add_argument("-n", "--limit", type=int, default=30, help="Limite de registros a exibir (padrão: 30)")
    parser.add_argument("-p", "--priority", type=str, help="Filtrar por prioridade (ex: ALTA, MÉDIA)")
    parser.add_argument("-s", "--search", type=str, help="Termo de busca no título ou fonte")
    parser.add_argument("--stats", action="store_true", help="Exibe estatísticas agregadas do banco")
    parser.add_argument("--export-csv", type=str, help="Salva o resultado em arquivo CSV")
    parser.add_argument("--export-json", type=str, help="Salva o resultado em arquivo JSON")

    args = parser.parse_args()

    if args.stats:
        show_stats()
    else:
        list_items(
            limit=args.limit,
            priority=args.priority,
            search=args.search,
            export_csv=args.export_csv,
            export_json=args.export_json,
        )


if __name__ == "__main__":
    main()
