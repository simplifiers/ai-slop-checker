# AI Slop Checker

**AI Slop Checker für Deutsch und Englisch** (AI slop checker for German and English). Er prüft Fachartikel, Posts und Newsletter, die mit Hilfe eines Sprachmodells entstehen, auf fehlende Substanz, Behauptungen ohne Quelle, Floskeln und einen maschinellen Rhythmus. Reines Python ohne Abhängigkeiten, läuft offline. Der Befehl heißt `slop-check`.

[English version](README.md)

## Das Problem

Die meisten Werkzeuge gegen "AI Slop" suchen nach einer Liste von Wörtern und dem langen Gedankenstrich. Streicht man alles davon, kann der Text immer noch nichts sagen. Ein Absatz kann frei von jeder gelisteten Phrase sein und trotzdem zu jeder Firma, jedem Thema und jedem Leser passen.

Phrasen zu streichen reicht nicht. Was hilft, ist Substanz. Also eine Zahl aus deinen eigenen Daten, eine genannte Quelle, ein Schritt, den jemand nachmachen kann, oder ein Beispiel, das nur du kennst. slop-check sucht zuerst nach fehlender Substanz und erst danach nach Phrasen.

## Beispiel in 30 Sekunden

`entwurf.md`:

```
In der heutigen schnelllebigen Welt ist Content-Marketing wichtiger denn je.
Experten sind sich einig, dass Unternehmen mit klarer Strategie 73 % schneller wachsen.
Es geht nicht darum, mehr zu produzieren. Es geht darum, besser zu produzieren.
```

```
$ slop-check entwurf.md --lang de

slop-check 0.1.0  |  ZU KURZ FÜR EIN URTEIL  |  35 Wörter
Unter 120 Wörtern gibt es kein Gesamturteil, nur die einzelnen Funde.

== Substanz (FEHLER 2, AUFFÄLLIG 0, HINWEIS 0)
  [FEHLER] S-02 Vage Zuschreibung (Zeile 2)
      > Experten sind sich einig
      "Studien zeigen", "Experten sagen", "laut einer Umfrage": eine Autorität wird behauptet, aber nicht genannt.
      Tipp: Die Quelle nennen und verlinken oder den Satz als eigene Erfahrung formulieren.
  [FEHLER] S-01 Zahl ohne Quelle (Zeile 2)
      > 73 %
      Zahl „73 %“ ohne Quelle im selben Satz.
      Tipp: Quelle als Link oder (Quelle: Name) in denselben Satz setzen, die Zahl als eigene Erfahrung kennzeichnen oder streichen.

== Floskeln (FEHLER 0, AUFFÄLLIG 1, HINWEIS 0)
  [AUFFÄLLIG] P-01 In der heutigen (schnelllebigen) Welt (Zeile 1)
      > In der heutigen schnelllebigen Welt
      Floskel „In der heutigen schnelllebigen Welt“ (In der heutigen (schnelllebigen) Welt): Zeitdiagnose ohne Inhalt als Einstieg.
      Tipp: Streichen oder durch eine konkrete Aussage ersetzen.

== Struktur (FEHLER 0, AUFFÄLLIG 0, HINWEIS 1)
  [HINWEIS] T-01 Kontrast-Schablone (Zeile 3)
      > Es geht nicht darum, mehr zu produzieren. Es geht
      "Es geht nicht um X, sondern um Y" und ähnliche Gegenüberstellungen, die eine Position erfinden, nur um sie zu widerlegen. Einmal ist ein Hinweis, ab zwei ein Muster.
      Tipp: Die Gegenposition streichen und die eigene Aussage direkt begründen.

slop-check sagt nicht, ob eine KI einen Text geschrieben hat. Es zeigt Muster, die du prüfen kannst.
```

Zu jedem Befund zitiert slop-check die Stelle und schlägt eine Lösung vor. Unter 120 Wörtern gibt es nur die Befunde ohne Gesamturteil. Ein ganzer Artikel bekommt `pass` oder `revise`. Es schreibt deinen Text nicht um und erfindet das fehlende Detail nicht.

## Installation

Mit pip direkt von GitHub:

```
pip install git+https://github.com/simplifiers/ai-slop-checker
```

Mit pipx in einer eigenen Umgebung:

```
pipx install git+https://github.com/simplifiers/ai-slop-checker
```

Als Claude-Skill:

```
npx skills add simplifiers/ai-slop-checker
```

Der Skill bringt eine eigene Kopie des Prüfers mit. Claude braucht dafür nur Python 3.9 oder neuer. Beide Wege installieren den Befehl `slop-check` und denselben Befehl unter dem Namen `ai-slop-checker`.

Zur Installation von Hand `ai-slop-checker-skill.zip` von der Release-Seite laden und in deinen Skill-Ordner entpacken (bei Claude Code ist das `~/.claude/skills/`). Oder das Repository als ZIP laden und darin `python -m slopcheck` aufrufen.

## Nutzung

Eine Datei prüfen:

```
slop-check entwurf.md
```

Die Sprache vorgeben, wenn der Text kurz oder gemischt ist:

```
slop-check entwurf.md --lang de
```

Den Text mit den Notizen, dem Transkript oder dem Briefing vergleichen, aus dem er entstanden ist. slop-check listet Fakten aus der Quelle, die im Text fehlen, und Zahlen im Text, die in der Quelle nicht vorkommen:

```
slop-check entwurf.md --source interview-notizen.md
```

Einen Bericht schreiben, den du im Browser öffnen oder weitergeben kannst. Es ist eine einzelne HTML-Datei ohne externe Ressourcen:

```
slop-check entwurf.md --format html --out bericht.html
```

JSON für Skripte und Editoren:

```
slop-check entwurf.md --format json
```

Einen Build abbrechen, wenn ein Text Arbeit braucht:

```
slop-check entwurf.md --fail-on revise
```

`python -m slopcheck` funktioniert überall dort, wo `slop-check` funktioniert.

## Was geprüft wird

Befunde haben drei Stufen. `fail` heißt: vor der Veröffentlichung beheben. `tell` heißt: ein Muster, das für generierten Text typisch ist. `hint` heißt: ein zweiter Blick lohnt sich. Einzelne Wörter werden nur dann allein markiert, wenn sie für sich ein starkes Indiz sind. Schwächere zählen erst, wenn mehrere zusammenkommen.

| Kategorie | Wonach gesucht wird | Zwei Beispiele |
|---|---|---|
| Substanz | Text, der nach Inhalt klingt, aber keinen trägt | "Experten sind sich einig, dass ..." ohne genannten Experten. Ein Satz, der in jeden Artikel zu jedem Thema passt. |
| Fakten | Aussagen, die einen Beleg brauchen | Eine Prozentzahl oder Studie ohne Quelle. Eine Zahl aus deinen Notizen, die im Text verloren ging. |
| Phrasen | Abgegriffene Formulierungen | "In der heutigen schnelllebigen Welt". "Lass uns eintauchen." |
| Struktur | Wiederkehrende Formen | "Es geht nicht um X. Es geht um Y." Dreierlisten in jedem Absatz. |
| Rhythmus | Satz- und Absatzlänge, Wortschatz, Wortlänge, Dreierlisten und Doppelpunkte, gemessen an menschlichen Texten | Kurze Sätze in kurzen Absätzen. Synonyme so oft gewechselt, dass es gewollt wirkt. |
| Form | Typografie und Layout | Ein Emoji vor jedem Aufzählungspunkt. Der lange Gedankenstrich, als abschaltbare Stilregel. |

Alle Muster mit ID, schlechtem und besserem Beispiel: [docs/patterns.de.md](docs/patterns.de.md).

Genannte Personen stehen in einer eigenen Liste "zum Prüfen". slop-check kann nicht feststellen, ob eine zitierte Person existiert oder gesagt hat, was der Text behauptet. Das musst du prüfen.

Texte unter einer Mindestlänge bekommen das Urteil `too_short` statt einer Bewertung, weil die Messwerte bei wenigen Sätzen nicht verlässlich sind.

Das Urteil heißt `revise`, wenn es mindestens einen `fail` gibt, wenn Auffälligkeiten aus fünf oder mehr verschiedenen Mustern kommen oder wenn sechs oder mehr Rhythmus-Messwerte gleichzeitig auf der Seite generierter Texte liegen. Sonst heißt es `pass`. Hinweise zählen nie.

## Wie der Rhythmus-Check kalibriert ist

Neun Messwerte werden mit einem Band menschlicher Texte verglichen: Wörter je Satz, Streuung der Satzlängen, Wörter je Absatz, Wortvielfalt (MATTR), Buchstaben je Wort, Nominalstil, Dreierlisten, Doppelpunkte und, nur im Englischen, Partizip-Anhängsel wie ", ensuring". Das Band reicht vom 10. bis zum 90. Perzentil.

Für das öffentliche Band haben wir frei lizenzierte Nachrichtentexte von vor 2022 genommen, 157 deutsche und 162 englische Wikinews-Artikel. Zum Vergleich haben wir je Sprache 40 Blogartikel erzeugt. Ins Band kamen nur Messwerte, die in jedem gemessenen Register in dieselbe Richtung zeigen (Nachrichten, Bundestagsreden, Lexikonartikel). Vier oft genannte Verdächtige haben in unserer Messung menschliche und generierte Texte nicht getrennt und fehlen deshalb: Gedankenstriche, Passiv, Konnektoren am Satzanfang, Klammern.

Ein einzelner Wert außerhalb des Bands kommt bei Menschen oft vor und ist nur ein Hinweis. Ab sechs Werten auf der generierten Seite heißt das Urteil `revise`. Wir haben beim Aufbau des Bands jeden vierten Text zurückgehalten und die Regel an diesen getestet. Sie schlug bei 2 von 39 deutschen und 0 von 40 englischen Nachrichtenartikeln an, und bei 4 von 10 deutschen und 5 von 10 englischen generierten Artikeln (Quelle: das Feld `evaluation` in `slopcheck/bands/de-basic.json` und `en-basic.json`). Die Rhythmus-Regel erfasst nur einen Teil generierter Texte; den Rest übernehmen die anderen Prüfungen.

Es gibt eine Grenze. Alle Vergleichstexte stammen bisher von einem Modell. Andere Modelle und Aufträge können woanders landen. Nachrichten sind außerdem ein anderes Register als ein Fachblog, deshalb zählen einzelne Werte nur als Hinweis. Ein Band, das an echten Fachartikeln kalibriert ist, steckt in AI Editorial Team.

## Was es bewusst nicht tut

- Es ist kein KI-Detektor. Ein Befund sagt, dass eine Stelle allgemein oder unbelegt ist. Er sagt nichts darüber, wer oder was sie geschrieben hat, und ein Bericht ohne Befunde beweist nicht, dass ein Mensch den Text geschrieben hat.
- Es schreibt nicht um. Du bekommst Befunde mit Vorschlägen. Deine Stimme bleibt deine.
- Es prüft Personen und Zitate nicht gegen echte Quellen. Es listet sie auf, damit du es tun kannst.
- Es misst nicht, ob dein Text in KI-Suchen auftaucht.

Wenn du den ganzen Ablauf willst, mit Recherche, einem Interview zu deiner eigenen Erfahrung und automatischer Quellenprüfung: Dafür gibt es AI Redaktion (redaktion.ai) und einen kostenlosen Claude-Skill, der dich hindurchführt: https://app.redaktion.ai/lite?lang=de&ref=github

## Konfiguration

Lege eine `.slopcheck.json` neben deine Texte oder ins Projektverzeichnis:

```json
{
  "lang": "de",
  "address": "du",
  "allow": ["robuste Regression", "Hebelarm"],
  "forbid": ["Synergie", "ganzheitlich"],
  "disable": ["T-02"],
  "own_names": ["Erika Mustermann"],
  "sources": ["notizen/interview.md"],
  "fail_on": "revise"
}
```

| Schlüssel | Bedeutung |
|---|---|
| `lang` | `de` oder `en`. Ohne Angabe erkennt slop-check die Sprache. |
| `address` | Nur Deutsch: `du` oder `sie`. Die andere Form ist dann ein harter Fund. Ohne Angabe wird eine Mischung markiert. |
| `allow` | Begriffe, die nie als Floskel gemeldet werden, etwa Fachbegriffe. |
| `forbid` | Zusätzliche Wörter, die du in deinen Texten nie willst. |
| `disable` | Muster-IDs, die abgeschaltet werden. |
| `own_names` | Dein Name und die deiner Kollegen, damit sie nicht unter "zum Prüfen" landen. |
| `emojis` | `allow`, `limit` oder `no`. |
| `dashes` | Stilregel für den langen Gedankenstrich: `tell` (Standard), `fail` oder `off`. Viele Leser empfinden lange Gedankenstriche als KI-typisch, in unserer Messung trennen sie menschliche und generierte Texte aber nicht. |
| `sources` | Quelldateien für den Fakten-Abgleich, wie `--source`. |
| `fail_on` | `revise`, um mit Code 1 zu enden, wenn ein Text Arbeit braucht. |

Optionen auf der Kommandozeile gehen vor. Mit `--config DATEI` liegt die Konfiguration woanders.

## GitHub Action

Markdown bei jedem Pull Request prüfen:

```yaml
name: Textqualität
on: pull_request
jobs:
  slop-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: simplifiers/ai-slop-checker@main
        with:
          paths: content/blog/*.md
          lang: de
          fail-on: revise
```

## Mitwirken

Die Muster liegen in `slopcheck/patterns/de.json` und `slopcheck/patterns/en.json`, ein Katalog je Sprache. Jeder Eintrag hat `id`, `name`, `description`, `bad` und `better`. Das bessere Beispiel darf keine Fakten ergänzen, die im schlechten fehlen. Wo ein echtes Detail nötig ist, steht ein Platzhalter wie `[Zahl aus deinen Daten]`. Meldungen über Fehlalarme helfen genauso: Öffne ein Issue mit dem Satz, der ihn ausgelöst hat.

Dieses README wird in der CI von slop-check geprüft. Wenn eine Änderung es durchfallen lässt, wird das README korrigiert, nicht die Prüfung. Details in [CONTRIBUTING.md](CONTRIBUTING.md).

## Danksagung

Diese Projekte haben die Ideen hinter slop-check geprägt. Wortlaut wurde nicht übernommen.

- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)
- [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop)
- [FeedHive/ai-slop-detector](https://github.com/FeedHive/ai-slop-detector)
- [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop)
- [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill)
- [ilien-dev/quiron](https://github.com/ilien-dev/quiron)
- Der Wikipedia-Leitfaden [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

Das Rhythmus-Band enthält Statistiken aus Artikeln von [Wikinews](https://www.wikinews.org/) (Autorinnen und Autoren von Wikinews, Lizenz [CC BY 2.5](https://creativecommons.org/licenses/by/2.5/)). Es enthält keinen Text aus Wikinews, nur Perzentile.

## Lizenz

MIT. Siehe [LICENSE](LICENSE).
