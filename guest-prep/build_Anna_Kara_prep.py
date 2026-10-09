#!/usr/bin/env python
# Builds the KIRP interview prep .docx for Anna Kara, Anna Kara Loans / Equity Smart Home Loans (Burbank, CA)
# Built to prompts/06_interview_prep.md v5: research -> draft -> stress test + council -> EP polish
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# ---- base styles ----
normal = doc.styles['Normal']
normal.font.name = 'Calibri'
normal.font.size = Pt(10.5)
normal.paragraph_format.space_after = Pt(6)

for name, size, color in (('Heading 1', 18, 0x1F3864), ('Heading 2', 14, 0x2E5496), ('Heading 3', 11.5, 0x2E5496)):
    st = doc.styles[name]
    st.font.name = 'Calibri'
    st.font.size = Pt(size)
    st.font.color.rgb = RGBColor((color >> 16) & 255, (color >> 8) & 255, color & 255)
    st.font.bold = True

for s in doc.sections:
    s.top_margin = s.bottom_margin = Inches(0.7)
    s.left_margin = s.right_margin = Inches(0.8)


def h1(t): doc.add_heading(t, level=1)
def h2(t): doc.add_heading(t, level=2)
def h3(t): doc.add_heading(t, level=3)


def p(text='', bold=False, italic=False, size=None, space=6):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(space)
    r = par.add_run(text)
    r.bold, r.italic = bold, italic
    if size:
        r.font.size = Pt(size)
    return par


def rich(segments, style=None, space=6):
    par = doc.add_paragraph(style=style)
    par.paragraph_format.space_after = Pt(space)
    for seg in segments:
        text = seg[0]
        b = seg[1] if len(seg) > 1 else False
        i = seg[2] if len(seg) > 2 else False
        r = par.add_run(text)
        r.bold, r.italic = b, i
    return par


def bullet(text_bold, text_rest=''):
    par = doc.add_paragraph(style='List Bullet')
    par.paragraph_format.space_after = Pt(2)
    if text_bold:
        par.add_run(text_bold).bold = True
    if text_rest:
        par.add_run(text_rest)
    return par


def quoted(label, text):
    par = doc.add_paragraph(style='Intense Quote')
    par.paragraph_format.space_after = Pt(3)
    par.paragraph_format.space_before = Pt(3)
    r = par.add_run(label + ' ')
    r.bold = True
    r.italic = True
    r2 = par.add_run(text)
    r2.italic = True
    return par


def table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = 'Light Grid Accent 1'
    hdr = t.rows[0].cells
    for i, htxt in enumerate(headers):
        hdr[i].text = ''
        run = hdr[i].paragraphs[0].add_run(htxt)
        run.bold = True
        run.font.size = Pt(9.5)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ''
            par = cells[i].paragraphs[0]
            run = par.add_run(str(val))
            run.font.size = Pt(9.5)
    if widths:
        for r in t.rows:
            for i, w in enumerate(widths):
                r.cells[i].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def q(num, question, if_vague, reveals, serves, note=None, short=None, permission=None):
    rich([(str(num) + '. ', True), (question, True)], space=2)
    if short:
        par = doc.add_paragraph()
        par.paragraph_format.space_after = Pt(3)
        par.paragraph_format.left_indent = Inches(0.25)
        r = par.add_run('SAY THIS: ')
        r.bold = True
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
        r2 = par.add_run('"' + short + '"')
        r2.bold = True
        r2.font.size = Pt(10.5)
    if permission:
        quoted('First, say this:', '"' + permission + '"')
    quoted('If vague, ask:', if_vague)
    quoted('Ideal answer reveals:', reveals)
    quoted('Serves:', serves)
    if note:
        rich([('PRODUCER NOTE: ', True), (note, False, True)], space=2)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def bridge(text):
    rich([('BRIDGE TO NEXT BLOCK (read as written): ', True), ('"' + text + '"', False, True)])




LIVE_TITLE = "Your Buyer's Bank Said No. That's Not the Final Answer. (Anna Kara)"
LIVE_BACKUP = "Rates Are Back Over 7%. What a Loan Officer Wants Agents to Say Now (Anna Kara)"

# =====================================================================
# TITLE
# =====================================================================
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run('KEEPING IT REAL PODCAST')
r.bold = True
r.font.size = Pt(13)
r.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run('Interview Prep: Anna Kara')
r.bold = True
r.font.size = Pt(20)
sub2 = doc.add_paragraph()
sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub2.add_run('Loan Officer, Anna Kara Loans (a branch of Equity Smart Home Loans)  |  Burbank, CA  |  Target runtime 43 minutes')
r.italic = True
r.font.size = Pt(10)

# =====================================================================
# 1. QUICK REFERENCE CARD
# =====================================================================
h1('1. Quick Reference Card')
p('One page. Glance at this during the interview.', italic=True, space=8)

h3('Who she is')
bullet('Name: ', 'Anna Kara on air. Her site\'s award badge says Anna Karapetian; Armenian press spells it Karapetyan. Confirm pronunciation and which name she wants used before you hit record.')
bullet('Role: ', 'Loan officer and owner of Anna Kara Loans, a mortgage broker branch of Equity Smart Home Loans. Office at 4300 W. Magnolia Blvd, Burbank, CA. Serves Glendale, Burbank, Pasadena, Studio City, Sherman Oaks, North Hollywood.')
bullet('She is a broker, not a bank: ', 'she shops a file across many wholesale lenders (her site says 178+). That is why she sees the buyers a bank turned down. It is the whole episode.')
bullet('Loan programs: ', 'Conventional, jumbo, FHA, FHA 203k, USDA, HELOC, reverse, self-employed / non-QM, refinance.')
bullet('Story (her intake): ', 'Born in Armenia, moved to Los Angeles at 12. Started as a receptionist. Had her own boutique mortgage company by 20. 26 years in the business. Married to Ron; they flip and invest in real estate together. Mother of three.')
bullet('Giving back: ', 'The Anna Kara Foundation. Armenpress reported it has supported graduates of an orphanage in Vanadzor, Armenia, with plans for a shelter that teaches life and job skills.')
bullet('Guest type: ', 'C, service provider to agents. She is not a realtor. Every question asks what she sees from the lender\'s side that agents can\'t. Product rule: only Q16 touches the broker-vs-bank question, and it\'s framed as "how any agent vets any lender."')

h3('Verified (safe to say on air)')
bullet('Rates: ', 'Freddie Mac\'s 30-year crossed 7% (7.03%) the week of Sept 24, 2026, the first time since January 2025. It was 7.28% on Oct 1. A new number drops every Thursday. Check freddiemac.com/pmms the morning of and update Q5.')
bullet('Prior podcast: ', 'Top Producer Mindset (Equity Smart\'s own show), Ep. 7, Sept 12, 2024, "Building Your Brand as a Loan Officer." The listing calls her Equity Smart\'s reigning Top Producer of the Year.')
bullet('Her site\'s lines (OK to read as "your site says"): ', '"Your bank\'s answer is one answer. It is not the answer." / "When a lender goes quiet for three days during escrow, you lose real money."')

h3('Guest supplied, do not state as verified')
bullet('', '"Top 1% Mortgage Producer" and Scotsman Guide recognition. The badges are on her site, but we could not find her on Scotsman\'s published lists. Say "Scotsman Guide has recognized you" only if she confirms pre-show.')
bullet('', '26 years in the business (intake). Her site says "over two decades." Say "more than two decades" or let her say 26.')
bullet('', '2,500+ families helped and 178+ lenders. Site claims. Fine for her to say, not for you to state.')

h3('Episode')
bullet('The Core Topic: ', 'The deals agents give up on too early, seen from the lender\'s side: the buyer one bank said no to, the buyer waiting on rates, and the escrow that\'s quietly dying.')
bullet('Overasked questions to avoid: ', '"What\'s it like being a woman in a male-dominated industry?" "How did you build your personal brand?" "How are you using AI?" (all three were the 2024 Top Producer Mindset episode).')
bullet('The "I\'ve interviewed hundreds" moment: ', 'Q16 only. "I\'ve interviewed hundreds of agents, and most of them send buyers to the same lender for years without ever asking that lender one hard question."')
bullet('Live stream title: ', LIVE_TITLE + ' (' + str(len(LIVE_TITLE)) + ' characters)')
bullet('Watch out for: ', 'Rapid Fire will spend her best advice ("Don\'t wait for the perfect opportunity. Create it.") and worst advice ("Play it safe."). Say "Love it, and we\'re coming back to that." Callbacks are Q6 (play it safe) and Q13 (create it).')
bullet('Watch out for: ', 'If she tells the toddler story in Rapid Fire Q4, skip Q15 and use its backup.')
bullet('Watch out for: ', 'She\'s licensed in California. Don\'t imply she can take a Chicago referral. Ask pre-show which states she lends in.')
bullet('Drift guard: ', 'If she quotes LA prices or California programs, ask "What does that look like for a $350,000 buyer in the Midwest?"')
rich([('ASK THE SHORT VERSION.  COUNT TO THREE BEFORE YOU RESPOND.', True)], space=4)

doc.add_page_break()

# =====================================================================
# 2. EPISODE FRAMEWORK
# =====================================================================
h1('2. Episode Framework')
h2('2A. Title Options')
table(['#', 'Title', 'Why it works'], [
    ['1', 'Your Buyer\'s Bank Said No. Here\'s Why That\'s Not the Final Answer. (Anna Kara)', 'Names a moment every buyer\'s agent has lived. Opens a gap: what\'s the other answer?'],
    ['2', 'Rates Are Back Over 7%. What a Loan Officer Wants Every Agent to Say Right Now (Anna Kara)', 'Rides this month\'s headline. Verified number. Promises exact words.'],
    ['3', 'From Armenia at 12 to Her Own Mortgage Company at 20: Anna Kara on the Deals Agents Give Up On', 'Personality hook for the new-agent segment. Two numbers. Story-led.'],
], widths=[0.3, 3.9, 2.6])

h2('2B. Cold Open Hook')
p('"Somewhere in your database is a buyer who got turned down by one bank, and you moved on to the next one. Today\'s guest has spent more than two decades closing the loans other lenders said no to, and she says that no was one answer, not the answer. We\'re going to talk about that today. Stay tuned."', italic=True)

h2('2C. Episode Arc')
rich([('Core Topic: ', True), ('The deals agents give up on too early, seen from the lender\'s side of the table.', False)])
rich([('Why this topic: ', True), ('She can\'t teach listing presentations, but she can tell agents exactly which buyers and which escrows they\'re throwing away, and that is money every agent in every market is leaving on the table right now with rates over 7%.', False)])
table(['Block', 'Angle', 'Ends on'], [
    ['1', 'The bank\'s no isn\'t the answer', 'Three questions to ask a declined buyer'],
    ['2', '7% is back', 'Exact words for "we\'ll wait for rates to drop"'],
    ['3', 'When escrow goes sideways', 'What to do the day your lender goes quiet'],
    ['4', 'The lender\'s view of agents', 'The one question to ask any lender'],
], widths=[0.6, 2.8, 3.4])

doc.add_page_break()

# =====================================================================
# 3. INTERVIEW QUESTIONS
# =====================================================================
h1('3. Interview Questions')
p('Questions are numbered 1 to 16 across all blocks so you can call one out by number.', italic=True)

h2('Rapid Fire (0:00-2:00, read as written, no follow-ups)')
for i, rq in enumerate([
    'Best real estate advice you\'ve ever received?',
    'Worst real estate advice you\'ve ever received?',
    'One tool or app you can\'t run your business without?',
    'What would surprise people most about your day-to-day?',
], 1):
    rich([('RF' + str(i) + '. ', True), (rq, True)], space=2)
rich([('PRODUCER NOTE: ', True), ('She\'ll likely give "Don\'t wait for the perfect opportunity. Create it." and "Play it safe." Say "Love it, and we\'re coming back to that." Both are callbacks (Q6 and Q13). If RF4 turns into the toddler story, laugh, move on, and use the Q15 backup.', False, True)])

# ---------------- BLOCK 1 ----------------
h2('Block 1: The Bank\'s No Isn\'t the Answer (2:00-12:00)')
p('Audience note: Buyer\'s agents, who have all lost a buyer to one denial and never followed up.', italic=True)
p('Arc: the line, the size of it, the file, the honest limit, the three questions.', italic=True)

q(1, 'Your site has a line I want every agent listening to hear: "Your bank\'s answer is one answer. It is not the answer." Out of every ten buyers who come to you after a bank already said no, how many do you end up closing?',
  'Give me a number. Out of ten.',
  'The size of the pool agents are walking away from. A number makes agents go back through their old leads tonight.',
  'Individual agents, new agents',
  short='"Your bank\'s answer is one answer, not the answer." Out of ten bank denials, how many do you close?')

q(2, 'Walk me through the most common one. A self-employed buyer writes off everything, so the tax return looks tiny, but the bank account says they\'re doing great. The bank says no. What do you actually do with that file, step by step?',
  'What do you ask for on day one, and how fast do you know if it works?',
  'How bank statement loans work (12 to 24 months of deposits instead of the tax return), what documents, and the timeline. Also the other buyers agents give up on: newer credit, no Social Security number, condo buildings that don\'t qualify.',
  'Agents with entrepreneur and small-business clients',
  short='Self-employed buyer, tiny tax return, big deposits. The bank says no. What do you do?',
  note='If she quotes LA price ranges, use the drift guard: "What does that look like for a $350,000 buyer in the Midwest?"')

q(3, 'Now be honest about the catch. These loans usually cost more. Your own site says about half a point to a point higher on some of them. When do you tell a buyer: you can get this loan, but you shouldn\'t?',
  'Tell me about the last time you talked somebody out of a loan you could have closed.',
  'Her integrity line. This is what makes the whole block credible instead of a pitch.',
  'All segments',
  short='When do you tell a buyer, "You can get this loan, but you shouldn\'t"?')

q(4, 'An agent\'s buyer just texted them: "The bank turned us down." Before that agent moves on to the next buyer, what three questions should they ask?',
  'If they only get one question, which one tells you in ten seconds whether there\'s another path?',
  'A triage script any agent can use on any declined buyer, with any lender.',
  'Individual agents, new agents',
  short='Buyer texts, "The bank said no." What three questions does the agent ask?')

bridge('So one bank\'s no is the start of the conversation. But right now the bigger problem isn\'t buyers getting turned down. It\'s buyers who won\'t even apply, because rates just went back over 7%.')

# ---------------- BLOCK 2 ----------------
h2('Block 2: 7% Is Back (12:00-21:00)')
p('Audience note: Every agent with a buyer on the fence this fall.', italic=True)
p('Arc: the headline, the callback, the eye-roll, the exact words.', italic=True)

q(5, 'Freddie Mac\'s 30-year rate went back over 7% in late September for the first time since January of last year, and it was 7.28% on October 1st. What are buyers actually saying to you on the phone this week?',
  'What\'s the exact sentence you hear most on a first call right now?',
  'Real buyer psychology this month, in their words. This is the current-moment question.',
  'All segments',
  short='Rates just went back over 7%. What are buyers saying to you this week?',
  note='Update the rate with Thursday\'s Freddie Mac number before recording.')

q(6, 'In Rapid Fire you said the worst advice you ever got was "play it safe." A lot of agents are telling buyers right now that the safe move is to wait for rates to come down. Is waiting playing it safe, or is it the risky move?',
  'Run the math for me. $400,000 house, the buyer waits a year. What has to happen for waiting to win?',
  'The math of waiting (price changes, rent paid, the refi option) versus the feeling of waiting. The callback rewards listeners who caught Rapid Fire.',
  'Individual agents',
  short='Your worst advice was "play it safe." Is waiting for rates playing it safe?')

q(7, 'There\'s an agent listening who has heard "marry the house, date the rate" so many times they don\'t believe it anymore. What do you say to that agent?',
  'What\'s your break-even rule? How fast does a refinance have to pay for itself before you\'d recommend it?',
  'An honest answer on refinancing, and the break-even math she uses. This is the objection-said-out-loud question.',
  'Individual agents, team leaders',
  short='An agent is sick of "marry the house, date the rate." What do you tell them?')

q(8, 'A buyer says, "We\'re going to wait until rates drop." Give the agent the exact words. Not the philosophy. The sentence.',
  'Pretend I\'m the buyer. Say it to me.',
  'A word-for-word script an agent can use on their next call.',
  'Individual agents, new agents',
  short='Buyer says, "We\'ll wait for rates to drop." What are the exact words?',
  note='If she gives a philosophy, use the if-vague line and make her role-play it with you. That\'s the clip.')

bridge('So that\'s how you get a buyer to apply. Now let\'s talk about what happens after, because the deal you lose in escrow hurts a lot more than the one that never started.')

# ---------------- BLOCK 3 ----------------
h2('Block 3: When Escrow Goes Sideways (21:00-31:00)')
p('Audience note: Every producing agent, and team leaders who run transaction coordination.', italic=True)
p('Arc: the frozen deal, the hero trap, the preventable kills, the day the lender goes quiet.', italic=True)

q(9, 'You told us about a deal where a government agency froze your borrower\'s money in the middle of escrow, and you spent about six weeks waiting on federal clearance. When it finally closed, they blamed you for how long it took. What happened?',
  'What did you do in week one that you\'d do differently now?',
  'The story, and the moment she realized that absorbing all the stress kept the client from understanding their own problem.',
  'All segments',
  short='A federal agency froze your buyer\'s money mid-escrow. What happened?',
  permission='Without naming anyone, I want to ask about the deal you mentioned in your notes.',
  note='Ask pre-show: was this commercial or residential, and which agency? Her intake says commercial. Do not read her intake wording back to her. Let her tell it fresh.')

q(10, 'You said the lesson was moving from "I\'ll fix this" to "here is the reality of your situation." Agents have the exact same hero problem. Where\'s the line between protecting your client and hiding the truth from them?',
  'What\'s the sentence you say now that you didn\'t say back then?',
  'How to deliver bad news early. This is the most transferable idea in the episode. Count to three after she answers.',
  'Individual agents, team leaders',
  short='"I\'ll fix this" versus "here\'s the reality." Where\'s the line?')

q(11, 'From your seat, what do buyers do during escrow that blows up a loan, that their agent could have stopped with one warning on day one?',
  'Give me the one you saw most recently.',
  'The "don\'t do this until we close" list: new car, new credit card, moving money around, changing jobs. The real story behind one of them.',
  'New agents, individual agents',
  short='What do buyers do in escrow that kills the loan, that agents could have prevented?')

q(12, 'Your site says when a lender goes quiet for three days during escrow, you lose real money. So what should an agent expect to hear from their lender every week, and what should they do the day the lender goes quiet?',
  'Who does the agent call, and what do they say?',
  'A weekly update standard agents can demand from any lender, and the escalation move when it breaks.',
  'Individual agents, team leaders',
  short='Your lender goes quiet for three days. What does the agent do?')

bridge('So you know what to expect from a great lender. Let\'s flip it, because you\'ve been watching agents from the lender\'s side for more than two decades, starting at a receptionist\'s desk.')

# ---------------- BLOCK 4 ----------------
h2('Block 4: The Lender\'s View of Agents (31:00-40:00)')
p('Audience note: New agents (how to earn a lender\'s trust) and team leaders and broker-owners (how to pick a preferred lender).', italic=True)
p('Arc: the 20-year-old, the 9 p.m. file, the laugh, the one question.', italic=True)

q(13, 'You came here from Armenia at 12, started as a receptionist, and had your own mortgage company at 20. Your best advice was "Don\'t wait for the perfect opportunity. Create it." So how does a 20-year-old get her first real estate agent to trust her with a buyer?',
  'Who told you that you were too young, and what did you say back?',
  'How she earned her first referral partner with no track record. That is exactly the new agent\'s problem in reverse.',
  'New agents',
  short='Your own company at 20. How did you get your first agent to trust you with a buyer?',
  note='This is her #1 requested topic. Give it this one question. If she goes to being a woman in a male-dominated industry here, let it run a minute. It fits here and nowhere else.')

q(14, 'Which agents get your best effort? Not your best referrals. Your best effort at 9 p.m. when a file is on fire. What do those agents do differently?',
  'And what does an agent do that makes you never want to work with them again?',
  'The behaviors that make a lender go the extra mile, and the ones that quietly get an agent dropped.',
  'Individual agents, team leaders',
  short='Which agents get your best effort at 9 p.m.? What do they do differently?')

q(15, 'I have to ask about the funniest application you ever took. A borrower standing up, nursing her toddler, while she read you her monthly income and her bank accounts. How did you keep a straight face?',
  'What did you say to her when it was done?',
  'A laugh to re-hook the last ten minutes, and a reminder that buyers bring their whole lives to the table.',
  'All segments',
  short='Tell me about the loan application with the toddler.',
  note='If she already told this in Rapid Fire, use the backup: "What\'s the strangest thing a buyer ever handed you as paperwork?"')

q(16, 'I\'ve interviewed hundreds of agents, and most of them send buyers to the same lender for years without ever asking that lender one hard question. You\'ve written nine questions for vetting a lender. If an agent could only ask one, which one?',
  'And what answer to that question is a red flag?',
  'One question any agent can ask any lender this week, with what a good and bad answer sound like.',
  'Individual agents, team leaders, broker-owners',
  short='An agent gets to ask their lender one hard question. Which one?',
  note='This is the only broker-vs-bank question. Keep it about vetting any lender, not about why her model is better.')

h2('The Close (40:00-43:00)')
h3('Homework (read verbatim)')
p('"Here\'s what I want you to do before the next episode. Go through your database and find three buyers from the last year who told you their bank said no, or who went quiet after they got pre-approved. Text each one: \'Hey, quick question. When you got turned down, did anyone shop your file with other lenders? There might be another path. Want me to connect you with someone who\'d take a look?\' Three texts. Not next month. This week."', italic=True)
h3('Guest close')
bullet('', '"Where can people find you, follow you, and work with you?"')
bullet('', 'annakaraloans.com  |  Instagram and Facebook: @annakaraloans  |  TikTok: @annakaraloan')
bullet('', 'Do not read her cell on air. Point people to the website.')
bullet('', 'Ask pre-show if she has a resource for agents (a "what to tell your buyers in escrow" sheet would be perfect for Q11).')

h3('If you\'re running long, cut these first')
bullet('1. Q15 (toddler story). ', 'Pure entertainment. It may already come out in Rapid Fire.')
bullet('2. Q11 (escrow loan killers). ', 'The list exists elsewhere. Ask her to share it after the show.')
bullet('3. Q7 (marry the house). ', 'Q6 already covers the waiting argument.')
bullet('4. Q14\'s if-vague follow-up. ', 'Keep the question, drop the "never work with again" follow-up.')

h3('Never cut')
bullet('Q1 ', 'the core idea of the episode.')
bullet('Q4 ', 'the do-it-tomorrow for declined buyers.')
bullet('Q8 ', 'the exact words, and the clip.')
bullet('Q10 ', 'the most transferable idea in the episode.')
bullet('Q13 ', 'the only question that costs her something personal.')

doc.add_page_break()

# =====================================================================
# 4. RESEARCH BRIEF
# =====================================================================
h1('4. Research Brief')
p('Read this the morning of, not during the interview.', italic=True)

h2('4A. Background')
p('Anna Kara was born in Armenia and moved to Los Angeles at 12. She started in mortgages as a receptionist and had her own boutique mortgage company by 20. She now runs Anna Kara Loans in Burbank as a branch of Equity Smart Home Loans, a California mortgage broker, and says she has 26 years in the business. She and her husband Ron invest in and flip real estate, she has three kids, and she runs the Anna Kara Foundation, which supports orphanage graduates in Armenia. She is not a realtor.')

h2('4B. Career Timeline')
p('Only dated entries we could confirm. We found no dates for her receptionist start, her first company, or joining Equity Smart.', italic=True)
table(['Year', 'Role / Company', 'Notable'], [
    ['Post-2018 (exact year unknown)', 'Anna Kara Foundation', 'Met with Anna Hakobyan, spouse of Armenia\'s acting PM, about the foundation\'s orphanage-graduate work in Vanadzor (Armenpress).'],
    ['Sept 2024', 'Equity Smart Home Loans', 'Guest on Top Producer Mindset, Ep. 7. Listing calls her Equity Smart\'s reigning Top Producer of the Year. Hosted an "Elevate Your Personal Brand" event in Glendale, Sept 26, 2024.'],
    ['Jul-Oct 2026', 'Anna Kara Loans', '20 blog posts on LA lending: non-QM, refinancing, first-time buyers, vetting a broker.'],
], widths=[1.4, 1.7, 3.7])

h2('4C. What Makes Her Interesting for This Audience')
bullet('She sees the buyers agents give up on: ', 'as a broker shopping files across many lenders, she gets the self-employed, thin-credit and ITIN buyers a bank declined. Every agent has some of those in their database right now.')
bullet('She lives in the rate headline: ', 'the 30-year just crossed 7% again. She hears the buyer\'s reaction before the agent does.')
bullet('She\'s been burned by being the hero: ', 'the frozen-asset deal is a lesson about delivering bad news early that applies directly to agents.')
bullet('She started with nothing: ', 'immigrant at 12, receptionist, own company at 20. A real "how do I get my first referral partner" story for new agents.')
bullet('She invests: ', 'she and Ron flip properties, so she can speak to investor clients if time allows.')

h2('4D. Key Data Points')
table(['Stat', 'Source', 'Confidence'], [
    ['Freddie Mac 30-year: 7.03% (Sept 24, 2026), first time over 7% since Jan 2025', 'Trading Economics, citing Freddie Mac PMMS', 'High (re-check Thursday)'],
    ['Freddie Mac 30-year: 7.28% (Oct 1, 2026), up from 6.34% a year earlier', 'Trading Economics, citing Freddie Mac PMMS', 'High (re-check Thursday)'],
    ['MBA Purchase Index 145.1 (Oct 2), down from 148.2', 'Newsquawk', 'Medium'],
    ['Non-QM loans often 0.5% to 1% above conventional (non-warrantable condos)', 'Her blog, Aug 26, 2026', 'Her claim'],
    ['96 Google reviews analyzed for her "what borrowers worry about" post', 'Her blog, Aug 15, 2026', 'Her claim'],
    ['Purchase loans close in 21 to 30 days; jumbo and non-QM 30 to 45', 'Her blog, Aug 15, 2026', 'Her claim'],
    ['178+ lenders; 2,500+ families; top 1% producer', 'annakaraloans.com', 'Unverified'],
    ['Scotsman Guide Top Originators and Top Women Originators', 'Badges on her site; not found on Scotsman lists', 'Unverified'],
    ['26 years in the business', 'Her intake (site says "over two decades")', 'Guest supplied'],
    ['NMLS #1241473 (Anna Kara Loans); Equity Smart NMLS #856170', 'annakaraloans.com footer', 'Medium'],
], widths=[3.2, 2.3, 1.3])

h2('4E. Previous Media Appearances')
bullet('Top Producer Mindset, Ep. 7 (Sept 12, 2024): ', '"Building Your Brand as a Loan Officer." Hosted by Pablo, produced by Equity Smart. Covered being a top producer as a woman in a male-dominated industry, AI, and brand recognition.')
bullet('Armenpress (date unknown, post-2018): ', 'Foundation meeting with the acting PM\'s spouse. Not a mortgage interview.')
bullet('No prior Keeping It Real appearance. ', 'We searched the KIR archive.')
bullet('Overasked: ', 'woman in a male-dominated industry, personal branding, AI. We avoid all three as questions. She can bring the first one up in Q13.')

h2('4F. Their Own Words')
p('The blog is high-volume and reads like SEO content, so she may not recognize her own sentences. Say "your site says," never "you wrote." Her intake is primary, but answers 3 and 4 read like reactions to stories rather than the stories, so treat those as paraphrase.', italic=True)
table(['Quote', 'Where and when', 'Confidence', 'How D.J. uses it'], [
    ['"Your bank\'s answer is one answer. It is not the answer."', 'Her blog, Aug 15, 2026', 'Verbatim (her site)', 'Opens Q1.'],
    ['"None of these things make someone a bad borrower. They make them a bad fit for a bank."', 'Her blog, Aug 26, 2026', 'Verbatim (her site)', 'Hold for Q2 if she gets technical. Read it back and ask her to explain it to a buyer.'],
    ['"When a lender goes quiet for three days during escrow, you lose real money."', 'Her blog, Aug 15, 2026', 'Verbatim (her site)', 'Opens Q12.'],
    ['"Playing it safe can sometimes be the riskiest thing you do."', 'Her intake', 'Verbatim', 'Hold for Q6 if she hedges on waiting for rates.'],
    ['Moving from "I\'ll fix this" to "here is the reality of your situation" is how you protect your peace.', 'Her intake', 'Paraphrase', 'Q10. Paraphrase it out loud ("you said something like...").'],
], widths=[2.3, 1.4, 1.2, 1.9])

h2('4G. Audience Relevance')
table(['Segment', 'What they get'], [
    ['Individual agents', 'Three questions for a declined buyer, exact words for "we\'ll wait for rates," and a lender update standard to demand.'],
    ['Team leaders', 'A bad-news-early rule for the team and a lender-vetting question for picking a preferred lender.'],
    ['Broker-owners', 'A one-question test for any lender partner they recommend to their agents.'],
    ['New agents', 'How a 20-year-old earned her first referral partner, and the escrow mistakes to warn buyers about on day one.'],
], widths=[1.5, 5.3])

doc.add_page_break()

# =====================================================================
# 5. LIVE STREAM
# =====================================================================
h1('5. Live Stream Title, Descriptions and Hashtags')
h2('5A. Live Stream Title')
rich([('Live stream title: ', True), (LIVE_TITLE + ' (' + str(len(LIVE_TITLE)) + ' characters)', False)])
rich([('Backup: ', True), (LIVE_BACKUP + ' (' + str(len(LIVE_BACKUP)) + ' characters)', False)])
p('This does not have to match the published episode title. Pick that after you hear the interview.', italic=True)

h2('5B. Platform Descriptions')
rich([('Facebook: ', True), ('Your buyer\'s bank said no. Most agents move on. Loan officer Anna Kara says that\'s the most expensive mistake in your database, and she\'s here to show you what to do instead, plus what to say now that rates are back over 7%. Drop your questions in the comments!', False)])
rich([('Instagram: ', True), ('One bank\'s no is not the final answer. Live with loan officer @annakaraloans. #KeepingItReal #RealEstatePodcast #MortgageTips', False)])
rich([('TikTok: ', True), ('Your buyer got denied? Don\'t move on yet. #realtortips #mortgage #realestateagent', False)])
rich([('YouTube: ', True), ('Loan officer Anna Kara joins the Keeping It Real Podcast to explain why a bank denial isn\'t the end of a deal, how self-employed and non-traditional buyers still get approved, and what agents should tell buyers now that mortgage rates are back over 7%.', False)])
rich([('LinkedIn: ', True), ('Agents lose deals they never had to lose: the buyer one bank declined, the buyer waiting on rates, the escrow where the lender went quiet. Loan officer Anna Kara walks through each one from the lender\'s side and gives agents the exact steps to keep those deals alive.', False)])

h2('5C. Hashtags')
bullet('Universal: ', '#KeepingItReal #RealEstatePodcast #DJParis #RealtorLife #RealEstateAgent')
bullet('Episode: ', '#MortgageTips #LoanOfficer #NonQM #FirstTimeHomeBuyer #MortgageRates #RealtorTips #SelfEmployedBuyer')
bullet('Guest tags: ', 'Instagram and Facebook @annakaraloans, TikTok @annakaraloan, LinkedIn /in/annakaraloans')

# =====================================================================
# 6. YOUTUBE CHAPTERS
# =====================================================================
h1('6. YouTube Chapter Markers')
table(['Timestamp', 'Chapter title'], [
    ['0:00', 'Your Buyer Got Denied. That\'s Not the Final Answer.'],
    ['2:00', 'Rapid Fire: Best and Worst Advice From a Top Loan Officer'],
    ['4:00', 'How Many Bank Denials Can Still Close?'],
    ['6:00', 'How Self-Employed Buyers Get Approved'],
    ['8:30', 'When a Buyer Shouldn\'t Take the Loan They Qualify For'],
    ['10:00', '3 Questions to Ask a Buyer the Bank Turned Down'],
    ['12:00', 'Mortgage Rates Back Over 7%: What Buyers Are Saying'],
    ['14:30', 'Is Waiting for Rates to Drop Actually Safe?'],
    ['17:00', 'Does "Marry the House, Date the Rate" Still Work?'],
    ['19:00', 'Exact Words When a Buyer Wants to Wait on Rates'],
    ['21:00', 'The Deal Where the Government Froze the Buyer\'s Money'],
    ['24:00', 'How to Deliver Bad News to a Client Early'],
    ['26:30', 'What Buyers Do in Escrow That Kills the Loan'],
    ['28:30', 'What to Do When Your Lender Goes Quiet'],
    ['31:00', 'Her Own Mortgage Company at 20: How She Got Her First Agent'],
    ['34:00', 'Which Agents Get a Lender\'s Best Effort'],
    ['36:30', 'The Funniest Loan Application Ever'],
    ['38:00', 'The One Question to Ask Any Lender'],
    ['40:00', 'Homework and Where to Find Anna Kara'],
], widths=[1.0, 5.8])

doc.add_page_break()

# =====================================================================
# 7. STRESS TEST, COUNCIL, EP POLISH
# =====================================================================
h1('7. Stress Test, Council Review and EP Polish')
h2('7A. Stress Test')
table(['#', 'What broke', 'Fix applied'], [
    ['1', 'Name conflict: Anna Kara, Karapetian (site badge), Karapetyan (Armenpress).', 'Doc uses Anna Kara. Card tells D.J. to confirm name and pronunciation pre-show.'],
    ['2', 'Unverifiable: "Top 1%" and Scotsman Guide. Badges on her site, but not found on Scotsman\'s lists.', 'Marked guest-supplied. Kept out of titles, cold open and descriptions.'],
    ['3', 'Fact conflict: 26 years (intake) vs "over two decades" (site).', 'All D.J. copy says "more than two decades." She can say 26.'],
    ['4', 'Her blog is high-volume SEO content (20 posts in 10 weeks). She may not own the exact wording.', 'Q1, Q3 and Q12 say "your site says," never "you wrote." Noted in 4F.'],
    ['5', 'Intake answers 3 and 4 read like reactions to her stories, not the stories. Key details missing (commercial or residential, which agency).', 'Q9 asks her to tell it fresh. Pre-show check added. Intake wording downgraded to paraphrase in 4F.'],
    ['6', 'Spent questions: best and worst advice come out in Rapid Fire.', 'Callbacks built into Q6 ("play it safe") and Q13 ("create it"). Line on the card.'],
    ['7', 'Spent question: RF4 may pull the toddler story.', 'Q15 has a backup question.'],
    ['8', 'Drift risk 1: LA prices and California programs. KIR\'s audience is national, mostly Chicago.', 'Drift-guard line on the card and on Q2.'],
    ['9', 'Drift risk 2: her #1 requested topic is the immigrant-to-entrepreneur story, which could eat a block.', 'Contained to Q13 and tied to the core topic (earning an agent\'s trust).'],
    ['10', 'Rate number goes stale every Thursday.', 'Q5 note and card tell D.J. to re-check Freddie Mac PMMS the morning of.'],
    ['11', 'Licensing: she\'s California-based. Listeners may assume she can take their referral.', 'Card tells D.J. not to imply it and to ask her states pre-show.'],
    ['12', 'Product rule: a broker guest can turn every answer into "use a broker, not a bank."', 'Only Q16 touches it, framed as vetting any lender. Q4 homework says "someone," not "a broker."'],
    ['13', 'Dodgeable: Q1 can be answered "a lot." Q8 can be answered with philosophy.', 'Q1 demands a number out of ten. Q8 follow-up makes her role-play it.'],
    ['14', 'Gotcha risk: Q7 could feel like an attack on her industry. Q9 involves a client who blamed her.', 'Q7 is framed as the agent\'s doubt, not a claim about lenders. Q9 gets "without naming anyone."'],
    ['15', 'Runtime: 16 questions plus Rapid Fire is at the ceiling.', 'Four-item cut list. Q15 cuts first.'],
], widths=[0.3, 3.1, 3.4])

h2('7B. Council Review')
h3('Member notes')
table(['Member', 'What they\'d change'], [
    ['Hormozi', 'Q4 and Q8 are the money. Every agent leaves with three questions and one sentence. Protect both.'],
    ['Donald Miller', 'She\'s the guide, not the hero. The hero is the agent with a declined buyer in their CRM. The homework proves it.'],
    ['Byron Lazine', 'Rates over 7% is the take this month. Don\'t bury it in Block 2. It belongs in the backup title and the YouTube description.'],
    ['Brendan Kane', 'Title 1 is a concept hook. Title 2 is a stat hook. Test them against each other.'],
    ['Eric Simon', 'The toddler application is the share. Every agent has a "client did WHAT on the call" story.'],
    ['Chris Do', 'Q13 is the only question that costs her something. Q9 is close. Don\'t cut either for time.'],
    ['Jon Youshaei', 'The chapters read like search queries. "What to Do When Your Lender Goes Quiet" will pull search on its own.'],
], widths=[1.5, 5.3])
p('The disagreement: Byron wants to open with the 7% headline because it\'s timely. Miller wants the "bank said no" idea because it lasts after rates move. Decision: lead the title and cold open with "bank said no" because it won\'t date the episode, and use the 7% title as the A/B and the live-stream backup.', italic=True)

h3('Title (pick one, keep others for A/B)')
table(['#', 'Title', 'Ingredient', 'Curiosity mechanism'], [
    ['1', 'Your Buyer\'s Bank Said No. Here\'s Why That\'s Not the Final Answer. (Anna Kara)', 'Insight', 'Opens with a loss the agent already had, then promises another answer.'],
    ['2', 'Rates Are Back Over 7%. What a Loan Officer Wants Every Agent to Say Right Now (Anna Kara)', 'Stat', 'Headline anxiety, then a promise of exact words.'],
    ['3', 'From Armenia at 12 to Her Own Mortgage Company at 20: Anna Kara on the Deals Agents Give Up On', 'Personality', 'How does a 20-year-old do that?'],
], widths=[0.3, 3.3, 1.2, 2.0])
p('Recommended: #1. It holds up after rates move, and it speaks to a problem every buyer\'s agent already has.', italic=True)

rich([('Cold-open hook (sharpened): ', True), ('"Somewhere in your database is a buyer who got turned down by one bank, and you moved on to the next one. Today\'s guest has spent more than two decades closing the loans other lenders said no to, and she says that no was one answer, not the answer. We\'re going to talk about that today. Stay tuned."', False, True)])

h3('The Clip Engine')
table(['Q#', 'Question', 'Berger emotion', 'Heath gap'], [
    ['8', 'Buyer says, "We\'ll wait for rates to drop." What are the exact words?', 'Anxiety, then relief', 'Every agent wants the sentence they dread needing.'],
    ['9', 'A federal agency froze your buyer\'s money mid-escrow. What happened?', 'Anxiety, indignation', 'Unusual setup. The twist is she got blamed.'],
    ['15', 'Tell me about the loan application with the toddler.', 'Amusement', 'Absurd setup with an instant payoff.'],
], widths=[0.4, 2.8, 1.6, 2.0])

h3('Live-description scrub')
table(['Platform', 'Verdict and fix'], [
    ['Facebook', 'Keep. Leads with the agent\'s problem and ends on comments.'],
    ['Instagram', 'Keep. Short and tags her.'],
    ['TikTok', 'Keep. One line, written as a question to the agent.'],
    ['YouTube', 'Fixed. Added "mortgage rates back over 7%" for search, per Byron.'],
    ['LinkedIn', 'Keep. Business framing: three deals agents lose.'],
], widths=[1.3, 5.5])

rich([('Arc fix: ', True), ('The sag risk is the start of Block 4 if Q13 becomes a 10-minute life story. Q13\'s short version forces it to "how did you get your first agent," and Q15 re-hooks with a laugh before the close.', False)])
h3('Why it should work')
bullet('Curiosity (Heath): ', 'Every agent thinks a denial is final. "One answer, not the answer" breaks that.')
bullet('Share driver (Berger): ', 'Agents will forward Q8\'s script to their team and the toddler clip to their friends.')
bullet('Retention (MrBeast): ', 'Every block ends on something to do tomorrow, and Rapid Fire sets up two callbacks.')
rich([('The dissent: ', True), ('Byron still thinks the 7% title wins this month. A/B title 2 against title 1 on the YouTube thumbnail test and see whether timeliness beats evergreen.', False)])

h2('7C. EP Polish (pass 3)')
bullet('', 'Changed every "you wrote" to "your site says" after the stress test flagged the blog as likely ghostwritten.')
bullet('', 'Rewrote Q9 so she tells the frozen-asset story fresh instead of D.J. reading her intake back to her.')
bullet('', 'Moved the immigrant story out of the opener and into Q13, tied to earning an agent\'s trust, so it serves the core topic.')
bullet('', 'Reframed Q7 from a claim about lenders to the listening agent\'s doubt, so it doesn\'t read as an ambush.')
bullet('', 'Pulled "Top 1%" and Scotsman Guide out of every title, the cold open, and the descriptions.')
bullet('', 'Added the drift-guard line ("$350,000 buyer in the Midwest") so LA numbers translate for a Chicago audience.')
bullet('', 'Rewrote the homework so the text says "someone" and not "a broker," so it isn\'t a pitch for her business model.')
bullet('', 'Added permission language to Q9 only.')

doc.save("/Users/djparis/GitHub Projects/keeping-it-real-content-system/guest-prep/Anna_Kara_Interview_Prep.docx")
print("Saved Anna_Kara_Interview_Prep.docx")
