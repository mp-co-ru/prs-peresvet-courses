"""Базовый курс лежит в 01.base и ссылается на опубликованный справочник."""

import re
from pathlib import Path
from xml.dom import minidom


ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "01.base"
MANUAL = "https://mp-co-ru.github.io/peresvet/"


def test_base_course_pages():
    page = (COURSE / "index.html").read_text(encoding="utf-8")
    lessons = [(COURSE / f"lesson-0{n}.html").read_text(encoding="utf-8") for n in (1, 2, 3)]
    install, tags, objects = lessons
    assert "Курс по платформе" in page
    assert "НС-1" in page
    assert "Главная задача платформы — создание модели объекта" in page
    assert "В платформе параметр называется <b>тегом</b>" in page
    first_tag = page.index("тег", page.index("<header"))
    assert first_tag > page.index("В платформе параметр называется")
    assert "пересекает порог" not in page
    assert page.index("<h2>Модель объекта</h2>") < page.index("<h2>Область применения</h2>") < page.index("<h2>Что даёт платформа</h2>")
    assert "Промышленная автоматизация" in page.replace("&shy;", "")
    intro = page[page.index('<details class="intro">'):page.index("</details>\n      </div>\n    </section>")]
    assert "<summary><h2>Введение</h2>" in intro
    for title in ("Модель объекта", "Область применения", "Что даёт платформа", "Чему научитесь", "С чего можно начинать"):
        assert f"<h2>{title}</h2>" in intro
    assert "<h2>Программа</h2>" not in intro
    assert '<details class="intro" open' not in page
    assert "./run_one_app.sh" in install
    assert "PRS_SSL" not in install and "PRS_REGISTRY_MIRROR" not in install
    assert install.count('<section class="step">') <= 4
    for html in lessons:
        assert '<div class="outcome">' in html and "Результат урока" in html
        deeper = html[html.index('<aside class="deeper">'):html.index("</aside>")]
        assert "В расширенном курсе" in deeper and f'href="{MANUAL}' in deeper
    assert "базовый курс" in page
    assert "режимы HTTPS" not in page and "что нужно заранее" not in page
    assert "Новый объект" not in install and "Новый тег" not in install
    assert "Записать данные" in tags and "корень «Теги»" in tags
    assert "Новый объект" not in tags
    assert "Новый объект" in objects and "Перетащите" in objects
    program = page[page.index('<ol class="path">'):page.index("</ol>", page.index('<ol class="path">'))]
    assert program.count("<details>") == 13
    assert program.count('class="chev"') == 13
    for n in (1, 2, 3):
        assert f'href="lesson-0{n}.html"' in program
    first = program[:program.index("</details>")]
    assert "Установка платформы" in first and 'href="lesson-01.html"' in first
    second = program[program.index("</details>"):program.index("</details>", program.index("</details>") + 1)]
    assert "список тегов" in second
    assert "Лампочка" not in page
    for html in (page, *lessons):
        assert 'href="https://matchpoint-consulting.ru/"' in html
        assert "© 2023-2026" in html
        assert "ООО «МПК»" in html
        assert 'src="pics/mpc-logo.svg"' in html
        assert 'href="tel:+74993930040"' in html
        assert 'href="mailto:info@mp-co.ru"' in html
        assert 'href="../' not in html
    grow = (COURSE / "pics" / "grow.svg").read_text(encoding="utf-8")
    assert "Цех" in grow
    assert "От простого объекта" not in grow
    cards = page.count('<article class="card">')
    pictures = re.findall(r'<svg class="card-icon"><use href="#(icon-[a-z]+)">', page)
    assert cards and len(pictures) == cards
    assert len(set(pictures)) == cards
    for name in ("logo.svg", "mpc-logo.svg", "grow.svg", "station.svg", "tree.svg", "point.svg", "tags.svg"):
        assert (COURSE / "pics" / name).is_file()


def test_base_course_pictures_are_valid_utf8_svg():
    pics = COURSE / "pics"
    svgs = sorted(pics.glob("*.svg"))
    assert svgs
    for svg in svgs:
        minidom.parseString(svg.read_bytes().decode("utf-8"))
    assert "Давление" in (pics / "tags.svg").read_text(encoding="utf-8")


def test_base_course_links_to_the_published_manual():
    for html in COURSE.glob("*.html"):
        for href in re.findall(r'href="(https://mp-co-ru\.github\.io/peresvet/[^"]+)"', html.read_text(encoding="utf-8")):
            assert href.startswith(MANUAL)
            assert href.removeprefix(MANUAL).endswith(".html")
