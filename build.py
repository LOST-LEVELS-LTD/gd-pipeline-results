# -*- coding: utf-8 -*-
"""Сборка сайта документации из content/*.md и templates/*.html в docs/.

Страницы-документы генерируются из markdown; обзорная страница и саммари
фазы «Игрок» лежат в templates/ с маркером @@SIDENAV@@.
"""
import pathlib
import markdown

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
DOCS = ROOT / "docs"

MD = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])

# ── навигация ────────────────────────────────────────────────────────────────

RUN4_NAV = [
    ("brief.html", "Бриф"),
    ("pool.html", "Пул идей"),
    ("candidates.html", "Отбор кандидатов"),
    ("concept-a.html", "Карточка A — Коридор"),
    ("concept-b.html", "Карточка B — Литерный"),
    ("concept-c.html", "Карточка C — Страна"),
    ("verdict-a.html", "Вердикт критика A"),
    ("verdict-b.html", "Вердикт критика B"),
    ("verdict-c.html", "Вердикт критика C"),
    ("report.html", "Итоговый отчёт"),
]
RUN3_NAV = [
    ("brief.html", "Бриф"),
    ("pool.html", "Пул идей"),
    ("candidates.html", "Отбор кандидатов"),
    ("concept-a.html", "Карточка A — Совет"),
    ("concept-b.html", "Карточка B — Полоса"),
    ("concept-c.html", "Карточка C — Чугунка"),
    ("verdict-a.html", "Вердикт критика A"),
    ("verdict-b.html", "Вердикт критика B"),
    ("verdict-c.html", "Вердикт критика C"),
    ("report.html", "Итоговый отчёт"),
]
PLAYER_NAV = [
    ("index.html", "Саммари пилота"),
    ("rules.html", "Свод правил сцены"),
    ("rng.html", "Сид-лог случайности"),
    ("exploiter.html", "Партия: эксплойтер"),
    ("exploiter-2.html", "Эксплойтер, дубль"),
    ("casual.html", "Партия: казуал"),
    ("casual-2.html", "Казуал, дубль"),
    ("verdict.html", "Вердикт фазы"),
]

GROUPS = [
    ("run4", "run-4", "Прогон №4 — Простой язык", RUN4_NAV),
    ("run3", "run-3", "Прогон №3 — Новые территории", RUN3_NAV),
    ("player", "player", "Фаза «Игрок» — симуляция", PLAYER_NAV),
]


def sidenav(rel, gkey, active_file):
    home_cls = ' class="s-home on"' if gkey == "home" else ' class="s-home"'
    parts = [f'<a{home_cls} href="{rel}index.html">Обзор</a>']
    for key, d, label, items in GROUPS:
        op = " open" if key == gkey else ""
        links = []
        for f, t in items:
            on = ' class="on"' if (key == gkey and f == active_file) else ""
            links.append(f'<a{on} href="{rel}{d}/{f}">{t}</a>')
        parts.append(f'<details{op}><summary>{label}</summary>{"".join(links)}</details>')
    return ('<details class="side" open><summary>Навигация</summary>'
            f'<nav class="sidenav">{"".join(parts)}</nav></details>')


# ── шаблон страницы-документа ────────────────────────────────────────────────

PAGE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@ — gd-pipeline: результаты прогонов</title>
<meta name="description" content="@@DESC@@">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=PT+Serif:ital,wght@0,400;0,700;1,400&family=Russo+One&display=swap" rel="stylesheet">
<link rel="stylesheet" href="@@REL@@assets/style.css">
</head>
<body>
<header class="topbar"><div class="in">
  <a class="brand" href="@@REL@@index.html">gd-pipeline</a>
  <span class="tag">результаты прогонов · Lost Levels</span>
</div></header>
<div class="shell">
@@SIDENAV@@
<div class="content">
  <nav class="crumbs">@@CRUMBS@@</nav>
  <div class="doc-head">
    <p class="over">@@OVER@@</p>
    <h1>@@H1@@</h1>
    <span class="badge doc">@@DOCTYPE@@</span>
  </div>
  <article class="doc">
@@BODY@@
  </article>
  <nav class="docnav">
    <span>@@PREV@@</span>
    <span>@@NEXT@@</span>
  </nav>
</div>
</div>
<footer><div class="in">
  <span>Lost Levels · сгенерировано конвейером gd-pipeline</span>
  <span><a href="@@REL@@index.html">обзор</a> · <a href="@@REL@@player/index.html">фаза «Игрок»</a></span>
</div></footer>
<script>if(matchMedia('(max-width:900px)').matches)document.querySelector('.side').removeAttribute('open')</script>
</body>
</html>
"""

# (src, out, h1, doctype)
RUN3 = [
    ("00-brief.md", "brief.html", "Бриф прогона", "входной документ"),
    ("01-pool.md", "pool.html", "Пул идей генератора", "20 идей"),
    ("02-candidates.md", "candidates.html", "Отбор кандидатов", "ранжирование"),
    ("03-concept-a-board.md", "concept-a.html", "A — «Совет директоров»", "концепт-карточка"),
    ("03-concept-b-saboteurs.md", "concept-b.html", "B — «Полоса отчуждения»", "концепт-карточка"),
    ("03-concept-c-crews.md", "concept-c.html", "C — «Чугунка»", "концепт-карточка"),
    ("04-verdict-a-board.md", "verdict-a.html", "Вердикт критика — A", "вердикт"),
    ("04-verdict-b-saboteurs.md", "verdict-b.html", "Вердикт критика — B", "вердикт"),
    ("04-verdict-c-crews.md", "verdict-c.html", "Вердикт критика — C", "вердикт"),
    ("06-report.md", "report.html", "Итоговый отчёт прогона №3", "синтез"),
]
RUN4 = [
    ("00-brief.md", "brief.html", "Бриф прогона", "входной документ"),
    ("01-pool.md", "pool.html", "Пул идей генератора", "20 идей"),
    ("02-candidates.md", "candidates.html", "Отбор кандидатов", "ранжирование"),
    ("03-concept-a-corridor.md", "concept-a.html", "A — «Магистраль-коридор»", "концепт-карточка"),
    ("03-concept-b-golden.md", "concept-b.html", "B — «Литерный состав»", "концепт-карточка"),
    ("03-concept-c-loopland.md", "concept-c.html", "C — «Страна вокруг рельсов»", "концепт-карточка"),
    ("04-verdict-a-corridor.md", "verdict-a.html", "Вердикт критика — A", "вердикт"),
    ("04-verdict-b-golden.md", "verdict-b.html", "Вердикт критика — B", "вердикт"),
    ("04-verdict-c-loopland.md", "verdict-c.html", "Вердикт критика — C", "вердикт"),
    ("06-report.md", "report.html", "Итоговый отчёт прогона №4", "синтез"),
]
PLAYER = [
    ("05-play-b-rules.md", "rules.html", "Свод правил сцены", "формализация концепта"),
    ("05-play-b-rng.md", "rng.html", "Сид-лог случайности", "68 карт"),
    ("05-play-b-exploiter.md", "exploiter.html", "Партия: эксплойтер", "протокол партии"),
    ("05-play-b-exploiter-2.md", "exploiter-2.html", "Партия: эксплойтер, дубль", "протокол партии"),
    ("05-play-b-casual.md", "casual.html", "Партия: казуал", "протокол партии"),
    ("05-play-b-casual-2.md", "casual-2.html", "Партия: казуал, дубль", "протокол партии"),
    ("05-play-b.md", "verdict.html", "Вердикт фазы «Игрок»", "сводка"),
]

SECTIONS = [
    ("run3", "run3", "run-3", RUN3, "Прогон №3 — «Новые территории»", "report.html",
     "Прогон №3 конвейера gd-pipeline: бриф, идеи, концепт-карточки, вердикты критика, отчёт"),
    ("run4", "run4", "run-4", RUN4, "Прогон №4 — «Простой язык»", "report.html",
     "Прогон №4 конвейера gd-pipeline: бриф, идеи, концепт-карточки, вердикты критика, отчёт"),
    ("player", "player", "player", PLAYER, "Фаза «Игрок» — симуляция", "index.html",
     "Симуляционная проверка концепта агентом-игроком: правила сцены, партии, метрики"),
]


def render(tpl, **kw):
    out = tpl
    for k, v in kw.items():
        out = out.replace("@@" + k.upper() + "@@", v)
    return out


def build():
    rel = "../"
    for gkey, src_dir, out_dir, pages, sec_title, sec_home, desc in SECTIONS:
        out = DOCS / out_dir
        out.mkdir(parents=True, exist_ok=True)
        for i, (src, dst, h1, doctype) in enumerate(pages):
            text = (CONTENT / src_dir / src).read_text(encoding="utf-8")
            MD.reset()
            body = MD.convert(text)
            prev_html = next_html = ""
            if i > 0:
                p = pages[i - 1]
                prev_html = f'<a href="{p[1]}">← {p[2]}</a>'
            if i < len(pages) - 1:
                n = pages[i + 1]
                next_html = f'<a href="{n[1]}">{n[2]} →</a>'
            crumbs = (f'<a href="{rel}index.html">Обзор</a> · '
                      f'<a href="{sec_home}">{sec_title}</a> · {h1}')
            html = render(
                PAGE, title=h1, desc=desc, rel=rel, crumbs=crumbs,
                over=sec_title, h1=h1, doctype=doctype, body=body,
                prev=prev_html, next=next_html,
                sidenav=sidenav(rel, gkey, dst),
            )
            (out / dst).write_text(html, encoding="utf-8")
            print(f"  {out_dir}/{dst}")
    # рукописные страницы из шаблонов
    idx = (TEMPLATES / "index.html").read_text(encoding="utf-8")
    (DOCS / "index.html").write_text(
        idx.replace("@@SIDENAV@@", sidenav("", "home", None)), encoding="utf-8")
    print("  index.html")
    pl = (TEMPLATES / "player-index.html").read_text(encoding="utf-8")
    (DOCS / "player" / "index.html").write_text(
        pl.replace("@@SIDENAV@@", sidenav("../", "player", "index.html")), encoding="utf-8")
    print("  player/index.html")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print("OK")


if __name__ == "__main__":
    build()
