"""Table-driven cases for German texts: hits and false-alarm guards."""

import unittest

from helpers import add_cases

EM = "\u2014"
EN = "\u2013"

CASES = [
    # --- S-01 figures --------------------------------------------------------------------------
    ("de_s01_percent", "de", "73 % der Kunden lesen Bewertungen vor dem Kauf.", "S-01", "fail"),
    ("de_s01_prozent_word", "de", "Rund 40 Prozent der Betriebe planen das.", "S-01", "fail"),
    ("de_s01_zahlwort_prozent", "de", "Vierzig Prozent der Leser springen ab.", "S-01", "fail"),
    ("de_s01_millionen", "de", "Der Markt umfasst 3,5 Millionen Betriebe.", "S-01", "fail"),
    ("de_s01_euro", "de", "Ein Relaunch kostet im Schnitt 12.000 Euro.", "S-01", "fail"),
    ("de_s01_euro_sign", "de", "Die Kampagne brachte € 5.000 zusätzlichen Umsatz.", "S-01", "fail"),
    ("de_s01_thousands", "de", "Das Portal hat 15.000 Abonnenten.", "S-01", "fail"),
    ("de_s01_x_von_y", "de", "7 von 10 Kunden fragen nach dem Preis.", "S-01", "fail"),
    ("de_s01_mal_schneller", "de", "Die Seite lädt 3x schneller als vorher.", "S-01", "fail"),
    ("de_s01_drittel", "de", "Ein Drittel der Anfragen kommt über Empfehlungen.", "S-01", "fail"),
    ("de_s01_haelfte", "de", "Die Hälfte der Kunden kauft mobil.", "S-01", "fail"),
    ("de_s01_jeder_dritte", "de", "Jeder dritte Besucher bricht den Kauf ab.", "S-01", "fail"),
    ("de_s01_jedem_vierten", "de", "Bei jedem vierten Projekt fehlt das Budget.", "S-01", "fail"),
    ("de_s01_doppelt", "de", "Videos werden doppelt so oft geteilt.", "S-01", "fail"),
    ("de_s01_dreifache", "de", "Der Umsatz stieg um das Dreifache.", "S-01", "fail"),
    ("de_s01_mehrheit", "de", "Die Mehrheit der Leser scrollt nicht bis zum Ende.", "S-01", "fail"),
    ("de_s01_heading_unbacked", "de", "## 73 % mehr Anfragen\n\nWir haben mehr Anfragen bekommen.", "S-01", "fail"),
    # sourced
    ("de_s01_link", "de", "73 % der Kunden lesen Bewertungen ([Erhebung](https://example.org/x)).", "S-01", "none"),
    ("de_s01_quelle_paren", "de", "73 % der Kunden lesen Bewertungen (Quelle: Branchenreport 2025).", "S-01", "none"),
    ("de_s01_bare_url", "de", "73 % der Kunden lesen Bewertungen, siehe https://example.org/bericht.", "S-01", "none"),
    ("de_s01_footnote", "de", "73 % der Kunden lesen Bewertungen.[^1]\n\n[^1]: https://example.org", "S-01", "none"),
    ("de_s01_heading_backed", "de", "## 40 % weniger Rückfragen\n\nDie Rückfragen sanken um 40 % ([Auswertung](https://example.org/a)).", "S-01", "none"),
    ("de_s01_table_source_col", "de", "| Kanal | Anteil | Quelle |\n|---|---|---|\n| Suche | 40 % | Report X |", "S-01", "none"),
    ("de_s01_table_caption", "de", "| Kanal | Anteil |\n|---|---|\n| Suche | 40 % |\n\nQuelle: eigene Auswertung 2025", "S-01", "none"),
    ("de_s01_table_unsourced", "de", "| Kanal | Anteil |\n|---|---|\n| Suche | 40 % |", "S-01", "fail"),
    # own experience
    ("de_s08_ich", "de", "Ich habe die Kosten um 40 % gesenkt.", "S-08", "hint"),
    ("de_s08_wir", "de", "Wir hatten danach 15.000 Leser im Monat.", "S-08", "hint"),
    ("de_s08_bei_uns", "de", "Bei uns fragen 7 von 10 Kunden zuerst nach dem Preis.", "S-08", "hint"),
    ("de_s08_not_fail", "de", "Ich habe die Kosten um 40 % gesenkt.", "S-01", "none"),
    # false-alarm guards
    ("de_fa_year", "de", "Seit 2019 schreibe ich über Handwerk.", "S-01", "none"),
    ("de_fa_year_range", "de", "Häuser von 1960 bis 1980 haben oft alte Estriche.", "S-01", "none"),
    ("de_fa_paragraph", "de", "Nach § 312k BGB braucht ein Abo einen Kündigungsbutton.", "S-01", "none"),
    ("de_fa_paragraph_abs", "de", "Das regelt § 13 Abs. 2 Satz 1 UStG.", "S-01", "none"),
    ("de_fa_artikel", "de", "Art. 17 DSGVO regelt das Recht auf Löschung.", "S-01", "none"),
    ("de_fa_measure_km", "de", "Der Weg zur Baustelle ist 12.000 km lang gewesen.", "S-01", "none"),
    ("de_fa_measure_mm", "de", "Die Platte ist 1.200 mm breit.", "S-01", "none"),
    ("de_fa_dims", "de", "Das Bild hat 1920 x 1080 px.", "S-01", "none"),
    ("de_fa_version", "de", "Ab Version 10.4.2 klappt der Export.", "S-01", "none"),
    ("de_fa_time", "de", "Der Laden öffnet um 9:30 Uhr.", "S-01", "none"),
    ("de_fa_date", "de", "Der Termin ist am 12.03.2026.", "S-01", "none"),
    ("de_fa_small_count", "de", "Hier sind 3 Schritte für den Anfang.", "S-01", "none"),
    ("de_fa_schritt_von", "de", "Das ist Schritt 2 von 5.", "S-01", "none"),
    ("de_fa_plz", "de", "Die Werkstatt liegt in 34117 Kassel.", "S-01", "none"),
    ("de_fa_range_en_dash", "de", "Wir rechnen mit 2" + EN + "3 Tagen Einbau.", "S-01", "none"),
    ("de_fa_temperature", "de", "Der Estrich braucht 20 °C zum Trocknen.", "S-01", "none"),
    ("de_fa_code", "de", "```\nrate = 73 %\nprice = 12.000 Euro\n```", "S-01", "none"),
    ("de_fa_inline_code", "de", "Setze `limit = 15000` in der Konfiguration.", "S-01", "none"),
    ("de_fa_frontmatter", "de", "---\ntitle: 73 % mehr\n---\n\nText ohne Zahl.", "S-01", "none"),
    ("de_fa_sources_section", "de", "Text.\n\n## Quellen\n\n- Report 2025: 73 % der Kunden, https://example.org", "S-01", "none"),
    # --- S-02 vague attribution ----------------------------------------------------------------
    ("de_s02_studien", "de", "Studien zeigen, dass kurze Texte besser funktionieren.", "S-02", "fail"),
    ("de_s02_experten", "de", "Experten sind sich einig: Video ist die Zukunft.", "S-02", "fail"),
    ("de_s02_laut_studie", "de", "Laut einer aktuellen Studie lesen Kunden weniger.", "S-02", "fail"),
    ("de_s02_umfrage", "de", "Eine aktuelle Umfrage belegt den Trend.", "S-02", "fail"),
    ("de_s02_wissenschaft", "de", "Das ist wissenschaftlich erwiesen.", "S-02", "fail"),
    ("de_s02_sourced", "de", "Studien zeigen, dass kurze Texte besser funktionieren ([Studie](https://example.org/s)).", "S-02", "none"),
    ("de_s02_own_study", "de", "Unsere Auswertung von elf Artikeln hat das bestätigt.", "S-02", "none"),
    # --- S-03 people ---------------------------------------------------------------------------
    ("de_s03_sagt", "de", "Thomas Weber sagt, Inhalte seien alles.", "S-03", "tell"),
    ("de_s03_rolle_dazwischen", "de", "Thomas Weber, Marketingexperte, sagt: \"Content ist alles.\"", "S-03", "tell"),
    ("de_s03_laut_rolle", "de", "Laut Expertin Anna Berg lohnt sich das.", "S-03", "tell"),
    ("de_s03_empfiehlt", "de", "Das empfiehlt Dr. Jana Krüger seit Jahren.", "S-03", "tell"),
    ("de_s03_linked", "de", "[Thomas Weber](https://example.org/tw) sagt, Inhalte seien alles.", "S-03", "none"),
    ("de_s03_sourced", "de", "Thomas Weber sagt, Inhalte seien alles (Quelle: Interview vom 3. Mai).", "S-03", "none"),
    ("de_s03_institution", "de", "Die Handwerkskammer Kassel empfiehlt eine Beratung.", "S-03", "none"),
    ("de_s03_own_name", "de", "Anna Lange sagt, wir sollten früher anfangen.", "S-03", "none", {"own_names": ["Anna Lange"]}),
    ("de_s03_satzanfang", "de", "Am Ende sagte der Kunde, es passe.", "S-03", "none"),
    # --- S-04 portability ----------------------------------------------------------------------
    ("de_s04_generic", "de",
     "Gute Kommunikation ist die Basis jeder Zusammenarbeit zwischen Marke und Publikum. Wer klar und verständlich "
     "kommuniziert, vermeidet Missverständnisse, schafft Vertrauen und legt den Grundstein für eine langfristige Beziehung, "
     "die beiden Seiten nützt und über die Zeit stärker wird.", "S-04", "hint"),
    ("de_s04_concrete", "de",
     "Gute Kommunikation hat bei dem Tischler aus Kassel den Ausschlag gegeben. Ich habe im März mit ihm jede Anfrage "
     "durchgesprochen, und wir haben die Antwortzeit auf einen Tag gesenkt, weil die Kunden sonst bei der Konkurrenz "
     "angefragt hätten, wie er mir erzählte.", "S-04", "none"),
    ("de_s04_short", "de", "Gute Kommunikation ist die Basis jeder Zusammenarbeit.", "S-04", "none"),
    # --- S-06 advice ---------------------------------------------------------------------------
    ("de_s06_advice", "de", "Du solltest deine Zielgruppe kennen. Du solltest regelmäßig posten. Achte darauf, dass alles stimmt.", "S-06", "tell"),
    ("de_s06_with_list", "de", "Du solltest deine Zielgruppe kennen. Du solltest regelmäßig posten. Achte darauf, dass alles stimmt:\n\n1. Liste\n2. Liste", "S-06", "none"),
    ("de_s06_with_example", "de", "Du solltest deine Zielgruppe kennen, zum Beispiel über Gespräche. Du solltest regelmäßig posten. Achte darauf, dass alles stimmt.", "S-06", "none"),
    # --- S-07 smoothing ------------------------------------------------------------------------
    ("de_s07_fuehrend", "de", "Ein führender Anbieter nutzt die Methode bereits.", "S-07", "tell"),
    ("de_s07_namhafte", "de", "Namhafte Unternehmen vertrauen auf uns.", "S-07", "tell"),
    ("de_s07_zahlreiche", "de", "Zahlreiche Kunden sind zufrieden.", "S-07", "tell"),
    ("de_s07_quote_ok", "de", "Er sagte: \"Ein führender Anbieter macht das so.\"", "S-07", "none"),
    # --- phrases -------------------------------------------------------------------------------
    ("de_p_heutige_welt", "de", "In der heutigen schnelllebigen Welt zählt jede Minute.", "P-01", "tell"),
    ("de_p_kein_geheimnis", "de", "Es ist kein Geheimnis, dass Kunden vergleichen.", "P-06", "tell"),
    ("de_p_eintauchen", "de", "Tauchen wir tiefer in das Thema ein.", "P-07", "tell"),
    ("de_p_gamechanger_inflected", "de", "Das sind echte Gamechangers für Betriebe.", "P-18", "tell"),
    ("de_p_potenzial", "de", "So schöpfst du das volle Potenzial aus.", "P-14", "tell"),
    ("de_p_zusammenfassend", "de", "Zusammenfassend lässt sich sagen, dass Planung hilft.", "P-29", "tell"),
    ("de_p_cluster_single", "de", "Wir arbeiten ganzheitlich.", "P-16", "none"),
    ("de_p_cluster_pair_paragraph", "de", "Wir arbeiten ganzheitlich und schaffen nahtlose Abläufe.", "P-16", "tell"),
    ("de_p_cluster_inflected", "de", "Eine ganzheitliche, maßgeschneiderte Beratung.", "P-17", "tell"),
    ("de_p_context_hint", "de", "Entscheidend ist die Planung.", "P-59", "hint"),
    ("de_p_in_quote", "de", "Der Kunde schrieb: \"Das war ein echter Gamechanger für uns.\"", "P-18", "none"),
    ("de_p_in_blockquote", "de", "> In der heutigen schnelllebigen Welt zählt jede Minute.", "P-01", "none"),
    ("de_p_in_code", "de", "```\nIn der heutigen schnelllebigen Welt\n```", "P-01", "none"),
    ("de_p_allow_robust", "de", "Wir nutzen robuste Standardfehler und nahtlose Rohre in der Analyse.", "P-57", "none"),
    ("de_p_hebel_physik", "de", "Der Hebelarm ist doppelt so lang wie der Lastarm, das Hebelgesetz gilt.", "P-37", "none"),
    ("de_p_hebel_floskel", "de", "Content ist der größte Hebel für Wachstum und gleichzeitig ganzheitlich.", "P-37", "tell"),
    ("de_p_user_allow", "de", "Wir arbeiten ganzheitlich und schaffen nahtlose Abläufe.", "P-16", "none", {"allow": ["ganzheitlich"]}),
    ("de_p_disable", "de", "In der heutigen schnelllebigen Welt zählt jede Minute.", "P-01", "none", {"disable": ["P-01"]}),
    ("de_p_nicht_nur_once", "de", "Das spart nicht nur Zeit, sondern auch Geld.", "P-58", "none"),
    # --- structure -----------------------------------------------------------------------------
    ("de_t01_once_hint", "de", "Es geht nicht um Reichweite. Es geht um Vertrauen.", "T-01", "hint"),
    ("de_t01_twice", "de", "Es geht nicht um Reichweite. Es geht um Vertrauen. Das ist kein Trick. Das ist Handwerk.", "T-01", "tell"),
    ("de_t01_plain_sondern", "de", "Wir liefern nicht morgens, sondern abends.", "T-01", "none"),
    ("de_t02_two_in_paragraph", "de", "Gute Inhalte sind klar, präzise und verständlich. Sie stärken Marke, Vertrauen und Umsatz.", "T-02", "tell"),
    ("de_t02_single", "de", "Wir liefern Holz, Leim und Schrauben.", "T-02", "none"),
    ("de_t03_connectors", "de", "Zudem ist es günstig. Darüber hinaus ist es schnell. Außerdem ist es leise.", "T-03", "tell"),
    ("de_t03_single", "de", "Das Holz ist trocken. Außerdem ist es günstig.", "T-03", "none"),
    ("de_t03_two_in_paragraph", "de", "Zudem ist es günstig. Außerdem ist es schnell.", "T-03", "none"),
    ("de_t03_spread_low_rate", "de", ("Zudem ist das Holz trocken und lagert seit dem Winter in der Halle am Fluss. " + "Wir prüfen jede Lieferung mit dem Messgerät, bevor sie auf die Baustelle geht und dort verbaut wird. " * 12 + "\n\n") * 3, "T-03", "none"),
    ("de_t04_same", "de", "Du planst den Text. Du schreibst ihn. Du prüfst ihn danach.", "T-04", "tell"),
    ("de_t04_varied", "de", "Du planst den Text. Danach schreibst du ihn. Am Ende prüfst du ihn.", "T-04", "none"),
    ("de_t05_one", "de", "Warum ist das eigentlich so wichtig? Weil Kunden vergleichen.", "T-05", "hint"),
    ("de_t06_colon", "de", "Das Ergebnis: mehr Anfragen. Der Grund: bessere Texte.", "T-06", "tell"),
    ("de_t06_exclude_tipp", "de", "Tipp: Lies den Text laut.", "T-06", "none"),
    ("de_t07_pathos", "de", "Wir haben viel gelernt.\n\nDie Zukunft gehört denen, die jetzt handeln.", "T-07", "tell"),
    ("de_t08_summary", "de", "Erster Absatz mit Inhalt.\n\nAlles in allem lohnt sich der Aufwand.", "T-08", "tell"),
    ("de_t09_tail_twice", "de", "Der Umsatz stieg, wodurch die Bedeutung klar wird. Der Traffic wuchs, was zeigt, dass es wirkt.", "T-09", "tell"),
    ("de_t09_once", "de", "Der Umsatz stieg, wodurch wir neue Leute einstellen konnten.", "T-09", "hint"),
    # --- form ----------------------------------------------------------------------------------
    ("de_f01_em", "de", "Das Ergebnis " + EM + " mehr Anfragen.", "F-01", "tell"),
    ("de_f01_em_fail_mode", "de", "Das Ergebnis " + EM + " mehr Anfragen.", "F-01", "fail", {"dashes": "fail"}),
    ("de_f01_em_off", "de", "Das Ergebnis " + EM + " mehr Anfragen.", "F-01", "none", {"dashes": "off"}),
    ("de_f02_en_off", "de", "Schnell " + EN + " und günstig.", "F-02", "none", {"dashes": "off"}),
    ("de_f01_em_in_quote", "de", "Er sagte: \"Das Ergebnis " + EM + " mehr Anfragen.\"", "F-01", "none"),
    ("de_f01_em_in_code", "de", "```\na " + EM + " b\n```", "F-01", "none"),
    ("de_f02_en_words", "de", "Schnell " + EN + " und günstig.", "F-02", "tell"),
    ("de_f02_en_numbers", "de", "Wir brauchen 10" + EN + "20 Minuten.", "F-02", "none"),
    ("de_f03_hyphen", "de", "Schnell - und günstig.", "F-03", "tell"),
    ("de_f03_numbers", "de", "Das Spiel endete 3 - 1.", "F-03", "none"),
    ("de_f03_compound", "de", "Wir bieten Ein- und Ausbau an.", "F-03", "none"),
    ("de_f04_emoji_limit", "de", "## Start\n\nLos geht es \U0001F680 mit Kraft \U0001F4AA heute.", "F-04", "hint"),
    ("de_f04_emoji_no", "de", "Los geht es \U0001F680 heute.", "F-04", "tell", {"emojis": "no"}),
    ("de_f04_emoji_one", "de", "Los geht es \U0001F680 heute.", "F-04", "none"),
    ("de_f05_bold", "de", "**Wichtig:** Nutze **klare** Ziele und **messbare** Werte.", "F-05", "tell"),
    ("de_f05_bold_heading_line", "de", "**Zwischentitel**\n\nNormaler Text mit einem **Begriff**.", "F-05", "none"),
    ("de_f06_fazit", "de", "## Fazit\n\nText.", "F-06", "tell"),
    ("de_f06_was_ist", "de", "## Was ist Content-Marketing?\n\nText.", "F-06", "tell"),
    ("de_f06_promise", "de", "## Was du morgen als Erstes ändern kannst\n\nText.", "F-06", "none"),
    ("de_f06_faq_question", "de", "## Häufige Fragen\n\n### Was ist ein Estrich?\n\nEin Untergrund.", "F-06", "none"),
    ("de_f07_switch_auto", "de", "Du kannst das testen. Probieren Sie es aus. Du wirst sehen, dass es klappt.", "F-07", "tell"),
    ("de_f07_du_config", "de", "Du kannst das testen. Probieren Sie es aus.", "F-07", "fail", {"address": "du"}),
    ("de_f07_sie_config", "de", "Sie können das testen. Probier es mit deinem Team aus.", "F-07", "fail", {"address": "sie"}),
    ("de_f07_sie_start", "de", "Du kannst sie fragen. Sie antworten meist schnell.", "F-07", "none", {"address": "du"}),
    ("de_f07_quote", "de", "Du kannst das testen. Der Kunde sagte: \"Probieren Sie es aus.\"", "F-07", "none", {"address": "du"}),
    ("de_f09_forbid", "de", "Wir bieten dynamische Teams.", "F-09", "fail", {"forbid": ["dynamisch"]}),
    ("de_f09_forbid_phrase", "de", "Wir bieten spannenden Aufgaben an.", "F-09", "fail", {"forbid": ["spannende Aufgaben"]}),
    ("de_f09_forbid_quote", "de", "Er sagte: \"dynamische Teams\".", "F-09", "none", {"forbid": ["dynamisch"]}),
]


class GermanCases(unittest.TestCase):
    pass


add_cases(GermanCases, CASES)

if __name__ == "__main__":
    unittest.main()


class GermanGuardrailCases(unittest.TestCase):
    pass


add_cases(GermanGuardrailCases, [
    ("de_titel_link", "de", "Siehe [Der ultimative Leitfaden für Estrich](https://example.org/l) für Details.", "P-39", "none"),
    ("de_titel_zitat", "de", "Ihr Buch „Der Schlüssel zum Erfolg“ ist kurz.", "P-13", "none"),
    ("de_link_person_numbers", "de", "Laut [Erhebung](https://example.org/e) sind es 40 %.", "S-01", "none"),
])
