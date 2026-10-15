"""Table-driven cases for English texts: hits and false-alarm guards."""

import unittest

from helpers import add_cases

EM = "\u2014"
EN = "\u2013"

CASES = [
    # --- S-01 figures --------------------------------------------------------------------------
    ("en_s01_percent", "en", "73% of customers read reviews before buying.", "S-01", "fail"),
    ("en_s01_percent_word", "en", "About 40 percent of firms plan this.", "S-01", "fail"),
    ("en_s01_word_percent", "en", "Forty percent of readers leave early.", "S-01", "fail"),
    ("en_s01_million", "en", "The market covers 3.5 million businesses.", "S-01", "fail"),
    ("en_s01_dollars", "en", "A relaunch costs $12,000 on average.", "S-01", "fail"),
    ("en_s01_thousands", "en", "The newsletter has 15,000 subscribers.", "S-01", "fail"),
    ("en_s01_k", "en", "The post reached 20k readers.", "S-01", "fail"),
    ("en_s01_out_of", "en", "7 out of 10 customers ask about price first.", "S-01", "fail"),
    ("en_s01_one_in", "en", "One in five visitors abandons the cart.", "S-01", "fail"),
    ("en_s01_times_faster", "en", "The page loads 3x faster than before.", "S-01", "fail"),
    ("en_s01_third", "en", "A third of enquiries come from referrals.", "S-01", "fail"),
    ("en_s01_half", "en", "Half of the customers buy on mobile.", "S-01", "fail"),
    ("en_s01_twice", "en", "Videos are shared twice as often.", "S-01", "fail"),
    ("en_s01_tripled", "en", "The company tripled its revenue.", "S-01", "fail"),
    ("en_s01_majority", "en", "The majority of readers never scroll to the end.", "S-01", "fail"),
    ("en_s01_link", "en", "73% of customers read reviews ([survey](https://example.org/x)).", "S-01", "none"),
    ("en_s01_source_paren", "en", "73% of customers read reviews (source: trade report 2025).", "S-01", "none"),
    ("en_s01_numbered_ref", "en", "73% of customers read reviews [1].\n\n## Sources\n\n[1] https://example.org", "S-01", "none"),
    ("en_s08_we", "en", "We cut costs by 40% in one year.", "S-08", "hint"),
    ("en_s08_i", "en", "I had 15,000 readers a month after that.", "S-08", "hint"),
    ("en_s08_our_clients", "en", "At our shop, 7 out of 10 customers ask about price first.", "S-08", "hint"),
    # false-alarm guards
    ("en_fa_year", "en", "I have written about trades since 2019.", "S-01", "none"),
    ("en_fa_year_range", "en", "Houses built between 1960 and 1980 often have old screed.", "S-01", "none"),
    ("en_fa_section", "en", "Section 230 covers this case.", "S-01", "none"),
    ("en_fa_legal_paragraph", "en", "Under § 312k BGB a subscription needs a cancel button.", "S-01", "none"),
    ("en_fa_measure", "en", "The board is 1,200 mm wide.", "S-01", "none"),
    ("en_fa_measure_miles", "en", "We drove 12,000 miles last year.", "S-01", "none"),
    ("en_fa_dims", "en", "The image is 1920 x 1080 px.", "S-01", "none"),
    ("en_fa_version", "en", "From version 10.4.2 the export works.", "S-01", "none"),
    ("en_fa_time", "en", "The shop opens at 9:30 am.", "S-01", "none"),
    ("en_fa_iso_date", "en", "The meeting is on 2026-03-12.", "S-01", "none"),
    ("en_fa_small_count", "en", "Here are 3 steps to start.", "S-01", "none"),
    ("en_fa_step_of", "en", "This is step 2 of 5.", "S-01", "none"),
    ("en_fa_range", "en", "Fitting takes 2" + EN + "3 days.", "S-01", "none"),
    ("en_fa_code", "en", "```\nrate = 73%\nprice = $12,000\n```", "S-01", "none"),
    ("en_fa_every_second_counts", "en", "On a busy site every second counts.", "S-01", "none"),
    # --- S-02 ----------------------------------------------------------------------------------
    ("en_s02_studies", "en", "Studies show that short texts work better.", "S-02", "fail"),
    ("en_s02_experts_agree", "en", "Experts agree that video is the future.", "S-02", "fail"),
    ("en_s02_according_study", "en", "According to a recent study, customers read less.", "S-02", "fail"),
    ("en_s02_research_shows", "en", "Research shows that people skim.", "S-02", "fail"),
    ("en_s02_our_data", "en", "Our data shows that people skim.", "S-02", "none"),
    ("en_s02_sourced", "en", "Studies show that people skim ([study](https://example.org/s)).", "S-02", "none"),
    # --- S-03 ----------------------------------------------------------------------------------
    ("en_s03_says", "en", "Thomas Weber says content is everything.", "S-03", "tell"),
    ("en_s03_role", "en", "Marketing expert Thomas Weber says content is everything.", "S-03", "tell"),
    ("en_s03_according", "en", "According to Jane Miller, the trend will last.", "S-03", "tell"),
    ("en_s03_linked", "en", "[Thomas Weber](https://example.org/tw) says content is everything.", "S-03", "none"),
    ("en_s03_institution", "en", "Harvard Business Review notes that trust matters.", "S-03", "none"),
    ("en_s03_own_name", "en", "Anna Lane says we should start earlier.", "S-03", "none", {"own_names": ["Anna Lane"]}),
    # --- S-04 / S-06 / S-07 -------------------------------------------------------------------
    ("en_s04_generic", "en",
     "Good communication is the foundation of every successful relationship between a brand and its audience. Those who "
     "communicate clearly avoid misunderstandings, build trust and lay the groundwork for a long-term relationship that "
     "benefits both sides.", "S-04", "hint"),
    ("en_s04_concrete", "en",
     "Good communication made the difference for the carpenter in Leeds. In March I went through every enquiry with him, "
     "and we cut the reply time to one day, because otherwise customers would have asked a competitor, as he told me later.",
     "S-04", "none"),
    ("en_s06_advice", "en", "You should know your audience. You should post regularly. Make sure everything is right.", "S-06", "tell"),
    ("en_s06_example", "en", "You should know your audience, for example through calls. You should post regularly. Make sure everything is right.", "S-06", "none"),
    ("en_s07_leading", "en", "A leading company already uses the method.", "S-07", "tell"),
    ("en_s07_numerous", "en", "Numerous clients trust us.", "S-07", "tell"),
    ("en_s07_industry_leaders", "en", "Industry leaders rely on this approach.", "S-07", "tell"),
    # --- phrases -------------------------------------------------------------------------------
    ("en_p_fast_paced", "en", "In today's fast-paced world, every minute counts.", "P-01", "tell"),
    ("en_p_delve", "en", "We delved into the details.", "P-07", "tell"),
    ("en_p_testament", "en", "The result is a testament to hard work.", "P-20", "tell"),
    ("en_p_game_changer", "en", "This is a real game-changer.", "P-21", "tell"),
    ("en_p_tapestry", "en", "A rich tapestry of ideas.", "P-37", "tell"),
    ("en_p_cluster_single", "en", "We take a holistic view.", "P-26", "none"),
    ("en_p_cluster_pair", "en", "We take a holistic view and seamless steps.", "P-26", "tell"),
    ("en_p_leverage_inflected", "en", "We are leveraging data and fostering trust here.", "P-24", "tell"),
    ("en_p_context_hint", "en", "Planning is crucial.", "P-65", "hint"),
    ("en_p_allow_robust", "en", "We used robust standard errors and a test harness.", "P-36", "none"),
    ("en_p_allow_leverage_ratio", "en", "The leverage ratio and the robust regression are reported.", "P-24", "none"),
    ("en_p_landscape_mode", "en", "Turn the phone to landscape mode and seamless scrolling works, robust enough.", "P-38", "none"),
    ("en_p_in_quote", "en", "The client wrote: \"This was a real game-changer for us.\"", "P-21", "none"),
    ("en_p_blockquote", "en", "> In today's fast-paced world, every minute counts.", "P-01", "none"),
    ("en_p_user_allow", "en", "We take a holistic view and seamless steps.", "P-26", "none", {"allow": ["holistic"]}),
    # --- structure -----------------------------------------------------------------------------
    ("en_t01_once", "en", "It's not about reach. It's about trust.", "T-01", "hint"),
    ("en_t01_twice", "en", "It's not about reach. It's about trust. This is not a trick. This is craft.", "T-01", "tell"),
    ("en_t01_plain_not_but", "en", "We deliver not in the morning but in the evening.", "T-01", "none"),
    ("en_t02_two_in_paragraph", "en", "Good content is clear, concise and engaging. It builds trust, loyalty and revenue.", "T-02", "tell"),
    ("en_t02_single", "en", "We sell wood, glue and screws.", "T-02", "none"),
    ("en_t03_connectors", "en", "Moreover, it is cheap. Furthermore, it is fast. Additionally, it is quiet.", "T-03", "tell"),
    ("en_t03_single", "en", "The wood is dry. Moreover, it is cheap.", "T-03", "none"),
    ("en_t03_two_in_paragraph", "en", "Moreover, it is cheap. Furthermore, it is fast.", "T-03", "none"),
    ("en_t04_same", "en", "You plan the text. You write it. You check it afterwards.", "T-04", "tell"),
    ("en_t05_once", "en", "Why does this matter so much? Because customers compare.", "T-05", "hint"),
    ("en_t06_question_reveal", "en", "The result? More enquiries. The reason? Better texts.", "T-06", "tell"),
    ("en_t06_exclude_note", "en", "Note: read the text aloud.", "T-06", "none"),
    ("en_t07_pathos", "en", "We learned a lot.\n\nThe future belongs to those who act now.", "T-07", "tell"),
    ("en_t08_summary", "en", "First paragraph with content.\n\nAll in all, the effort pays off.", "T-08", "tell"),
    ("en_t09_tail_twice", "en", "Revenue rose, highlighting the importance of SEO. Traffic grew, underscoring the value.", "T-09", "tell"),
    # --- form ----------------------------------------------------------------------------------
    ("en_f01_em", "en", "The result " + EM + " more enquiries.", "F-01", "tell"),
    ("en_f01_em_fail_mode", "en", "The result " + EM + " more enquiries.", "F-01", "fail", {"dashes": "fail"}),
    ("en_f01_em_off", "en", "The result " + EM + " more enquiries.", "F-01", "none", {"dashes": "off"}),
    ("en_f01_em_quote", "en", "She said: \"The result " + EM + " more enquiries.\"", "F-01", "none"),
    ("en_f02_en_words", "en", "Fast " + EN + " and cheap.", "F-02", "tell"),
    ("en_f02_en_numbers", "en", "Pages 10" + EN + "20 cover this.", "F-02", "none"),
    ("en_f03_hyphen", "en", "Fast - and cheap.", "F-03", "tell"),
    ("en_f05_bold", "en", "**Important:** Use **clear** goals and **measurable** values.", "F-05", "tell"),
    ("en_f06_conclusion", "en", "## Conclusion\n\nText.", "F-06", "tell"),
    ("en_f06_what_is", "en", "## What Is Content Marketing?\n\nText.", "F-06", "tell"),
    ("en_f06_question_ok", "en", "## What does only this business know?\n\nText.", "F-06", "none"),
    ("en_f07_absent", "en", "You can test it. Try it yourself.", "F-07", "none"),
    ("en_f09_forbid", "en", "We have dynamic teams.", "F-09", "fail", {"forbid": ["dynamic"]}),
    ("en_f09_forbid_inflected", "en", "We are disrupting the market.", "F-09", "fail", {"forbid": ["disrupt"]}),
]


class EnglishCases(unittest.TestCase):
    pass


add_cases(EnglishCases, CASES)

if __name__ == "__main__":
    unittest.main()


class EnglishGuardrailCases(unittest.TestCase):
    pass


add_cases(EnglishGuardrailCases, [
    ("en_title_link_text", "en", "See [The Ultimate Guide to Screed](https://example.org/g) for details.", "P-43", "none"),
    ("en_title_quoted", "en", "Her book \"Unlock the Potential of Clay\" is short.", "P-15", "none"),
    ("en_title_url", "en", "Read https://example.org/delve-into-seo for more.", "P-07", "none"),
])
