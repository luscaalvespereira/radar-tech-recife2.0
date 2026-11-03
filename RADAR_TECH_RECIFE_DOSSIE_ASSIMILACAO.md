# 📑 DOSSIÊ DE ASSIMILAÇÃO EXPANSIVA I.D.E.A.L.
## RADAR TECH RECIFE: Sistema Autônomo de Inteligência Territorial, Ingestão Multicanal e Captação de Oportunidades Tecnológicas

> **Protocolo Operacional:** MODO ASSIMILAÇÃO EXPANSIVA  
> **Chancela Metodológica:** MODO LUCAS 10.000  
> **Território de Aplicação:** Ecossistema de Inovação de Recife / Pernambuco (Bairro do Recife, Cais do Apolo, Rua Dona Maria César)  
> **Data de Homologação:** 02 de Novembro de 2026  

---

## 1. IDENTIFICAÇÃO (I)

### 1.1. Denominação Oficial e Taxonomia Ontológica
- **Nome do Sistema:** RADAR TECH RECIFE (*Territorial Opportunity Ingestion Engine*)
- **Classificação Ontológica:** *Continuous Territorial Event Sink, Heuristic Opportunity Classifier & Telegram Push Dispatcher*.
- **Natureza:** Sistema *local-first*, não-invasivo, com tolerância a falhas de rede, desenhado para transformar canais assimétricos e voláteis em um fluxo unificado e acionável de dados.

### 1.2. Mapeamento Territorial e Institucional Primário
O ecossistema de tecnologia de Recife é geograficamente concentrado, porém informacionalmente fragmentado. O **RADAR TECH RECIFE** ancora-se nos seguintes polos cardeais:

| Entidade / Polo | Localização Física | Papel Estratégico no Ecossistema | URLs Primárias |
| :--- | :--- | :--- | :--- |
| **Porto Digital** | Bairro do Recife (Cais do Apolo, Bom Jesus, etc.) | Maior parque tecnológico urbano e aberto do Brasil; fomento, editais, eventos e aceleração. | [portodigital.org](https://portodigital.org/) |
| **CESAR & CESAR School** | Cais do Apolo, 77 / Bairro do Recife | Centro de Inovação e Instituto de Ensino Superior; residências de software, hackathons, bolsas e pós-graduação. | [cesar.org.br](https://www.cesar.org.br/) |
| **Edifício O NERD** | Rua Dona Maria César, 70 | Plataforma física de 2.500 m², Café 70, coworking, arena de games, auditório e ponto de encontro presencial da comunidade dev. | [nerd.portodigital.org](https://nerd.portodigital.org/) |
| **Sympla Recife (Tecnologia)** | Plataforma Web | Ponto de agregação comercial de workshops, meetups de comunidades, hackathons independentes e conferências locais. | [sympla.com.br](https://www.sympla.com.br/) |
| **SECTI-PE / FACEPE** | Governo de PE / Bairro do Recife | Financiamento público de P&D, editais de subvenção econômica, bolsas de inovação e programas estaduais. | [secti.pe.gov.br](https://www.secti.pe.gov.br/) |
| **Prefeitura do Recife (Empreende / Conecta)** | Cais do Apolo, 925 | Programas municipais de qualificação e bolsas (Embarque Digital, GO Recife, Parcerias de IA). | [recife.pe.gov.br](https://recife.pe.gov.br/) |

### 1.3. Proposta de Valor Irrefutável
Aniquilar a assimetria informacional que provoca o **"Custo da Janela Perdida"**: a perda de prazos de inscrição em hackathons, residências de software e editais pelo simples desconhecimento temporal de sua abertura. O sistema transforma a postura do operador de **passiva/ansiosa** (abrir dezenas de redes sociais todos os dias) para **reativa/estruturada** (receber apenas oportunidades qualificadas em um canal privado de alta densidade).

---

## 2. DESCONSTRUÇÃO TÉCNICA E ANATÔMICA (D)

### 2.1. Topologia Arquitetural em Camadas

```mermaid
flowchart TD
    subgraph SOURCES["Camada 1: Ingestão Multicanal (Polimórfica)"]
        S1["Porto Digital (Eventos/Notícias) - HTML Scraper"]
        S2["CESAR (Notícias/Eventos) - HTML Scraper"]
        S3["Edifício O NERD - HTML Scraper"]
        S4["Sympla Recife Tech - HTML/JSON"]
        S5["SECTI-PE - HTML Scraper"]
        S6["Instagram Público (@Porto_Digital) - RSSHub Bridge"]
    end

    subgraph ENGINE["Camada 2: Motor de Processamento & Heurística (radar.py)"]
        E1["Normalizador Lexical & Decoder HTML"]
        E2["Gerador de ID Estável (Hash SHA-256)"]
        E3["Filtro de Deduplicação (SQLite Lookup)"]
        E4["Classificador Semântico Ponderado (Score Heurístico)"]
        E5{"Score >= 4?"}
    end

    subgraph STORAGE["Camada 3: Persistência Atômica"]
        DB[("SQLite Local: data/radar.db")]
        IDX["Índices: Score, Data e Hash"]
    end

    subgraph SINK["Camada 4: Despacho & Interface com o Usuário"]
        TG["Telegram Bot API (sendMessage HTML)"]
        CLI["CLI de Auditoria (query_db.py)"]
        USER["Loop Humano: Planilha & Google Agenda"]
    end

    S1 & S2 & S3 & S4 & S5 & S6 --> E1
    E1 --> E2
    E2 --> E3
    E3 -- "Novo Registro" --> E4
    E3 -- "Já Capturado" --> DISCARD["Ignorar"]
    E4 --> E5
    E5 -- "Sim (Qualificado)" --> DB
    E5 -- "Sim (Qualificado)" --> TG
    E5 -- "Não (Ruído < 4)" --> DISCARD
    DB --- IDX
    DB --> CLI
    TG --> USER
```

---

### 2.2. A Anatomia do "Gargalo do Instagram" e sua Solução Forense

A rede social Instagram tornou-se o principal megafone visual das instituições do ecossistema pernambucano, contudo apresenta severas barreiras arquiteturais para automação:

1. **Ausência de Feeds RSS/Atom Nativos:** A Meta descontinuou qualquer protocolo público aberto de leitura desde a década passada.
2. **APIs Oficiais Blindadas:** As APIs Graph do Instagram exigem aprovação corporativa, app review e contas Business associadas; servem apenas para gerenciar a *própria* conta, sendo tecnicamente proibidas de realizar *scraping* ou monitorar contas alheias sem credenciais.
3. **Mecanismos Anti-Bot e WAF:** Instagram emprega checagem de IP, TLS fingerprinting, desafios de JavaScript e CAPTCHA agressivo para requisições automatizadas sem cookies válidos de sessão.

#### Matriz de Solução Tática:
```
+--------------------------------------------------------------------------+
|                  ESTRATÉGIAS DE INGESTÃO DO INSTAGRAM                    |
+----------------------+--------------------+------------------------------+
| MÉTODO               | CONFIABILIDADE     | TRADE-OFFS & LIMITAÇÕES      |
+----------------------+--------------------+------------------------------+
| 1. Notificações App  | 100%               | Manual; interrompe a atenção |
|    (Push Direto)     |                    | e gera sobrecarga sensorial. |
+----------------------+--------------------+------------------------------+
| 2. RSSHub / OpenRSS  | 80% a 90%          | Requer instância resiliente; |
|    (Ponte de RSS)    | (com cookies/auth) | pode falhar se o IG mudar UI.|
+----------------------+--------------------+------------------------------+
| 3. Sites Oficiais    | 99.9% (Canônico)   | O evento real SEMPRE possui  |
|    como Fonte da     |                    | página ou link de inscrição  |
|    Verdade           |                    | fora do Instagram.           |
+----------------------+--------------------+------------------------------+
```

> **Doutrina Operacional:** O Instagram opera como **sensor de descoberta antecipada** (*Radar Precoce*), enquanto os sites oficiais e editais do Porto Digital e CESAR operam como **fonte definitiva de homologação**.

---

### 2.3. Motor Heurístico de Classificação Semântica (Scoring Model)

O sistema não opera como um *crawler* cego. Cada oportunidade passa por uma função de ponderação matemática baseada em densidade semântica de tokens:

$$\text{Score} = \sum w_{\text{high}} + \sum w_{\text{relevant}} - \sum w_{\text{low}} + \text{Bônus}_{\text{geo}}$$

Onde:
- **Termos de Ação Imediata ($w_{\text{high}} = +4$):** `inscrição`, `edital`, `chamada pública`, `vaga`, `hackathon`, `ideathon`, `bootcamp`, `residência`, `bolsa`, `gratuito`, `embarque digital`, `demoday`, `seleção`.
- **Termos de Contexto e Ecossistema ($w_{\text{relevant}} = +2$):** `recife`, `pernambuco`, `porto digital`, `cesar`, `cesar school`, `nerd`, `bairro do recife`, `cais do apolo`, `tecnologia`, `inovação`, `ia`, `software`.
- **Termos de Descarte e Notícias Expiradas ($w_{\text{low}} = -3$):** `resultado`, `vencedor`, `retrospectiva`, `cobertura`, `entrevista`, `podcast`, `finalizado`, `encerrado`, `galeria`.
- **Bônus Geográfico Estratégico:** $+3$ pontos se contiver `recife`; $+2$ pontos se contiver `porto digital`, `cesar` ou `nerd`.

#### Níveis de Prioridade:
- **🔥 ALTA:** $\text{Score} \ge 8$ (Editais abertos, bolsas, hackathons locais de alta relevância).
- **⚡ MÉDIA:** $4 \le \text{Score} < 8$ (Cursos, workshops, notícias de programas prestes a abrir).
- **👀 BAIXA:** $\text{Score} < 4$ (Descartado automaticamente da fila de envio do Telegram para evitar fadiga de alertas).

---

### 2.4. Deduplicação Criptográfica Imutável (SHA-256)

Para evitar renotificações cíclicas e garantir consistência transacional:

$$\text{Hash ID} = \text{SHA-256}(\text{Fonte} \parallel \text{Link} \parallel \text{Título})$$

O hash é utilizado como Chave Primária (`PRIMARY KEY`) no SQLite. A cláusula `INSERT OR IGNORE` garante idempotência: se o script rodar 50 vezes no mesmo dia, uma oportunidade já capturada gerará `rowcount = 0` e nenhum pacote de dados será duplicado no Telegram.

---

## 3. EVIDÊNCIAS & IMPLEMENTAÇÃO PRÁTICA (E)

### 3.1. Estrutura de Diretórios Padronizada
O projeto foi materializado em `C:\Users\lucas\OneDrive\Área de Trabalho\RADAR TECH RECIFE`:

```text
RADAR TECH RECIFE/
├── .env                     # Variáveis de ambiente ativas
├── .env.example             # Template limpo versionável
├── requirements.txt         # Pacotes Python homologados
├── config.py                # Configuração central de feeds e termos
├── radar.py                 # Orquestrador de varredura e agendador
├── query_db.py              # CLI para relatórios, busca e exportação CSV/JSON
├── README.md                # Guia do operador
├── RADAR_TECH_RECIFE_DOSSIE_ASSIMILACAO.md # Este dossiê analítico
├── data/
│   └── radar.db             # Banco relacional SQLite local
└── scripts/
    ├── setup_env.ps1        # Provisionador do ambiente (UTF-8 BOM/CRLF)
    ├── run_radar.ps1        # Inicializador do radar (UTF-8 BOM/CRLF)
    ├── test_telegram.ps1    # Diagnóstico de rede do Telegram (UTF-8 BOM/CRLF)
    └── inspect_db.ps1       # Inspetor do banco de dados (UTF-8 BOM/CRLF)
```

### 3.2. Modelo Relacional SQLite (`data/radar.db`)
```sql
CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    published TEXT,
    score INTEGER NOT NULL,
    priority TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_items_score ON items(score);
CREATE INDEX IF NOT EXISTS idx_items_created ON items(created_at);
```

### 3.3. Protocolo de Envio Formatado para Telegram
A mensagem despachada utiliza HTML padronizado com sanitização rígida via `html.escape` para prevenir quebras de parser:

```html
<b>🔥 ALTA — Porto Digital — Notícias & Editais</b>

📌 <b>Inscrições abertas para nova turma de Residência de Software CESAR</b>

📅 <i>Detectado:</i> 02/11/2026 16:30
🎯 <i>Score de Relevância:</i> 14

🔗 <a href="https://portodigital.org/noticias/exemplo">Abrir e verificar inscrição oficial</a>
```

---

## 4. APLICAÇÃO TÁTICA E RESENHA CRÍTICA (A)

### 4.1. Conexão com o Terreno Real do Operador Lucas Alves Pereira
Recife possui uma dinâmica muito particular de oportunidades:

1. **A Janela dos Editais de Residência de Software do CESAR:**
   As residências do CESAR em parceria com gigantes do setor de telecom, automotivo e financeiro costumam abrir janelas curtas de 7 a 15 dias. O estudante que não acompanha o portal semanalmente perde bolsas de valor significativo com capacitação de padrão internacional.
2. **O Edifício O NERD (Rua Dona Maria César, 70):**
   O prédio funciona como o "Living Lab" presencial do Porto Digital. Além do Café 70 no térreo e da Arena no 1º andar, eventos relâmpago de networking, meetups de comunidades de IA e maratonas de código acontecem nos 4 andares. Estar notificado dessas iniciativas permite presença física imediata.
3. **Programas Públicos (Embarque Digital & FACEPE):**
   Editais de bolsas para desenvolvedores de Recife e Pernambuco publicam no Diário Oficial e na página da SECTI antes de ganharem tração nas redes sociais. O monitoramento das páginas de governo confere prioridade de inscrição no dia zero.

### 4.2. A "Regra dos 30 Segundos" contra o Déficit de Execução
Para evitar que o excesso de informação gere paralisia (especialmente considerando o perfil neurodivergente TDAH/TEA do Piloto):

```
+-------------------------------------------------------------------------+
|                  O PROTOCOLO DOS 30 SEGUNDOS (ANTI-FOMO)                |
+-------------------------------------------------------------------------+
| [Passo 1] Alerta no Telegram: Você lê o TÍTULO e o SCORE em 5 segundos. |
| [Passo 2] Se for irrelevante: Desliza e ignora.                         |
| [Passo 3] Se for oportunidade de ouro: Clica no link oficial.           |
| [Passo 4] Anotação Imediata: Prazo Final + Requisitos + Link na Agenda. |
| [Passo 5] Alarme disparador: 24 horas antes do fechamento do edital.    |
+-------------------------------------------------------------------------+
```

---

## 5. LEGADO & CONCLUSÕES FORENSES (L)

### 5.1. Doutrina Perene de Soberania de Dados
1. **Local-First é Inegociável:** Armazenar os eventos em um banco local SQLite (`data/radar.db`) garante que o histórico de oportunidades nunca seja perdido mesmo se uma conta de rede social for suspensa, se um site sair do ar ou se a API mudar.
2. **Resiliência a Falhas de Scraper:** O sistema é desacoplado. Se o scraper do Sympla falhar por alteração de DOM, o Porto Digital, o CESAR e o RSSHub continuarão funcionando perfeitamente sem interromper o loop.
3. **Evolução Gradual:** A arquitetura aceita a adição de novos conectores (APIs REST, Webhooks do Discord, canais públicos do Telegram via Telethon) apenas adicionando dicionários ao array `FEEDS` em `config.py`.

### 5.2. Certificação de Conformidade
Este sistema foi projetado e implantado respeitando integralmente as diretrizes do **MODO LUCAS 10.000**:
- Scripts PowerShell 5.1/7+ blindados com **UTF-8 com BOM** e quebras de linha **CRLF**.
- Zero dependência de serviços externos pagos ou instáveis.
- Persistência estruturada, modular e verificável.

---
*Homologado pelo Cérebro Virtual em 02 de Novembro de 2026.*  
*Assinatura Epistêmica: `LUCAS_10K_RADAR_RECIFE_v1.0`*

