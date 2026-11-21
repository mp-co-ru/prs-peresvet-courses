"""Базовый курс лежит в 01.base и ссылается на опубликованный справочник."""

import re
from pathlib import Path
from xml.dom import minidom


ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "01.base"
ADVANCED = ROOT / "02.advanced"
MANUAL = "https://mp-co-ru.github.io/peresvet/"


def test_base_course_pages():
    page = (COURSE / "index.html").read_text(encoding="utf-8")
    lessons = [(COURSE / f"lesson-0{n}.html").read_text(encoding="utf-8") for n in range(1, 10)]
    install, tags, objects, power, alarm, feed, schedule, camera, screen = lessons
    assert "Курс по платформе" in page
    assert "Насосная станция" in page
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
    prep = page[page.index('<section id="prep"'):page.index('<section id="program">')]
    assert '<details class="intro">\n          <summary><h2>Подготовка</h2>' in prep
    assert "<h2>Виртуальная машина</h2>" in prep and "<h2>Что нужно знать</h2>" in prep
    for skill, link in (("Формат JSON", "https://www.json.org/"), ("Основы JSONata", "https://jsonata.org/"), ("Python", "https://docs.python.org/")):
        assert skill in prep and link in prep
    assert "JSONPath" in prep
    optional = page[page.index('<div class="k">Не обязательно</div>'):]
    assert "Python" not in optional[:optional.index("</article>")]
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
    assert "Новый метод" in power and "pump.power" in power
    assert '@rpc("pump.power")' in power and 'project="methods_app"' in power
    assert "https://github.com/Vovaman/prs-methods-core" in power and "launch.json" in power
    addon = power[power.index('<details class="addon">'):]
    main_path = power[:power.index('<details class="addon">')]
    assert "launch.json" in addon and "pip install" in addon
    assert "launch.json" not in main_path and "pip install -e" not in main_path
    assert main_path.index('<section class="check">') < power.index('<details class="addon">')
    assert "Новая тревога" in alarm and "<strong>Тревоги</strong>" in alarm and "Квитировать" in alarm
    assert "Активна, квитирована" in alarm and "Пропала, не квитирована" in alarm
    assert "/v1/alarms/" not in alarm
    assert "«Старт»" in alarm and "«Финиш»" in alarm and "«Квитирование»" in alarm
    assert "Цех→Насосы→Насос→Уровень" in alarm and "<code>acked</code>" not in alarm
    assert 'src="pics/alarm.svg"' in alarm
    for n in range(1, 12):
        assert f'src="pics/05-lesson-{n:02d}.png"' in alarm
    assert "<h2>История тревоги</h2>" in alarm and "Данные тревоги" in alarm
    for key in ("parentId", "getChildren", "fired", "format", "count"):
        assert f"<code>{key}</code>" in alarm
    assert "только у узлов с красным кружком" not in alarm and "обновляет его каждые" not in alarm
    assert "Отсутствие источника данных - не ошибка" in install
    for html in lessons:
        assert "Получить данные" not in html
    assert "Читать данные" in tags and "Читать данные" in alarm
    assert "POST /v1/data/" in feed and "simulator.py" in feed
    assert "pump.avg_power" in schedule and "Каждую минуту" in schedule and "timeStep" in schedule
    assert "Сохранить в CSV" in schedule
    alarm_addon = schedule[schedule.index('<span class="t">Метод по тревоге</span>'):]
    assert '@rpc("pump.count")' in alarm_addon and "<strong>Срабатывание</strong>" in alarm_addon
    for n in range(1, 9):
        assert f'src="pics/07-lesson-0{n}.png"' in schedule
    assert "rtspUrl" in camera and "Видеопоток" in camera and "Видеоархив" in camera
    assert "Живой поток" in camera and "Снимок" in camera and "Фрагмент" in camera
    for n in range(6, 9):
        assert f'src="pics/08-lesson-0{n}.png"' in camera
    assert "откройте её в новой вкладке" not in camera
    for button in ("Ближе", "Домой", "Стоп", "Микрофон", "Зона"):
        assert f"<strong>{button}</strong>" in camera
    assert "Камера не отвечает по OnVif." in camera
    assert "$__isoFrom()" in screen and "/alarms/" in screen and "${__to:date:iso}" in screen
    assert "<strong>peresvet</strong>" in screen and "Тестирование" in screen
    assert "«Пересвет»" not in screen and "JSON API: Not Found" not in screen
    for html in (alarm, feed, schedule, camera, screen):
        assert "curl " not in html
    for n, html in enumerate(lessons, start=1):
        if n > 1:
            assert f'href="lesson-0{n - 1}.html"' in html
        if n < 9:
            assert f'href="lesson-0{n + 1}.html"' in html
        for src in re.findall(r'src="(pics/[^"]+)"', html):
            assert (COURSE / src.replace("%20", " ")).is_file(), src
    for n in range(1, 9):
        assert f'src="pics/04-lesson-0{n}.png"' in power
        assert (COURSE / "pics" / f"04-lesson-0{n}.png").is_file()
    assert 'href="lesson-04.html"' in objects
    program = page[page.index('<ol class="path">'):page.index("</ol>", page.index('<ol class="path">'))]
    assert program.count("<details>") == 9
    assert program.count('class="chev"') == 9
    for n in range(1, 10):
        assert f'href="lesson-0{n}.html"' in program
    assert 'class="later"' not in program and "Урок готовится" not in program
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
        for href in re.findall(r'href="(\.\./[^"]*)"', html):
            assert href.startswith("../02.advanced/"), href
    grow = (COURSE / "pics" / "grow.svg").read_text(encoding="utf-8")
    assert "Цех" in grow
    assert "От простого объекта" not in grow
    cards = page.count('<article class="card">')
    pictures = re.findall(r'<svg class="card-icon"><use href="#(icon-[a-z]+)">', page)
    assert cards and len(pictures) == cards
    assert len(set(pictures)) == cards
    for name in ("logo.svg", "mpc-logo.svg", "grow.svg", "station.svg", "tree.svg", "point.svg", "tags.svg", "power.svg", "alarm.svg"):
        assert (COURSE / "pics" / name).is_file()


def test_base_course_pictures_are_valid_utf8_svg():
    pics = COURSE / "pics"
    svgs = sorted(pics.glob("*.svg"))
    assert svgs
    for svg in svgs:
        minidom.parseString(svg.read_bytes().decode("utf-8"))
    assert "Давление" in (pics / "tags.svg").read_text(encoding="utf-8")


def test_advanced_course_program_and_links_from_base():
    page = (ADVANCED / "index.html").read_text(encoding="utf-8")
    ids = re.findall(r'<li id="(lesson-\d\d)" class="later">', page)
    assert ids == [f"lesson-{n:02d}" for n in range(1, len(ids) + 1)] and len(ids) == 15
    assert f"<li>{len(ids)} тем</li>" in page
    assert page.count('<p class="from">') == len(ids)
    assert '<summary><h2>Подготовка</h2>' in page and "Пройден базовый курс" in page
    for href in re.findall(r'href="(\.\./[^"]*)"', page):
        assert href.startswith("../01.base/"), href
        assert (ADVANCED / href.split("#")[0]).is_file(), href
    for src in re.findall(r'(?:src|href)="((?:pics/|course\.)[^"]+)"', page):
        assert (ADVANCED / src).is_file(), src
    for needle in ('href="https://matchpoint-consulting.ru/"', "© 2023-2026", 'href="tel:+74993930040"', 'href="mailto:info@mp-co.ru"'):
        assert needle in page
    for html_path in [COURSE / "index.html", *sorted(COURSE.glob("lesson-0*.html"))]:
        html = html_path.read_text(encoding="utf-8")
        for anchor in re.findall(r'href="\.\./02\.advanced/index\.html#([^"]+)"', html):
            assert anchor in ids, (html_path.name, anchor)
    for n in range(1, 10):
        html = (COURSE / f"lesson-0{n}.html").read_text(encoding="utf-8")
        deeper = html[html.index('<aside class="deeper">'):html.index("</aside>")]
        for item in re.findall(r"<li>(.*?)</li>", deeper, re.S):
            assert item.startswith('<a href="../02.advanced/index.html#lesson-'), (n, item)
    assert 'href="../02.advanced/index.html"' in (COURSE / "index.html").read_text(encoding="utf-8")


def test_base_course_links_to_the_published_manual():
    for html in [*COURSE.glob("*.html"), *ADVANCED.glob("*.html")]:
        for href in re.findall(r'href="(https://mp-co-ru\.github\.io/peresvet/[^"]+)"', html.read_text(encoding="utf-8")):
            assert href.startswith(MANUAL)
            assert href.removeprefix(MANUAL).endswith(".html")
