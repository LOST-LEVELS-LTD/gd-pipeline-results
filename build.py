# -*- coding: utf-8 -*-
"""Сборка страниц-документов сайта из content/*.md в docs/.

Главная (docs/index.html) и саммари игрока (docs/player/index.html) написаны
руками и этим скриптом не трогаются.
"""
import pathlib
import markdown

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "content"
DOCS = ROOT / "docs"

MD = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])

PAGE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — ГД-архив LOST LEVELS</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=PT+Serif:ital,wght@0,400;0,700;1,400&family=Russo+One&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body>
<header class="topbar"><div class="in">
  <a class="brand" href="{rel}index.html">ГД-архив <b>Lost Levels</b></a>
  <span class="tag">депо идей · прогоны конвейера</span>
</div></header>
<nav class="crumbs">{crumbs}</nav>
<main>
  <div class="doc-head">
    <p class="over">{over}</p>
    <h1>{h1}</h1>
    <span class="stamp doc">{doctype}</span>
  </div>
  <article class="doc">
{body}
  </article>
  <nav class="docnav">
    <span>{prev}</span>
    <span>{next}</span>
  </nav>
</main>
<footer><div class="in">
  <span>Сгенерировано конвейером gd-pipeline · Lost Levels Ltd · 2026</span>
  <span><a href="{rel}index.html">архив</a> · <a href="{rel}player/index.html">агент-игрок</a></span>
</div></footer>
</body>
</html>
"""

# (src, out, h1, doctype)
RUN3 = [
    ("00-brief.md", "brief.html", "Бриф прогона", "бриф"),
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
    ("00-brief.md", "brief.html", "Бриф прогона", "бриф"),
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
    ("05-play-b-rules.md", "rules.html", "Свод правил сцены", "формализация"),
    ("05-play-b-rng.md", "rng.html", "Сид-лог случайности", "68 карт, сид 20260722"),
    ("05-play-b-exploiter.md", "exploiter.html", "Партия: эксплойтер", "протокол партии"),
    ("05-play-b-exploiter-2.md", "exploiter-2.html", "Партия: эксплойтер, дубль", "протокол партии"),
    ("05-play-b-casual.md", "casual.html", "Партия: казуал", "протокол партии"),
    ("05-play-b-casual-2.md", "casual-2.html", "Партия: казуал, дубль", "протокол партии"),
    ("05-play-b.md", "verdict.html", "Вердикт фазы «Игрок»", "сводка оркестратора"),
]

SECTIONS = [
    ("run3", "run-3", RUN3, "Прогон №3 · «Новые территории» · 2026-07-22",
     "Прогон №3 конвейера gd-pipeline: бриф, идеи, карточки, вердикты"),
    ("run4", "run-4", RUN4, "Прогон №4 · «Простой язык» · 2026-07-22",
     "Прогон №4 конвейера gd-pipeline: бриф, идеи, карточки, вердикты, игрок"),
    ("player", "player", PLAYER, "Фаза «Игрок» · пилот на «Литерном составе»",
     "Симуляционный плейтест концепта агентом-игроком: правила, партии, метрики"),
]


def crumb(rel, sec_title, page_title, sec_home):
    return (f'<a href="{rel}index.html">Архив</a> · '
            f'<a href="{sec_home}">{sec_title}</a> · {page_title}')


def build():
    for src_dir, out_dir, pages, sec_title, desc in SECTIONS:
        out = DOCS / out_dir
        out.mkdir(parents=True, exist_ok=True)
        rel = "../"
        sec_home = rel + "index.html" if out_dir != "player" else "index.html"
        if out_dir == "player":
            sec_home = "index.html"
        elif out_dir in ("run-3", "run-4"):
            sec_home = "report.html"
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
            html = PAGE.format(
                title=h1, desc=desc, rel=rel,
                crumbs=crumb(rel, sec_title, h1, sec_home),
                over=sec_title, h1=h1, doctype=doctype,
                body=body, prev=prev_html, next=next_html,
            )
            (out / dst).write_text(html, encoding="utf-8")
            print(f"  {out_dir}/{dst}")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print("OK")


if __name__ == "__main__":
    build()
