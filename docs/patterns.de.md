# Muster

[English version](patterns.md)

<!-- Diese Seite wird von `scripts/build_docs.py` aus `slopcheck/patterns/*.json` erzeugt. Bitte die JSON-Dateien bearbeiten, nicht diese Seite. -->

Jedes Muster hat eine ID, einen kurzen Namen, eine Beschreibung und zwei Beispiele. Das bessere Beispiel ergänzt nie Fakten, die im schlechten fehlen. Wo ein echtes Detail nötig ist, steht ein Platzhalter in eckigen Klammern.

## Inhalt

- [Substanz](#substanz) (8 Muster)
- [Fakten](#fakten) (3 Muster)
- [Phrasen](#phrasen) (73 Muster)
- [Struktur](#struktur) (9 Muster)
- [Rhythmus](#rhythmus) (10 Muster)
- [Form](#form) (9 Muster)

## Substanz

Stellen, die nach Inhalt klingen, aber keinen tragen: vage Zuschreibungen, Sätze, die in jeden Artikel zu jedem Thema passen, Rat ohne Schritte, glattgebügelte Einzelheiten. Diese Kategorie zählt am meisten.

### S-01 Zahl ohne Quelle

Stufe: `fail`

Prozente, Anteile, Beträge, große Zahlen oder Vielfache ohne Quelle im selben Satz. Maße, Jahreszahlen, Versionen, Paragraphen und Uhrzeiten zählen nicht.

**Schlecht:**

> 73 % der Kunden lesen Bewertungen vor dem Kauf.

**Besser:**

> Ein Link zur Erhebung im selben Satz, oder: Bei uns fragen [deine Zahl aus eigener Erfahrung] von zehn Kunden zuerst nach Bewertungen.

**Vorschlag:** Quelle als Link oder (Quelle: Name) in denselben Satz setzen, die Zahl als eigene Erfahrung kennzeichnen oder streichen.

### S-02 Vage Zuschreibung

Stufe: `fail`

"Studien zeigen", "Experten sagen", "laut einer Umfrage": eine Autorität wird behauptet, aber nicht genannt.

**Schlecht:**

> Studien zeigen, dass kurze Texte besser funktionieren.

**Besser:**

> Nenne die Studie mit Link, oder schreibe, was du selbst beobachtet hast: [deine Beobachtung].

**Vorschlag:** Die Quelle nennen und verlinken oder den Satz als eigene Erfahrung formulieren.

### S-03 Person ohne Quelle

Stufe: `tell`

Eine namentlich genannte Person wird zitiert oder paraphrasiert, ohne Quelle im Satz. Prüfe, ob es die Person gibt und ob sie das gesagt hat.

**Schlecht:**

> Thomas Weber, Marketingexperte, sagt: "Content ist alles."

**Besser:**

> [Name] sagte im Gespräch mit uns am [Datum]: "[wörtliches Zitat]" oder ein Link zur Originalquelle.

**Vorschlag:** Link zur Originalquelle ergänzen oder die Person streichen. Eigene Namen per Konfiguration own_names freigeben.

### S-04 Austauschbarer Absatz

Stufe: `hint`

Ein längerer Absatz ohne jedes konkrete Detail: keine Zahl, kein Name, kein Ort, kein Datum, kein Beispiel, keine eigene Erfahrung. Er könnte in jedem Text zum Thema stehen.

**Schlecht:**

> Gute Kommunikation ist die Basis jeder Zusammenarbeit. Wer klar kommuniziert, vermeidet Missverständnisse und schafft Vertrauen.

**Besser:**

> Ergänze ein Detail, das nur du kennst: [ein Fall aus deiner Arbeit, mit Ort oder Zeitpunkt].

**Vorschlag:** Ein konkretes Detail aus eigener Erfahrung ergänzen oder den Absatz streichen.

### S-05 Wenig Konkretes

Stufe: `tell`

Über den ganzen Text gerechnet kommen auf 100 Wörter sehr wenige konkrete Angaben (Zahlen, Namen, Daten, Beispiele, eigene Erfahrung). Grenze vorläufig.

**Schlecht:**

> Ein ganzer Artikel aus allgemeinen Ratschlägen.

**Besser:**

> Pro Abschnitt mindestens ein Beispiel aus deiner Praxis: [Fall], [Zeitraum], [Ergebnis].

**Vorschlag:** Mehr eigene Fälle, Zahlen mit Quelle und Beispiele einbauen.

### S-06 Rat ohne Schritte

Stufe: `tell`

Ein Absatz häuft Aufforderungen ("du solltest", "achte darauf"), nennt aber weder Schritte noch ein Beispiel.

**Schlecht:**

> Du solltest deine Zielgruppe kennen. Du solltest regelmäßig posten. Achte auf Qualität.

**Besser:**

> Eine nummerierte Liste mit den Schritten, die du selbst gehst, und einem Beispiel: [Schritt 1], [Schritt 2].

**Vorschlag:** Den Rat in Schritte zerlegen oder ein Beispiel aus der Praxis ergänzen.

### S-07 Geglättetes Detail

Stufe: `tell`

Ein konkretes Detail wird durch eine vage Größe ersetzt: "ein führender Anbieter", "namhafte Unternehmen", "zahlreiche Kunden".

**Schlecht:**

> Ein führender Anbieter setzt die Methode bereits ein.

**Besser:**

> Nenne den Anbieter, wenn du darfst, oder beschreibe ihn: [Branche], [Größe], [was er damit macht].

**Vorschlag:** Den Namen nennen oder das Detail beschreiben, das den Fall besonders macht.

### S-08 Zahl aus eigener Erfahrung

Stufe: `hint`

Eine Zahl in einem Ich- oder Wir-Satz. Das kann eigene Erfahrung sein. Prüfe, ob sie stimmt und ob du sie belegen könntest.

**Schlecht:**

> Wir haben die Kosten um 40 % gesenkt.

**Besser:**

> Wir haben die Kosten von [Betrag] auf [Betrag] gesenkt, gemessen über [Zeitraum].

**Vorschlag:** Zeitraum und Messgröße ergänzen.

## Fakten

Zahlen, Studien und genannte Personen, die einen Beleg brauchen, und Fakten aus deinen Notizen, die auf dem Weg in den Text verloren gingen.

### S-11 Fakt aus der Quelle fehlt

Stufe: `tell`

Eine Zahl, ein Datum, ein Name oder ein Link steht in deinen Notizen, aber nicht im Entwurf.

**Schlecht:**

> Notizen: 15.000 Abonnenten. Entwurf: viele Abonnenten.

**Besser:**

> Übernimm die Angabe aus den Notizen, wenn sie für den Leser zählt.

**Vorschlag:** Prüfen, ob die Angabe absichtlich weggefallen ist.

### S-12 Neue Zahl oder neuer Link ohne Beleg

Stufe: `fail`

Eine Zahl oder ein Link steht im Entwurf, aber in keiner Quelle, und der Satz hat keinen Beleg. Typisch für erfundene Angaben.

**Schlecht:**

> Notizen: keine Zahl. Entwurf: 73 % der Leser bleiben länger.

**Besser:**

> Nimm nur Zahlen auf, die in deinen Notizen stehen, oder ergänze die Quelle.

**Vorschlag:** Angabe prüfen und belegen oder streichen. Links öffnen und prüfen, ob sie die Aussage tragen.

### S-13 Neuer Name oder neues Datum

Stufe: `tell`

Ein Name oder Datum steht im Entwurf, aber in keiner Quelle.

**Schlecht:**

> Notizen: ein Kunde aus Leipzig. Entwurf: Kundin Maria Hofmann aus Leipzig.

**Besser:**

> Bleib bei der Angabe aus den Notizen: [wie in den Notizen].

**Vorschlag:** Prüfen, ob der Name oder das Datum stimmt.

## Phrasen

Formulierungen, die in generiertem Text deutlich häufiger vorkommen als in redigierten Texten. Starke Einzelwörter werden allein markiert, schwächere nur gehäuft.

### P-01 In der heutigen (schnelllebigen) Welt

Stufe: `tell`

Zeitdiagnose ohne Inhalt als Einstieg.

**Schlecht:**

> In der heutigen schnelllebigen Welt zählt jede Minute.

**Besser:**

> Seit [Monat/Jahr] beantworten wir Anfragen innerhalb von [deine Zeitspanne].

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-02 Im digitalen Zeitalter

Stufe: `tell`

Epochen-Floskel statt konkretem Anlass.

**Schlecht:**

> Im digitalen Zeitalter ändert sich alles.

**Besser:**

> Seit [konkrete Änderung] müssen Teams [konkrete Folge].

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-03 In einer Welt, in der

Stufe: `tell`

Großer Rahmen, der vom eigentlichen Punkt ablenkt.

**Schlecht:**

> In einer Welt, in der Daten alles sind, ...

**Besser:**

> Beginne mit dem Problem, das deine Leser heute haben.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-04 Mehr denn je

Stufe: `tell`

Steigerung ohne Vergleichsgröße.

**Schlecht:**

> Sichtbarkeit ist heute wichtiger denn je.

**Besser:**

> Nenne, was sich geändert hat und seit wann.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-05 Es ist wichtig zu beachten

Stufe: `tell`

Ankündigung statt Aussage.

**Schlecht:**

> Es ist wichtig zu beachten, dass Backups Zeit brauchen.

**Besser:**

> Backups brauchen Zeit: plane [deine Dauer] dafür ein.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-06 Es ist kein Geheimnis

Stufe: `tell`

Behauptet Allgemeinwissen, statt es zu zeigen.

**Schlecht:**

> Es ist kein Geheimnis, dass Kunden Bewertungen lesen.

**Besser:**

> Kunden lesen Bewertungen: [deine Beobachtung, z. B. was sie zuerst fragen].

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-07 Tauchen wir ein

Stufe: `tell`

Reisemetapher als Übergang.

**Schlecht:**

> Tauchen wir tiefer in das Thema ein.

**Besser:**

> Streiche den Satz und beginne direkt mit dem ersten Punkt.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-08 Willkommen in der Welt von

Stufe: `tell`

Begrüßungsformel statt Einstieg.

**Schlecht:**

> Willkommen in der Welt des E-Mail-Marketings!

**Besser:**

> Beginne mit der Frage, die deine Leser hergeführt hat.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-09 Stell dir vor

Stufe: `tell`

Erfundenes Szenario als Aufhänger.

**Schlecht:**

> Stell dir vor, dein Shop verkauft im Schlaf.

**Besser:**

> Erzähle einen echten Fall: [was einem deiner Kunden passiert ist].

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-10 In diesem Artikel erfährst du

Stufe: `tell`

Inhaltsangabe statt Inhalt.

**Schlecht:**

> In diesem Artikel erfährst du alles über Steuern.

**Besser:**

> Sag im ersten Satz die wichtigste Antwort.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-11 Spielt eine entscheidende Rolle

Stufe: `tell`

Wichtigkeit behauptet, nicht erklärt.

**Schlecht:**

> Die Ladezeit spielt eine entscheidende Rolle.

**Besser:**

> Sag, was passiert, wenn die Ladezeit steigt: [deine Beobachtung].

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-12 Von entscheidender Bedeutung

Stufe: `tell`

Wichtigkeits-Etikett ohne Begründung.

**Schlecht:**

> Datenschutz ist von zentraler Bedeutung.

**Besser:**

> Datenschutz entscheidet hier über [konkrete Folge].

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-13 Der Schlüssel zum Erfolg

Stufe: `tell`

Erfolgsversprechen ohne Inhalt.

**Schlecht:**

> Konsistenz ist der Schlüssel zum Erfolg.

**Besser:**

> Nenne, was Konsistenz in deinem Fall konkret bewirkt hat.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-14 Das volle Potenzial ausschöpfen

Stufe: `tell`

Potenzial-Rhetorik ohne Ergebnis.

**Schlecht:**

> So schöpfst du das volle Potenzial deiner Website aus.

**Besser:**

> Nenne das Ergebnis, das der Leser erreichen kann.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-15 Auf ein neues Level heben

Stufe: `tell`

Steigerungsbild ohne Messgröße.

**Schlecht:**

> Hebe dein Marketing auf das nächste Level.

**Besser:**

> Sag, was danach anders ist: [deine Messgröße].

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-16 Ganzheitlich

Stufe: `tell`

Modewort, das Vollständigkeit vortäuscht.

**Schlecht:**

> Wir bieten eine ganzheitliche Beratung.

**Besser:**

> Zähle auf, was die Beratung umfasst.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-17 Maßgeschneidert

Stufe: `tell`

Versprechen von Individualität ohne Beleg.

**Schlecht:**

> Wir entwickeln maßgeschneiderte Lösungen.

**Besser:**

> Beschreibe, was du für einen Kunden angepasst hast.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-18 Gamechanger

Stufe: `tell`

Superlativ aus dem Werbe-Englisch.

**Schlecht:**

> Diese Funktion ist ein echter Gamechanger.

**Besser:**

> Sag, was die Funktion ändert und für wen.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-19 Revolutionieren

Stufe: `tell`

Übertreibung ohne Vorher-Nachher.

**Schlecht:**

> KI revolutioniert die Buchhaltung.

**Besser:**

> KI übernimmt in der Buchhaltung [konkrete Aufgabe].

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-20 Nahtlos

Stufe: `tell`

Verspricht Reibungslosigkeit, belegt sie nicht.

**Schlecht:**

> Die Software integriert sich nahtlos.

**Besser:**

> Die Software liest [konkretes Format] direkt ein.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-21 Synergien

Stufe: `tell`

Beraterwort ohne konkreten Zusammenhang.

**Schlecht:**

> So entstehen Synergien zwischen den Teams.

**Besser:**

> Nenne, was ein Team dem anderen konkret abnimmt.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-22 Innovative Lösungen

Stufe: `tell`

Leeres Etikett für ein Angebot.

**Schlecht:**

> Wir liefern innovative Lösungen.

**Besser:**

> Sag, was das Angebot tut.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-23 Facettenreich / vielschichtig

Stufe: `tell`

Komplexität behauptet statt gezeigt.

**Schlecht:**

> Das Thema ist vielschichtig.

**Besser:**

> Nenne die zwei Seiten, um die es geht.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-24 Hand in Hand

Stufe: `tell`

Bild für Zusammenhang ohne Mechanismus.

**Schlecht:**

> SEO und Content gehen Hand in Hand.

**Besser:**

> Erkläre, wie das eine vom anderen abhängt.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-25 Am Ende des Tages

Stufe: `tell`

Übersetzte Redewendung als Füllung.

**Schlecht:**

> Am Ende des Tages zählt das Ergebnis.

**Besser:**

> Streichen oder das Ergebnis nennen.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-26 Last but not least

Stufe: `tell`

Aufzählungsfloskel.

**Schlecht:**

> Last but not least: die Kosten.

**Besser:**

> Nenne den Punkt ohne Ankündigung.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-27 Auf dieser Reise

Stufe: `tell`

Reise als Metapher für einen Prozess.

**Schlecht:**

> Wir begleiten dich auf deiner Reise.

**Besser:**

> Beschreibe die Schritte, bei denen du hilfst.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-28 Auf den Punkt gebracht

Stufe: `tell`

Ankündigung einer Verdichtung.

**Schlecht:**

> Auf den Punkt gebracht: Qualität zählt.

**Besser:**

> Sag direkt, was zählt und warum.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-29 Zusammenfassend lässt sich sagen

Stufe: `tell`

Schlussformel statt Schlussgedanke.

**Schlecht:**

> Zusammenfassend lässt sich sagen, dass Planung hilft.

**Besser:**

> Ende mit dem nächsten Schritt für den Leser.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-30 Werfen wir einen Blick

Stufe: `tell`

Leser-Choreografie statt Inhalt.

**Schlecht:**

> Werfen wir einen Blick auf die Vorteile.

**Besser:**

> Streiche den Satz und nenne den ersten Vorteil.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-31 Hier kommt X ins Spiel

Stufe: `tell`

Bühnenauftritt für ein Produkt oder Konzept.

**Schlecht:**

> Hier kommt Automatisierung ins Spiel.

**Besser:**

> Sag, welche Aufgabe die Automatisierung übernimmt.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-32 Dreh- und Angelpunkt

Stufe: `tell`

Bildhafte Wichtigkeit.

**Schlecht:**

> Der Kunde ist der Dreh- und Angelpunkt.

**Besser:**

> Sag, welche Entscheidung vom Kunden abhängt.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-33 Eckpfeiler

Stufe: `tell`

Architekturbild für Wichtigkeit.

**Schlecht:**

> Vertrauen ist ein Eckpfeiler der Marke.

**Besser:**

> Nenne, woran Kunden Vertrauen festmachen.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-34 Den Grundstein legen

Stufe: `tell`

Baumetapher ohne Bauplan.

**Schlecht:**

> So legst du den Grundstein für Wachstum.

**Besser:**

> Nenne den ersten konkreten Schritt.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-35 Nicht zu unterschätzen

Stufe: `tell`

Doppelte Verneinung als Betonung.

**Schlecht:**

> Der Aufwand ist nicht zu unterschätzen.

**Besser:**

> Der Aufwand liegt bei [deine Schätzung aus der Praxis].

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-36 Effizient und effektiv

Stufe: `tell`

Wortpaar ohne Unterschied im Satz.

**Schlecht:**

> Arbeite effizient und effektiv.

**Besser:**

> Sag, was der Leser weglassen kann.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-37 Der größte Hebel

Stufe: `tell`

Hebel-Metapher für Wirkung.

**Schlecht:**

> Content ist dein größter Hebel.

**Besser:**

> Sag, was Content bei dir konkret bewirkt hat.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-38 Wertvolle Einblicke

Stufe: `tell`

Wertung statt Inhalt.

**Schlecht:**

> Der Bericht bietet wertvolle Einblicke.

**Besser:**

> Nenne die eine Erkenntnis aus dem Bericht.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-39 Der ultimative Leitfaden

Stufe: `tell`

Superlativ im Titel.

**Schlecht:**

> Der ultimative Leitfaden für Newsletter

**Besser:**

> Newsletter: [konkretes Versprechen, das der Text hält]

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-40 Im Handumdrehen / leicht gemacht

Stufe: `tell`

Verspricht Mühelosigkeit.

**Schlecht:**

> So erstellst du im Handumdrehen Rechnungen.

**Besser:**

> Nenne, wie lange es wirklich dauert: [deine Zeit].

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-41 Die digitale Landschaft

Stufe: `tell`

Landschaftsbild für einen Markt.

**Schlecht:**

> In der digitalen Landschaft verändert sich viel.

**Besser:**

> Nenne die eine Veränderung, die deine Leser betrifft.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-42 Im stetigen Wandel

Stufe: `tell`

Wandel als Dauerzustand ohne Richtung.

**Schlecht:**

> Der Markt befindet sich im stetigen Wandel.

**Besser:**

> Sag, was sich zuletzt geändert hat.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-43 Fakt ist

Stufe: `tell`

Behauptung als Tatsache verkleidet.

**Schlecht:**

> Fakt ist: Ohne Strategie geht nichts.

**Besser:**

> Nenne den Beleg oder formuliere es als deine Erfahrung.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-44 Die gute Nachricht

Stufe: `tell`

Spannungsbogen-Formel.

**Schlecht:**

> Die gute Nachricht: Es gibt eine Lösung.

**Besser:**

> Nenne die Lösung direkt.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-45 Bahnbrechend

Stufe: `tell`

Superlativ ohne Vergleich.

**Schlecht:**

> Eine bahnbrechende Methode.

**Besser:**

> Sag, was die Methode anders macht als die übliche.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-46 Wegweisend / zukunftsweisend

Stufe: `tell`

Zukunftsversprechen ohne Inhalt.

**Schlecht:**

> Ein zukunftsweisender Ansatz.

**Besser:**

> Sag, welches Problem der Ansatz löst.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-47 Essenziell / unerlässlich

Stufe: `tell`

Pflicht-Rhetorik ohne Grund.

**Schlecht:**

> Eine gute Datenbasis ist essenziell.

**Besser:**

> Sag, was ohne Datenbasis schiefgeht.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-48 Mehrwert schaffen

Stufe: `tell`

Nutzen behauptet statt beschrieben.

**Schlecht:**

> Wir schaffen echten Mehrwert für Kunden.

**Besser:**

> Nenne, was der Kunde danach kann oder spart.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-49 Wettbewerbsvorteil sichern

Stufe: `tell`

Strategie-Floskel.

**Schlecht:**

> So sicherst du dir einen Wettbewerbsvorteil.

**Besser:**

> Sag, worin du besser wirst als die Konkurrenz.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-50 Herausforderungen meistern

Stufe: `tell`

Abstrakter Kampf statt konkretem Problem.

**Schlecht:**

> So meisterst du die Herausforderungen des Alltags.

**Besser:**

> Nenne das eine Problem und deinen Umgang damit.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-51 In den Fokus rücken

Stufe: `tell`

Bewegungsbild für Aufmerksamkeit.

**Schlecht:**

> Nachhaltigkeit rückt zunehmend in den Fokus.

**Besser:**

> Sag, wer worauf achtet und seit wann.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-52 Proaktiv

Stufe: `tell`

Managementwort ohne Handlung.

**Schlecht:**

> Gehe proaktiv auf Kunden zu.

**Besser:**

> Melde dich bei Kunden, bevor [konkreter Anlass].

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-53 Zielgerichtet / zielführend

Stufe: `tell`

Bürokratischer Füller.

**Schlecht:**

> Ein zielgerichteter Ansatz ist zielführend.

**Besser:**

> Sag, welches Ziel und welcher Ansatz.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-54 Wissen ist Macht

Stufe: `tell`

Sinnspruch als Argument.

**Schlecht:**

> Denn Wissen ist Macht.

**Besser:**

> Streichen.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-55 Die Antwort ist einfach

Stufe: `tell`

Behauptete Einfachheit.

**Schlecht:**

> Die Antwort ist einfach: Daten.

**Besser:**

> Gib die Antwort und begründe sie.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-56 Ein entscheidender Faktor

Stufe: `tell`

Faktor-Rhetorik statt Ursache.

**Schlecht:**

> Der Preis ist ein entscheidender Faktor.

**Besser:**

> Sag, ab welchem Preis Kunden abspringen: [deine Erfahrung].

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-57 Robust

Stufe: `tell`

Technik-Adjektiv als Qualitätssiegel.

**Schlecht:**

> Eine robuste Lösung für dein Team.

**Besser:**

> Sag, was die Lösung aushält: [Last, Fehler, Zeitraum].

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-58 Nicht nur, sondern auch (als Muster)

Stufe: `tell`

Doppelte Konstruktion, die beide Hälften aufbläht.

**Schlecht:**

> Das spart nicht nur Zeit, sondern auch Geld.

**Besser:**

> Das spart Zeit und Geld.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-59 Entscheidend

Stufe: `hint`

Häufiges Wichtigkeitswort.

**Schlecht:**

> Entscheidend ist die Planung.

**Besser:**

> Sag, was die Planung verhindert.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-60 Unverzichtbar

Stufe: `hint`

Pflichtwort, oft ohne Begründung.

**Schlecht:**

> Ein Newsletter ist unverzichtbar.

**Besser:**

> Sag, was ohne Newsletter fehlt.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-61 Best Practices

Stufe: `hint`

Fachjargon, oft ohne Inhalt.

**Schlecht:**

> Wir folgen Best Practices.

**Besser:**

> Nenne die eine Praxis, die du anwendest.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-62 Potenzial

Stufe: `hint`

Möglichkeitswort ohne Größe.

**Schlecht:**

> Hier liegt großes Potenzial.

**Besser:**

> Sag, was konkret möglich ist.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-63 Kurz gesagt

Stufe: `hint`

Ankündigung einer Kurzfassung.

**Schlecht:**

> Kurz gesagt: Es lohnt sich.

**Besser:**

> Sag direkt, was sich lohnt.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-64 Auf Augenhöhe

Stufe: `hint`

Haltungsformel.

**Schlecht:**

> Wir arbeiten auf Augenhöhe.

**Besser:**

> Beschreibe, wie Entscheidungen bei euch fallen.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-65 Es lohnt sich

Stufe: `hint`

Werturteil ohne Maßstab.

**Schlecht:**

> Es lohnt sich, das zu testen.

**Besser:**

> Sag, was der Test zeigt.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-66 Erfolgsgeschichte

Stufe: `hint`

Etikett statt Geschichte.

**Schlecht:**

> Eine echte Erfolgsgeschichte.

**Besser:**

> Erzähle, was passiert ist.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-67 Nachhaltig (als Füllwort)

Stufe: `hint`

Oft nur Verstärker.

**Schlecht:**

> Nachhaltig erfolgreich werden.

**Besser:**

> Sag, was über welchen Zeitraum hält.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-68 Optimal / optimieren (als Füllwort)

Stufe: `hint`

Versprechen ohne Maßstab.

**Schlecht:**

> Optimale Ergebnisse erzielen.

**Besser:**

> Nenne das Ergebnis, das du erwartest.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-69 Zahlreiche Vorteile

Stufe: `tell`

Menge behauptet, nicht genannt.

**Schlecht:**

> Die Methode bietet zahlreiche Vorteile.

**Besser:**

> Nenne die zwei wichtigsten Vorteile.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-70 Ein wahrer Schatz / Goldgrube

Stufe: `tell`

Bild für Wert.

**Schlecht:**

> Kundenfeedback ist eine wahre Goldgrube.

**Besser:**

> Sag, was du aus Feedback gelernt hast.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-71 Den Unterschied machen

Stufe: `tell`

Wirkung behauptet ohne Vergleich.

**Schlecht:**

> Kleine Details machen den Unterschied.

**Besser:**

> Nenne das Detail und was es geändert hat.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-72 Nicht mehr wegzudenken

Stufe: `tell`

Unverzichtbarkeits-Floskel.

**Schlecht:**

> Social Media ist nicht mehr wegzudenken.

**Besser:**

> Sag, wofür deine Kunden Social Media nutzen.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

### P-73 Immer wichtiger

Stufe: `tell`

Trendbehauptung ohne Zeitpunkt.

**Schlecht:**

> Bewertungen werden immer wichtiger.

**Besser:**

> Sag, woran du merkst, dass Bewertungen mehr zählen.

**Vorschlag:** Streichen oder durch eine konkrete Aussage ersetzen.

## Struktur

Wiederkehrende Formen: Aufbau und Auflösung, Dreierlisten überall, Zwischenüberschriften als Frage ohne Antwort im Absatz, eine Zusammenfassung nach jedem Abschnitt.

### T-01 Kontrast-Schablone

Stufe: `tell`

"Es geht nicht um X, sondern um Y" und ähnliche Gegenüberstellungen, die eine Position erfinden, nur um sie zu widerlegen. Einmal ist ein Hinweis, ab zwei ein Muster.

**Schlecht:**

> Es geht nicht um Reichweite. Es geht um Vertrauen.

**Besser:**

> Vertrauen bringt uns mehr Anfragen als Reichweite: [deine Beobachtung].

**Vorschlag:** Die Gegenposition streichen und die eigene Aussage direkt begründen.

### T-02 Dreierlisten-Häufung

Stufe: `tell`

Immer wieder drei Begriffe in einer Reihe ("schnell, einfach und sicher"). Einzelne Dreierlisten sind normal, gehäuft wirken sie mechanisch.

**Schlecht:**

> Schnell, einfach und sicher. Klar, präzise und verständlich.

**Besser:**

> Nenne nur die Eigenschaft, die du belegen kannst, und belege sie.

**Vorschlag:** Listen kürzen: zwei Begriffe oder einer mit Beleg.

### T-03 Konnektor am Satzanfang

Stufe: `tell`

Gehäufte Satzanfänge mit "Zudem", "Darüber hinaus", "Außerdem". Sie verbinden nichts, sie stapeln.

**Schlecht:**

> Zudem ist es günstig. Darüber hinaus ist es schnell.

**Besser:**

> Es ist günstig und schnell, weil [Grund].

**Vorschlag:** Konnektor streichen oder den Zusammenhang ausformulieren (weil, deshalb, aber).

### T-04 Gleiche Satzanfänge

Stufe: `tell`

Drei oder mehr Sätze in Folge beginnen mit demselben Wort.

**Schlecht:**

> Du planst. Du schreibst. Du prüfst.

**Besser:**

> Variiere den Einstieg oder fasse die Schritte als Liste.

**Vorschlag:** Satzanfänge variieren oder Sätze zusammenfassen.

### T-05 Rhetorische Frage als Einstieg

Stufe: `tell`

Ein Absatz beginnt mit einer Frage, die er selbst sofort beantwortet. Einmal geht, gehäuft wirkt es wie eine Schablone.

**Schlecht:**

> Warum ist das wichtig? Weil Kunden vergleichen.

**Besser:**

> Kunden vergleichen, bevor sie anfragen: [woran du das merkst].

**Vorschlag:** Die Antwort direkt als ersten Satz schreiben.

### T-06 Doppelpunkt-Enthüllung

Stufe: `tell`

Ein kurzer Satzanfang mit Doppelpunkt oder Fragezeichen baut Spannung auf ("Das Ergebnis:", "Der Grund?").

**Schlecht:**

> Das Ergebnis: mehr Anfragen.

**Besser:**

> Wir bekamen danach mehr Anfragen, etwa [deine Zahl] pro Woche statt [vorher].

**Vorschlag:** Den Satz normal bauen: Subjekt, Verb, Aussage.

### T-07 Pathos am Schluss

Stufe: `tell`

Der letzte Satz endet mit einer großen Geste ("Die Zukunft gehört dir", "Der erste Schritt beginnt jetzt").

**Schlecht:**

> Die Zukunft gehört denen, die jetzt handeln.

**Besser:**

> Ende mit einem konkreten nächsten Schritt: [was der Leser morgen tun kann].

**Vorschlag:** Den Schlusssatz streichen oder durch einen konkreten Schritt ersetzen.

### T-08 Zusammenfassung als Ende

Stufe: `tell`

Der Text endet mit einer Wiederholung des Gesagten ("Zusammenfassend", "Alles in allem").

**Schlecht:**

> Zusammenfassend lässt sich sagen, dass Planung wichtig ist.

**Besser:**

> Ende mit einer offenen Frage aus deiner Praxis oder dem nächsten Schritt.

**Vorschlag:** Den Schlussabsatz streichen oder durch etwas Neues ersetzen.

### T-09 Partizip-Anhängsel

Stufe: `tell`

Ein Satz bekommt hinten eine Deutung angehängt (", wodurch ...", ", was zeigt, dass ...").

**Schlecht:**

> Der Umsatz stieg, wodurch die Bedeutung von SEO deutlich wird.

**Besser:**

> Der Umsatz stieg. Den größten Anteil hatten [deine Quelle der Anfragen].

**Vorschlag:** Das Anhängsel streichen oder als eigenen Satz mit Beleg schreiben.

## Rhythmus

Gemessen über den ganzen Text und verglichen mit dem Bereich menschlich geschriebener Vergleichstexte. Zu gleichförmig ist ein Befund, übers Ziel hinaus auch.

### R-01 Kurze Sätze

Stufe: `hint`

Mittlere Satzlänge in Wörtern. Generierte Fachtexte haben im Mittel deutlich kürzere Sätze als menschliche Texte im Vergleichsband.

**Schlecht:**

> Jeder Satz ist kurz. Jeder Satz endet schnell. Kein Gedanke wird entwickelt.

**Besser:**

> Verbinde Gedanken, die zusammengehören, zu einem Satz und begründe sie [weil ...].

**Vorschlag:** Nur ein Hinweis: Ein einzelner Wert außerhalb des Bands kommt auch bei Menschen oft vor. Zählt erst im Zusammentreffen (R-10).

### R-02 Gleichförmige Satzlängen

Stufe: `hint`

Streuung der Satzlängen innerhalb der Absätze (Variationskoeffizient). Sehr gleichmäßige Sätze liegen auf der Seite generierter Texte.

**Schlecht:**

> Alle Sätze sind ähnlich lang und ähnlich gebaut.

**Besser:**

> Mische kurze und lange Sätze, so wie du sprichst.

**Vorschlag:** Nur ein Hinweis: Ein einzelner Wert außerhalb des Bands kommt auch bei Menschen oft vor. Zählt erst im Zusammentreffen (R-10).

### R-03 Kurze Absätze

Stufe: `hint`

Mittlere Wörter je Absatz. Generierte Texte zerlegen den Inhalt in viele kurze Absätze.

**Schlecht:**

> Ein Absatz, ein Satz. Dann der nächste Absatz.

**Besser:**

> Fasse Absätze zusammen, die einen Gedanken gemeinsam tragen.

**Vorschlag:** Nur ein Hinweis: Ein einzelner Wert außerhalb des Bands kommt auch bei Menschen oft vor. Zählt erst im Zusammentreffen (R-10).

### R-04 Hohe Wortvielfalt

Stufe: `hint`

Wortvielfalt (MATTR, Fenster 50 Wörter). Generierte Texte wiederholen Wörter seltener und wechseln öfter das Synonym als menschliche Texte.

**Schlecht:**

> Lösung, Ansatz, Methode, Strategie: viermal dasselbe gemeint.

**Besser:**

> Bleib beim Fachwort, wenn du dasselbe meinst.

**Vorschlag:** Nur ein Hinweis: Ein einzelner Wert außerhalb des Bands kommt auch bei Menschen oft vor. Zählt erst im Zusammentreffen (R-10).

### R-05 Lange Wörter

Stufe: `hint`

Mittlere Wortlänge in Buchstaben. Generierte Texte greifen öfter zu langen, abstrakten Wörtern.

**Schlecht:**

> Effizienzsteigerungspotenziale werden zielgerichtet ausgeschöpft.

**Besser:**

> Sag, was konkret schneller geht: [Vorgang].

**Vorschlag:** Nur ein Hinweis: Ein einzelner Wert außerhalb des Bands kommt auch bei Menschen oft vor. Zählt erst im Zusammentreffen (R-10).

### R-06 Nominalstil

Stufe: `hint`

Wörter auf -ung, -heit, -keit, -tion, -ität, -schaft, -ismus je 1.000 Wörter.

**Schlecht:**

> Die Durchführung der Optimierung erfolgt nach der Analyse.

**Besser:**

> Wir optimieren, nachdem wir [Gegenstand] analysiert haben.

**Vorschlag:** Nur ein Hinweis: Ein einzelner Wert außerhalb des Bands kommt auch bei Menschen oft vor. Zählt erst im Zusammentreffen (R-10).

### R-07 Viele Dreierlisten

Stufe: `hint`

Aufzählungen der Form "A, B und C" je 1.000 Wörter. Ergänzt das Muster T-02 um eine gemessene Rate.

**Schlecht:**

> Schnell, sicher und einfach. Klar, präzise und verständlich.

**Besser:**

> Nenne nur, was wirklich zutrifft, auch wenn es zwei Punkte sind.

**Vorschlag:** Nur ein Hinweis: Ein einzelner Wert außerhalb des Bands kommt auch bei Menschen oft vor. Zählt erst im Zusammentreffen (R-10).

### R-08 Viele Doppelpunkte

Stufe: `hint`

Doppelpunkte im Fließtext je 1.000 Wörter (ohne Uhrzeiten und Links).

**Schlecht:**

> Das Ziel: Wachstum. Der Weg: Klarheit. Das Ergebnis: Erfolg.

**Besser:**

> Schreib ganze Sätze statt "Begriff: Erklärung".

**Vorschlag:** Nur ein Hinweis: Ein einzelner Wert außerhalb des Bands kommt auch bei Menschen oft vor. Zählt erst im Zusammentreffen (R-10).

### R-09 Partizip-Anhängsel (Rate)

Stufe: `hint`

Nur im Englischen gemessen: Anhängsel wie ", ensuring ..." je 1.000 Wörter. Das deutsche Gegenstück "um ... zu" trennt in der Messung nicht.

**Schlecht:**

> Wir prüfen jeden Text, um höchste Qualität zu gewährleisten.

**Besser:**

> Wir prüfen jeden Text, weil [Grund].

**Vorschlag:** Nur ein Hinweis: Ein einzelner Wert außerhalb des Bands kommt auch bei Menschen oft vor. Zählt erst im Zusammentreffen (R-10).

### R-10 Viele Messwerte auf der KI-Seite

Stufe: `tell`

Mindestens so viele gemessene Merkmale wie die Urteilsgrenze des Bands liegen gleichzeitig außerhalb des Bands auf der Seite generierter Texte. Ein einzelnes Merkmal ist nur ein Hinweis, das Zusammentreffen ist ein Befund.

**Schlecht:**

> Kurze Sätze, kurze Absätze, viele Doppelpunkte und Dreierlisten in einem Text.

**Besser:**

> Schreib den Text in deiner eigenen Gliederung neu: weniger Zwischentitel, längere Gedanken, konkrete Beispiele [aus deiner Arbeit].

**Vorschlag:** Die gemeldeten Messwerte einzeln angehen, nicht nur Wörter tauschen.

## Form

Typografie und Layout: lange Gedankenstriche als Stilmittel, Emoji-Aufzählungen, fett gesetzte Wörter mitten im Fließtext.

### F-01 Langer Gedankenstrich

Stufe: `tell`

Stilregel: der lange Gedankenstrich (U+2014) außerhalb von Zitaten. Viele Leser empfinden lange Gedankenstriche als KI-typisch. In der Messung trennt er menschliche und generierte Texte nicht; deshalb ist er eine abschaltbare Stilregel (Konfiguration "dashes").

**Schlecht:**

> Das Ergebnis — mehr Anfragen.

**Besser:**

> Das Ergebnis: mehr Anfragen.

**Vorschlag:** Durch Punkt, Komma, Doppelpunkt oder Klammer ersetzen.

### F-02 Halbgeviertstrich als Gedankenstrich

Stufe: `tell`

Der Halbgeviertstrich (U+2013) ist zwischen Zahlen richtig (10–20), zwischen Wörtern wirkt er wie ein Gedankenstrich.

**Schlecht:**

> Schnell – und günstig.

**Besser:**

> Schnell und günstig.

**Vorschlag:** Durch Komma, Punkt oder Doppelpunkt ersetzen.

### F-03 Bindestrich als Gedankenstrich

Stufe: `tell`

" - " mit Leerzeichen ersetzt einen Gedankenstrich.

**Schlecht:**

> Schnell - und günstig.

**Besser:**

> Schnell und günstig.

**Vorschlag:** Durch Komma, Punkt oder Doppelpunkt ersetzen.

### F-04 Emojis

Stufe: `hint`

Emojis im Fachtext. Standard: mehr als eines pro Abschnitt ist ein Hinweis. Mit emojis: no ist jedes ein Fund.

**Schlecht:**

> 🚀 Starte jetzt 💪

**Besser:**

> Starte jetzt.

**Vorschlag:** Emoji entfernen.

### F-05 Fettdruck-Häufung

Stufe: `tell`

Viele fett gesetzte Stellen in einem Absatz. Wenn alles betont ist, ist nichts betont.

**Schlecht:**

> **Wichtig:** Nutze **klare** Ziele und **messbare** Werte.

**Besser:**

> Nutze klare Ziele und messbare Werte. Fett höchstens für den einen Begriff, den Leser wiederfinden müssen.

**Vorschlag:** Fettdruck auf einen Begriff pro Abschnitt reduzieren.

### F-06 Etikett-Überschrift

Stufe: `tell`

Überschriften wie "Was ist X?", "Fazit" oder "Einleitung" sagen, wo man ist, nicht was man erfährt.

**Schlecht:**

> ## Fazit

**Besser:**

> ## Was du morgen als Erstes ändern kannst

**Vorschlag:** Die Überschrift als Aussage oder Versprechen formulieren.

### F-07 Anrede-Wechsel

Stufe: `tell`

Der Text wechselt zwischen du und Sie. Mit address: du oder sie (Option --address) ist jede falsche Form ein Fehler, ohne Angabe ein Hinweis auf die seltenere Form.

**Schlecht:**

> Du kannst das sofort testen. Probieren Sie es aus.

**Besser:**

> Du kannst das sofort testen. Probier es aus.

**Vorschlag:** Eine Anrede wählen und durchziehen.

### F-08 Zu viele Überschriften

Stufe: `tell`

Sehr viele Überschriften für wenig Text. Der Text zerfällt in Häppchen.

**Schlecht:**

> Alle 60 Wörter eine neue Zwischenüberschrift.

**Besser:**

> Abschnitte zusammenlegen, bis jeder etwas zu sagen hat.

**Vorschlag:** Abschnitte zusammenlegen.

### F-09 Verbotenes Wort (eigene Liste)

Stufe: `fail`

Ein Wort aus deiner eigenen Verbotsliste (Option --forbid oder forbid in .slopcheck.json).

**Schlecht:**

> [ein Wort von deiner Liste]

**Besser:**

> [deine bevorzugte Formulierung]

**Vorschlag:** Wort ersetzen oder streichen.
