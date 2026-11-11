// Кнопка «Копировать» для блоков с командами консоли (<pre class="cmd">).
// В буфер попадает только текст команд: символ приглашения «$» не копируется.
(function () {
  var ICON_COPY = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 0 1 2-2h9"/></svg>';
  var ICON_DONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';

  function commandText(pre) {
    var lines = pre.querySelectorAll('.line');
    var out = [];
    lines.forEach(function (line) {
      var clone = line.cloneNode(true);
      clone.querySelectorAll('.prompt').forEach(function (p) { p.remove(); });
      out.push(clone.textContent);
    });
    return out.join('\n');
  }

  function fallbackCopy(text) {
    var area = document.createElement('textarea');
    area.value = text;
    area.setAttribute('readonly', '');
    area.style.position = 'fixed';
    area.style.opacity = '0';
    document.body.appendChild(area);
    area.select();
    try { document.execCommand('copy'); } catch (e) { /* ничего не делаем */ }
    document.body.removeChild(area);
  }

  function copy(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).catch(function () { fallbackCopy(text); });
    }
    fallbackCopy(text);
    return Promise.resolve();
  }

  document.querySelectorAll('pre.cmd').forEach(function (pre) {
    var wrap = document.createElement('div');
    wrap.className = 'cmd-wrap';
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy-btn';
    btn.title = 'Копировать команду';
    btn.setAttribute('aria-label', 'Копировать команду');
    btn.innerHTML = ICON_COPY;
    wrap.appendChild(btn);

    var timer = null;
    btn.addEventListener('click', function () {
      copy(commandText(pre)).then(function () {
        btn.innerHTML = ICON_DONE;
        btn.classList.add('done');
        btn.title = 'Скопировано';
        clearTimeout(timer);
        timer = setTimeout(function () {
          btn.innerHTML = ICON_COPY;
          btn.classList.remove('done');
          btn.title = 'Копировать команду';
        }, 1500);
      });
    });
  });
})();
