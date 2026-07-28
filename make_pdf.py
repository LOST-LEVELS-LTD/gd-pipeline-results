# -*- coding: utf-8 -*-
"""Сборка PDF-версии документации с навигацией как на сайте.

Навигация в PDF: панель закладок (дерево = сайдбар сайта), кликабельное
оглавление с номерами страниц, работающие внутренние ссылки.

Запуск: python make_pdf.py  →  export/gd-pipeline-results.pdf
"""
import pathlib
import re

import markdown
from weasyprint import HTML

import build  # списки документов и подписи навигации

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "export"
MD = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])

NAV_TITLES = {  # короткие подписи как в сайдбаре
    "run4": dict(build.RUN4_NAV),
    "run3": dict(build.RUN3_NAV),
    "player": dict(build.PLAYER_NAV),
}

PARTS = [  # (gkey, заголовок части, src_dir, список документов)
    ("run4", "Прогон №4 — «Простой язык»", "run4", build.RUN4),
    ("run3", "Прогон №3 — «Новые территории»", "run3", build.RUN3),
    ("player", "Фаза «Игрок» — симуляция", "player", build.PLAYER),
]

CSS = """
@page {
  size: A4;
  margin: 17mm 15mm 18mm 15mm;
  @bottom-center { content: counter(page); font-family: Menlo, monospace;
                   font-size: 9px; color: #6d5f4a; }
  @top-right { content: "gd-pipeline — результаты прогонов"; font-family: Menlo, monospace;
               font-size: 8px; letter-spacing: .08em; color: #a89a7e; }
}
@page :first { @top-right { content: none } @bottom-center { content: none } }

body { font-family: 'PT Serif', Georgia, serif; font-size: 10.5pt; line-height: 1.55;
       color: #241e16; }
a { color: #7c2917; text-decoration: none; }

/* закладки: только структура сайта, без внутренних заголовков документов */
h1.part { bookmark-level: 1; }
h2.dt   { bookmark-level: 2; }
.md h1, .md h2, .md h3, .md h4, .md h5, .md h6 { bookmark-level: none; }
.title-page h1, .toc h1 { bookmark-level: none; }
#overview h2.dt { bookmark-level: 1; }

/* титул */
.title-page { page-break-after: always; padding-top: 70mm; }
.title-page .over { font-family: Menlo, monospace; font-size: 10px; letter-spacing: .2em;
  text-transform: uppercase; color: #a8371f; margin: 0 0 8mm; }
.title-page h1 { font-family: 'Russo One', 'Arial Black', sans-serif; font-size: 30pt;
  line-height: 1.1; margin: 0 0 8mm; }
.title-page p { font-size: 12pt; color: #3d3428; max-width: 130mm; }

/* оглавление */
.toc { page-break-after: always; }
.toc h1 { font-family: 'Russo One', 'Arial Black', sans-serif; font-size: 17pt; }
.toc ul { list-style: none; padding: 0; margin: 0 0 4mm; }
.toc > ul > li { margin-top: 4mm; }
.toc .grp { font-family: Menlo, monospace; font-size: 9.5px; letter-spacing: .12em;
  text-transform: uppercase; color: #6d5f4a; border-top: 1px dashed #cbbfa3; padding-top: 2.5mm; }
.toc ul ul { margin: 1.5mm 0 0 6mm; }
.toc ul ul li { margin: 0.8mm 0; }
.toc a { display: block; }
.toc a::after { content: leader('.') "  " target-counter(attr(href), page);
  font-family: Menlo, monospace; font-size: 8.5px; color: #6d5f4a; }

/* части и документы */
h1.part { font-family: 'Russo One', 'Arial Black', sans-serif; font-size: 22pt;
  page-break-before: always; padding-top: 60mm; margin: 0 0 6mm; }
.part-note { color: #3d3428; max-width: 135mm; }
section.pdf-doc { page-break-before: always; }
.dochead { border-bottom: 2.5px solid #a8371f; padding-bottom: 2.5mm; margin-bottom: 5mm; }
.dochead .over { font-family: Menlo, monospace; font-size: 8.5px; letter-spacing: .16em;
  text-transform: uppercase; color: #a8371f; margin: 0 0 1.5mm; }
.dochead h2.dt { font-family: 'Russo One', 'Arial Black', sans-serif; font-size: 15pt; margin: 0; }
.dochead .doctype { font-family: Menlo, monospace; font-size: 8px; letter-spacing: .1em;
  text-transform: uppercase; color: #6d5f4a; border: 1px solid #6d5f4a; border-radius: 3px;
  padding: 0.5mm 2mm; }

/* тела документов */
.md h1 { font-family: 'Russo One', 'Arial Black', sans-serif; font-size: 13pt; margin: .4em 0 .5em; }
.md h2 { font-family: 'Russo One', 'Arial Black', sans-serif; font-size: 11.5pt;
  margin: 1.3em 0 .4em; padding-top: .6em; border-top: 1px dashed #cbbfa3; }
.md h3 { font-size: 11pt; margin: 1.1em 0 .3em; }
.md blockquote { margin: 1em 0; padding: .3em 1em; border-left: 3px solid #8a6d1f;
  background: #f5efe0; font-style: italic; }
.md code { font-family: Menlo, monospace; font-size: 8.5pt; background: #e6dcc4;
  padding: 0 1px; border-radius: 2px; }
.md pre { background: #211b13; color: #e9e0cb; border-left: 3px solid #a8371f;
  padding: 3mm 3.5mm; font-size: 7.6pt; line-height: 1.5; white-space: pre-wrap;
  border-radius: 2px; }
.md pre code { background: none; color: inherit; font-size: inherit; }
.md table { border-collapse: collapse; font-size: 8.8pt; margin: .8em 0; }
.md th, .md td { border: 0.6px solid #cbbfa3; padding: 1.2mm 2.2mm; text-align: left;
  vertical-align: top; }
.md th { background: #e6dcc4; font-family: Menlo, monospace; font-size: 7.6pt;
  letter-spacing: .05em; text-transform: uppercase; }
.md hr { border: 0; border-top: 1px solid #cbbfa3; margin: 1.5em 0; }
"""

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=PT+Serif:ital,wght@0,400;0,700;1,400'
         '&family=Russo+One&display=swap" rel="stylesheet">')

LINK_RX = re.compile(r'href="(?:\.\./)?(run-4|run-3|player)/([a-z0-9-]+)\.html(?:#[^"]*)?"')
DIR2KEY = {"run-4": "run4", "run-3": "run3", "player": "player"}


def relink(html: str) -> str:
    return LINK_RX.sub(lambda m: f'href="#{DIR2KEY[m.group(1)]}-{m.group(2)}"', html)


def md_body(path: pathlib.Path) -> str:
    MD.reset()
    return relink(MD.convert(path.read_text(encoding="utf-8")))


def player_summary() -> str:
    """Тело саммари фазы «Игрок» — из шаблона сайта."""
    tpl = (ROOT / "templates" / "player-index.html").read_text(encoding="utf-8")
    m = re.search(r'<article class="doc">(.*?)</article>', tpl, re.S)
    body = m.group(1)
    body = re.sub(r'href="([a-z0-9-]+)\.html"', r'href="#player-\1"', body)  # соседние документы
    return relink(body)


OVERVIEW = """
<section class="pdf-doc" id="overview">
<div class="dochead"><p class="over">Обзор</p><h2 class="dt">ГД-конвейер gd-pipeline</h2></div>
<div class="md">
<p><b>gd-pipeline</b> — экспериментальный конвейер из ИИ-агентов, который ищет и проверяет идеи игр.
Тестовая задача: одиночная премиум-игра «в духе Ticket to Ride» с роглайт-механиками.
В документе — два лучших прогона целиком, от брифа до вердиктов, без правок задним числом.</p>
<h2>Как устроен конвейер</h2>
<p>Пять ролей, каждая фаза оставляет отдельный документ. <b>Генератор</b> выдаёт 20 разнообразных
идей по заданным «линзам» (механики проверенных рынком игр). Оркестратор отбирает 3 кандидата,
<b>концептер</b> разворачивает каждого в карточку — описание игры языком рядового игрока.
<b>Критик</b> разбирает карточку на прочность: оценки 0–3 по аспектам, находки с контраргументами.
<b>Игрок</b> — симуляционная проверка: агент играет формализованную сцену концепта и меряет её
метриками. <b>Синтез</b> сводит всё в отчёт с жёстким правилом: ноль в фундаменте не
компенсируется ничем.</p>
<h2>Как читать документ</h2>
<p>Каждый прогон — раздел из документов в порядке работы конвейера: <b>бриф</b> → <b>пул идей</b> →
<b>отбор кандидатов</b> → <b>концепт-карточки A/B/C</b> → <b>вердикты критика A/B/C</b> →
<b>итоговый отчёт</b>. Быстрый способ понять прогон — начать с итогового отчёта: он открывается
блоком «Что за игра» и сводной таблицей оценок. Навигация — через панель закладок PDF-читалки
(дерево разделов слева) и кликабельное оглавление.</p>
<p>Статусы кандидатов: <b>GO</b> — фундамент цел, можно углублять; <b>GO с условиями</b> — цел,
но следующий шаг предписан; <b>REWORK</b> — найден блокер уровня ядра, нужна переработка.</p>
</div>
</section>
"""


def main():
    parts_html = [
        '<div class="title-page"><p class="over">Lost Levels · gd-pipeline</p>'
        "<h1>Результаты прогонов ГД-конвейера</h1>"
        "<p>Поиск и проверка идей игр «в духе Ticket to Ride» с роглайт-механиками: "
        "два лучших прогона и симуляционная проверка лидера фазой «Игрок».</p></div>"
    ]

    # оглавление (структура = сайдбар сайта)
    toc = ['<nav class="toc"><h1>Оглавление</h1><ul>']
    toc.append('<li><ul><li><a href="#overview">Обзор</a></li></ul></li>')
    for gkey, label, _src, docs in PARTS:
        toc.append(f'<li><div class="grp">{label}</div><ul>')
        if gkey == "player":
            toc.append('<li><a href="#player-index">Саммари пилота</a></li>')
        for _s, out, _h1, _dt in docs:
            stem = out[:-5]
            toc.append(f'<li><a href="#{gkey}-{stem}">{NAV_TITLES[gkey][out]}</a></li>')
        toc.append("</ul></li>")
    toc.append("</ul></nav>")
    parts_html.append("".join(toc))

    parts_html.append(OVERVIEW)

    for gkey, label, src_dir, docs in PARTS:
        parts_html.append(f'<h1 class="part" id="part-{gkey}">{label}</h1>')
        if gkey == "player":
            parts_html.append(
                '<section class="pdf-doc" id="player-index">'
                '<div class="dochead"><p class="over">Фаза «Игрок» — симуляция</p>'
                '<h2 class="dt">Саммари пилота</h2></div>'
                f'<div class="md">{player_summary()}</div></section>'
            )
        for src, out, h1, doctype in docs:
            stem = out[:-5]
            body = md_body(ROOT / "content" / src_dir / src)
            parts_html.append(
                f'<section class="pdf-doc" id="{gkey}-{stem}">'
                f'<div class="dochead"><p class="over">{label}</p>'
                f'<h2 class="dt">{h1}</h2> <span class="doctype">{doctype}</span></div>'
                f'<div class="md">{body}</div></section>'
            )

    html = (f'<!doctype html><html lang="ru"><head><meta charset="utf-8">{FONTS}'
            f"<style>{CSS}</style></head><body>{''.join(parts_html)}</body></html>")

    OUT.mkdir(exist_ok=True)
    (OUT / "print.html").write_text(html, encoding="utf-8")
    HTML(string=html, base_url=str(ROOT)).write_pdf(OUT / "gd-pipeline-results.pdf")
    print("OK:", OUT / "gd-pipeline-results.pdf")


if __name__ == "__main__":
    main()
