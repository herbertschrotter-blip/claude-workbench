// Erzeugt das Theme der Mockups aus den Stilen der App. Vorlage für Lit: Pfade und Stile an das Projekt anpassen, Dateien
// als Mockup.Theme ins Skill-Profil. Kann ein Stack das nicht, liegt das Theme von Hand gepflegt in einer Datei (ohne Befehl).
// Aufruf: node tools/mockup_theme.mjs – nach jeder Änderung an den Stilen.
import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const wurzel = join(dirname(fileURLToPath(import.meta.url)), '..');
const { stil } = await import(join(wurzel, 'src/stil.js')); // anpassen: Modul mit den Stilen der App

const css = (x) => (Array.isArray(x) ? x.map(css).join('\n') : x.cssText);
const kopf = '/* Erzeugt von tools/mockup_theme.mjs aus den Stilen der App – nicht von Hand ändern. */\n';

writeFileSync(join(wurzel, 'mockups/theme-app.css'), kopf + css(stil));
