// Gemeinsame Bausteine der Mockups je Seite: Vorführleiste (Nummer, Version, Ansichten, Zustände), Version unten links und Wechsel zwischen den
// Seiten. Eine Seite ruft Mockup.start({ nr, titel, version, zustaende, zeige(s) }) auf. Bausteine, die mehrere Seiten
// nutzen, kommen hierher, nie in eine Seite. ANSICHTEN aus Mockup.Ansichten des Skill-Profils eintragen; die Pfade `seiten/` und
// `../index.html` gelten für Seiten unter <Ablage>/seiten/ neben der Seitenliste.
(() => {
  const ANSICHTEN = [['d', 'Desktop', 1100], ['h', '390 px', 390]];
  const rahmen = document.createElement('style');
  rahmen.textContent = `
    html, body { margin: 0; background: #1a1a1a; color: #ddd; font-family: -apple-system, system-ui, "Segoe UI", Roboto, sans-serif; }
    .vorf { display: flex; flex-wrap: wrap; gap: 8px 14px; align-items: center; padding: 10px 16px; font-size: 13px; background: #111; border-bottom: 1px solid #333; }
    .vorf a { color: #64a8ff; text-decoration: none; }
    .vorf .gruppe { display: inline-flex; flex-wrap: wrap; gap: 4px; align-items: center; }
    .vorf button { font: inherit; font-size: 12px; background: #2a2a2a; color: #ddd; border: 1px solid #444; border-radius: 8px; padding: 4px 9px; cursor: pointer; }
    .vorf button.on { background: #3987e5; border-color: #3987e5; color: #fff; }
    .buehne { display: flex; justify-content: center; padding: 16px; }
    .rahmen { width: 100%; height: 800px; border-radius: 18px; overflow: hidden; border: 1px solid #333; position: relative; transform: translateZ(0); }
    .vnr { position: absolute; left: 10px; bottom: 6px; z-index: 50; padding: 1px 6px; border-radius: 5px; font-size: 11px; color: #fff; background: rgba(0, 0, 0, .55); pointer-events: none; }`;
  document.head.appendChild(rahmen);

  let s = {}, opt = {};
  const setz = (k, v) => { s[k] = v; zeigen(); };
  const gehe = (seite) => `Mockup.geh('${seite}')`;

  // In der Seitenliste läuft das Mockup in deren Fenster: dann gehen Wechsel über sie
  const eingebettet = window.parent !== window;
  const geh = (seite) => { if (eingebettet) window.parent.postMessage({ mockup: `seiten/${seite}.html` }, '*'); else location.href = `${seite}.html`; };

  function zeigen() {
    const r = document.getElementById('rahmen');
    r.style.maxWidth = `${ANSICHTEN.find(([k]) => k === s.ansicht)[2]}px`;
    r.innerHTML = `${opt.zeige(s)}<div class="vnr">${opt.nr} v${opt.version}</div>`;
    document.querySelectorAll('.vorf button').forEach((b) => b.classList.toggle('on', s[b.dataset.k] === b.dataset.w));
  }

  function start(o) {
    opt = o;
    s = { ansicht: ANSICHTEN[ANSICHTEN.length - 1][0], z: (o.zustaende || [[]])[0]?.[0], ...o.start };
    document.title = `${o.nr} ${o.titel}`;
    const knopf = (k) => ([w, t]) => `<button data-k="${k}" data-w="${w}">${t}</button>`;
    const z = (o.zustaende || []).map(knopf('z')).join('');
    document.body.innerHTML = `<div class="vorf">${eingebettet ? '' : '<a href="../index.html">‹ Seitenliste</a>'}<b>${o.nr} ${o.titel}</b><span>Version ${o.version}</span>
      <span class="gruppe">${ANSICHTEN.map(knopf('ansicht')).join('')}</span>
      ${z ? `<span class="gruppe">${z}</span>` : ''}</div><div class="buehne"><div class="rahmen" id="rahmen"></div></div>`;
    document.querySelectorAll('.vorf button').forEach((b) => { b.onclick = () => setz(b.dataset.k, b.dataset.w); });
    zeigen();
  }

  window.Mockup = { start, setz, gehe, geh };
})();
