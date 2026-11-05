#!/usr/bin/env python
# Builds the KIRP interview prep .docx for Nick Schlekeway, Amherst Madison Real Estate Advisors (Boise, ID)
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




LIVE_TITLE = "Why Rigid Time Blocks Fail, and What Top Producers Do Instead (Nick Schlekeway)"
LIVE_BACKUP = "Firefighter to Brokerage Founder: The System Top Agents Run On (Nick Schlekeway)"

# =====================================================================
# TITLE
# =====================================================================
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run('KEEPING IT REAL WITH D.J. PARIS')
r.bold = True
r.font.size = Pt(13)
r.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run('Interview Prep: Nick Schlekeway')
r.bold = True
r.font.size = Pt(20)
sub2 = doc.add_paragraph()
sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub2.add_run('Founder and CEO, Amherst Madison Real Estate Advisors  |  Boise, ID  |  Target runtime 43 minutes')
r.italic = True
r.font.size = Pt(10)

# =====================================================================
# 1. QUICK REFERENCE CARD
# =====================================================================
h1('1. Quick Reference Card')
p('One page. Glance at this during the interview.', italic=True, space=8)

h3('Who he is')
bullet('Name: ', 'Nick Schlekeway (some outlets misspell it "Schleckaway"). Confirm pronunciation pre-show.')
bullet('Role: ', 'Founder and CEO of Amherst Madison Real Estate Advisors, Boise. Founded 2013. Independent, locally owned, no outside investors. Offices in Boise and McCall (2022 press also listed Eagle and Hidden Springs). About 170 agents per his own site.')
bullet('Before real estate: ', 'Boise State football, defensive end from Eagle, Idaho. Started all 13 games in 2006 and played on the 2007 Fiesta Bowl team. Then a Boise firefighter. Master\'s in real estate from Georgetown, summa cum laude.')
bullet('Writing: ', 'Inman contributor since 2017, about 40 bylines (four pillars of service, the 411 referral model, the Thermostat Effect, "asset vs. income"). Writes The Signal, a weekly newsletter. Book: The Essential Agent.')
bullet('Community: ', 'Make-A-Wish Idaho board. Founded A Giving Circle (over $600,000 raised for Treasure Valley nonprofits, per Boise State).')
bullet('KIR connection: ', 'No prior Nick appearance. Elliot Hoyte, an Amherst Madison agent, was on KIR in May 2020 ("How A Defensive Lineman Became A Top Real Estate Agent"). Two D-linemen from the same brokerage. Ask Nick pre-show if Elliot is still with him.')
bullet('Guest type: ', 'D (coach/author) with B (broker-owner) behind it. The questions push for frameworks agents can install. Broker shop talk is held to one bonus question.')

h3('Verified (safe to say on air)')
bullet('', 'Founded Amherst Madison in 2013. RealTrends Top 500 for the first time in 2022 at No. 342, based on 2021 volume, one of two independent Idaho brokerages on the list.')
bullet('', 'Inc. 5000: No. 715 in 2018 and No. 28 in 2019. Company press titled the 2019 list "No. 1 in Real Estate Category."')
bullet('', 'Boise State 2025 COBE Outstanding Alumni.')
bullet('', 'His own line (Inman, Feb 10, 2026): "I cannot recruit on promises anymore."')

h3('Guest supplied, do not state as verified')
bullet('', 'Lifetime sales: his intake and company bio say $6B; his personal site says $7B. Say "billions in sales" or let him say the number.')
bullet('', 'National rank: "Top 1%" (intake, Inman bio), "top 0.05%" (company bio), and "top 0.4%" (his own 2022 quote about the RealTrends 500). Don\'t say any of them. Let him.')
bullet('', '"#1 luxury brokerage in Idaho": on his site, no ranking body named.')
bullet('', 'Denali and Rainier summits, football captain, "Agent Operating System": intake only (captain is also in the Boise State bio). Fine to ask about, not to state as fact.')
bullet('', 'Book release: Kindle listed Oct 4, 2026, hardcover Jan 4, 2027, his site said August 2026. Ask pre-show whether it\'s out and where listeners should buy it.')

h3('Episode')
bullet('The Core Topic: ', 'The Agent Operating System, in his own terms: the calendar, the business plan and the CRM, plus the proof and the client journey that run on them. What top producers do that nobody teaches.')
bullet('Overasked questions to avoid: ', '"Average is invisible" and the "rookie mentality" (a full Real Estate Insiders Unfiltered episode, Sept 14, 2026). "How did a firefighter become a broker?" (Idaho Cutthroat Business podcast 2022, his own 2023 Inman piece). Downtown Boise development (Idaho Business Review 2020).')
bullet('The "I\'ve interviewed hundreds" moment: ', 'Q5 only. "I\'ve interviewed hundreds of agents, and almost every one has written a business plan. Almost none of them could tell me what\'s in it by March."')
bullet('Live stream title: ', LIVE_TITLE + ' (' + str(len(LIVE_TITLE)) + ' characters)')
bullet('Watch out for: ', 'Rapid Fire will spend both of his advice answers. Worst advice ("time block every hour of your day") is the hook for Block 1. Say "Love it, and we\'re coming back to that." Best advice ("hire slow, fire fast") is the bonus question, only if there\'s time.')
bullet('Pre-show check: ', 'Ask him to confirm the "30 offers in six months, none accepted" story. It came from an article the podcast hosts wrote, not from him.')
bullet('Watch out for: ', 'If RF4 pulls the Zillow buyer story, skip Q8 and go straight to Q9 (how he built the skill).')
bullet('Drift guard: ', 'He runs a brokerage and you recruit for one. If it turns into broker shop talk, say "Bring it back to the agent listening. What do they do Monday?"')
rich([('ASK THE SHORT VERSION.  COUNT TO THREE BEFORE YOU RESPOND.', True)], space=4)

doc.add_page_break()

# =====================================================================
# 2. EPISODE FRAMEWORK
# =====================================================================
h1('2. Episode Framework')
h2('2A. Title Options')
table(['#', 'Title', 'Why it works'], [
    ['1', 'Why Rigid Time Blocks Fail: The Operating System Top Producers Actually Run On (Nick Schlekeway)', 'Contrarian to the most common advice agents get, without overclaiming. Opens a gap: what instead?'],
    ['2', 'Your Clients Don\'t Believe You Yet. A Brokerage Founder on How to Prove It (Nick Schlekeway)', 'Names a fear every agent has after the buyer-agreement rules. Promises a fix.'],
    ['3', 'From Boise Firefighter to Brokerage Founder: The System Nobody Teaches Agents (Nick Schlekeway)', 'Personality hook. Story first, system second.'],
], widths=[0.3, 3.9, 2.6])

h2('2B. Cold Open Hook')
p('"The most common productivity advice in real estate is to time block every hour of your day. Today\'s guest built one of the top independent brokerages in the country, and he says that advice is the worst he ever got. We\'re going to talk about that today. Stay tuned."', italic=True)

h2('2C. Episode Arc')
rich([('Core Topic: ', True), ('The Agent Operating System: what top producers run on that nobody teaches, installed one piece at a time.', False)])
rich([('Why this topic: ', True), ('"Average Is Invisible" was covered in full two months ago on another show. The operating system is new and it\'s the spine of his book. Blocks 1 and 2 cover his own four parts (calendar, habits, plan, CRM). Blocks 3 and 4 cover his second and fourth suggested topics, which are what the system is for. Every block ends on something an agent can install this week.', False)])
table(['Block', 'Angle', 'Ends on'], [
    ['1', 'The calendar: energy, not time blocks', 'Rebuilding tomorrow around your sharpest hours'],
    ['2', 'The plan and the CRM', 'The one number to check every Friday'],
    ['3', 'Proof over promise', 'One piece of proof to build this week'],
    ['4', 'Clients for Life', 'What to do in the 30 days after closing'],
], widths=[0.6, 2.8, 3.4])

doc.add_page_break()

# =====================================================================
# 3. INTERVIEW QUESTIONS
# =====================================================================
h1('3. Interview Questions')
p('Questions are numbered 1 to 15 across all blocks, plus one bonus, so you can call one out by number.', italic=True)

h2('Rapid Fire (0:00-2:00, read as written, no follow-ups)')
for i, rq in enumerate([
    "Best real estate advice you've ever received?",
    "Worst real estate advice you've ever received?",
    "One tool or app you can't run your business without?",
    "What would surprise people most about your day-to-day?",
], 1):
    rich([('RF' + str(i) + '. ', True), (rq, True)], space=2)
rich([('PRODUCER NOTE: ', True), ('His intake answers: best is "hire slow, fire fast," worst is "time block every hour of my day." Say "Love it, and we\'re coming back to that" after RF2. Q1 opens on it. RF1 is saved for the bonus question. If he gives the long version of either answer, cut in gently: "Hold that, it\'s our first topic."', False, True)])

# ---------------- BLOCK 1 ----------------
h2('Block 1: The Calendar, Energy Not Time Blocks (2:00-12:00)')
p('Audience note: Individual agents, who have all built the perfect calendar grid and watched it collapse.', italic=True)
p('Arc: the callback, the day, the firehouse, the crash, the rebuild.', italic=True)

q(1, "You just said the worst advice you ever got was to time block every hour of your day. That's the advice every coach in this business gives. What happened when you tried it?",
  "What day of the week did it usually fall apart, and why that day?",
  "The failure of rigid blocks in his own words, and his claim that energy, not time, drives production.",
  'Individual agents, new agents',
  short="Time blocking every hour was your worst advice. What happened when you tried it?")

q(2, "Walk me through a real day. Not the ideal one. Last Tuesday. When are you sharpest, what goes in that window, and what gets pushed to the hours when you're running on fumes?",
  "What's the one task you never let into your sharp hours?",
  "His actual sequencing: what he considers highest-value work, when it goes, and what's banished to low-energy time.",
  'Individual agents',
  short="Walk me through last Tuesday. What goes in your sharpest hours?")

q(3, "You wrote about the stop-and-start 'deadly cycle,' where an agent prospects hard, gets busy with deals, stops prospecting, and then has nothing. Doesn't an energy-based calendar make that worse? On a low-energy day, the prospecting is the first thing to go.",
  "So what's the rule? What can never move, no matter how you feel?",
  "The line between flexibility and excuses. The non-negotiable that makes energy scheduling work instead of becoming permission to skip.",
  'Individual agents, team leaders',
  short="Doesn't scheduling around energy just give agents permission to skip prospecting?",
  note="This is the objection-said-out-loud question. Don't accept 'discipline' as the answer. Get the rule.")

q(4, "An agent listening wants to rebuild tomorrow's calendar tonight. Give them the steps.",
  "How do they figure out when their sharp hours actually are? Do they track it, or guess?",
  "A do-it-tonight method: find the window, protect it, put the highest-value task there first.",
  'Individual agents, new agents',
  short="An agent wants to rebuild tomorrow's calendar tonight. What are the steps?")

bridge("So the calendar runs on energy, with one thing that never moves. But a calendar only works if you know what you're aiming at, and most agents have a plan they wrote in January and haven't opened since.")

# ---------------- BLOCK 2 ----------------
h2('Block 2: The Plan and the CRM (12:00-20:00)')
p('Audience note: Producing agents and team leaders who set goals every January and drift by spring.', italic=True)
p('Arc: the dead plan, the CRM, the Friday number.', italic=True)

q(5, "I've interviewed hundreds of agents, and almost every one has written a business plan. Almost none of them could tell me what's in it by March. What's actually in yours, and how often do you open it?",
  "What are the numbers on it? Not the goal. The weekly activities.",
  "The mechanism: what goes in the plan, which leading numbers he tracks, and the review cadence.",
  'Individual agents, team leaders',
  short="Most plans are dead by March. What's in yours, and how often do you open it?",
  note="Backup if he needs a scene: \"Early on you wrote something like 30 offers in six months and none got accepted. What did that teach you about planning?\" Only if he confirmed the story pre-show.")

q(6, "You put the CRM in the operating system right next to the calendar. Most agents treat their CRM like a junk drawer. What's in yours that most agents' CRMs are missing?",
  "Open it up for me. What does one client record look like? What fields, what tags, what's the next step?",
  "How the CRM drives the calendar: what he records about each person, how it decides who he contacts this week, and who keeps it clean.",
  'Individual agents, team leaders',
  short="Most CRMs are junk drawers. What's in yours that other agents' are missing?",
  note="If he names software, ask \"And for the agent on a free CRM, what's the same?\" The system, not the tool.")

q(7, "If an agent only checks one number every Friday, which number?",
  "And what does a bad Friday number tell them to do Monday?",
  "A single leading indicator any agent can track, with the action it triggers.",
  'Individual agents, new agents',
  short="An agent checks one number every Friday. Which one?",
  note="If he says 'GCI' or 'closings,' push: 'That's a result. What's the number that predicts it?'")

bridge("So you have a calendar, a plan you actually open, and a CRM that tells you who to call. But none of it matters if the client across the table doesn't believe you, and right now, they don't.")

# ---------------- BLOCK 3 ----------------
h2('Block 3: Proof Over Promise (20:00-31:00)')
p('Audience note: Every agent whose buyers now want proof before they sign anything.', italic=True)
p('Arc: the Zillow buyer, the skill, the new rules, the rookie with no proof, the proof asset.', italic=True)

q(8, "You had a buyer who wanted to see twenty view homes in one weekend, and at every front door he'd ask what it was worth and check your answer against Zillow while you were still talking. That's every buyer now, isn't it?",
  "What did he teach you that you now teach your agents?",
  "The shift from clients trusting agents to clients checking them, told through his best story. The laugh earns the block.",
  'All segments',
  short="Tell me about the buyer who checked you against Zillow at every front door.")

q(9, "You said that buyer is why you can walk into a house today and give a confident number on the spot. How does an agent build that skill without a buyer quizzing them for a whole weekend?",
  "What's the drill? How many houses, how often, and how do they check their answer?",
  "A repeatable practice for pricing on the spot: previews, guessing before looking at comps, tracking the misses. Proof an agent can show at the door.",
  'New agents, individual agents',
  short="How does an agent learn to give a confident number at the front door?")

q(10, "In February you wrote, \"I cannot recruit on promises anymore,\" and that touring first and talking later is dead. You also wrote about the MLS policy changes that took effect in January. What changed this year, and what does an agent have to prove now before a client commits?",
  "Give me a specific piece of proof. Something an agent can hand a client.",
  "What changed in 2026 from a broker's seat, and what verifiable authority looks like in practice: track record, market knowledge on the spot, a plan for the client, reviews.",
  'Individual agents, broker-owners',
  short="What changed this year, and what does an agent have to prove now?",
  note="Current-moment question. The quotes are verbatim from his Feb 10, 2026 Inman byline. Let him explain the January MLS changes. Don't describe them yourself. Buyer agreements (Aug 2024) are background only.")

q(11, "Here's the agent who's pushing back right now. Licensed eight months, two closings, no reviews. 'Proof over promise' sounds great when you have billions in sales behind you. What proof does she have?",
  "If she has zero sales, what's the first proof she can build this month?",
  "Proof a new agent can build without a track record: knowledge, preparation, borrowed credibility, the way she answers 'what's it worth?'",
  'New agents',
  short="An agent has two closings and no reviews. What proof does she have?")

q(12, "Give every agent listening one piece of proof they can build this week.",
  "What does done look like? When do they know it's finished?",
  "A concrete, this-week action that creates verifiable authority.",
  'Individual agents, new agents',
  short="One piece of proof an agent can build this week. What is it?")

bridge("So you earn the client with proof. The last piece is keeping them, and you have a story about a client that took ten years to pay off.")

# ---------------- BLOCK 4 ----------------
h2('Block 4: Clients for Life (31:00-40:00)')
p('Audience note: Producing agents who live transaction to transaction.', italic=True)
p('Arc: the ten-year client, the referral system, the first 30 days.', italic=True)

q(13, "One of your first clients came from six months of prospecting at an alumni association. You got outbid by flippers, so the two of you built townhomes together instead. Then you didn't hear from him for years. Then he came back and bought two office buildings through you for about $7 million. What were you doing during the years you didn't hear from him?",
  "Did you stay in touch, or did he just remember you? Be honest.",
  "Whether Clients for Life is a system or luck, and what the decade of touches looked like.",
  'Individual agents',
  short="A client vanished for years, then bought $7 million through you. What were you doing in between?",
  permission="Without getting into his personal life,",
  note="His intake mentions the client's divorce. Don't raise it. His line 'I worked ten years to become an overnight success' is the payoff. If he doesn't say it, read it back to him.")

q(14, "You've written about the '411' conversion model for referrals. Explain it like I'm an agent with 150 past clients and no system.",
  "What's the first message an agent sends to a past client they haven't talked to in two years?",
  "The mechanism: how a past client turns into a referral, step by step, with the cadence.",
  'Individual agents, new agents',
  short="Explain the 411 referral model to an agent with 150 past clients and no system.",
  note="We know the name from his March 2025 Inman headline only. Let him define it.")

q(15, "Last one. An agent closes a deal this Friday. What's the one thing they do in the next 30 days that turns that client into a client for life?",
  "Give me the date and the message.",
  "A concrete post-close touch with timing.",
  'Individual agents, new agents',
  short="An agent closes Friday. What do they do in the next 30 days?")

h3('Bonus (only if you\'re ahead of time)')
q('B', "Your best advice came from the fire department: hire slow, fire fast. You've said you can't install a motor in someone who doesn't have one. For the team leaders listening, how do you test for that motor before you hire?",
  "What's the work test you give? What do they actually have to do?",
  "How he screens for people the operating system will run on.",
  'Team leaders, broker-owners',
  short="'Hire slow, fire fast.' How do you test for the motor before you hire?",
  permission="I know letting people go is the hard part, so I'll ask about the front end.",
  note="Broker shop talk lives here and nowhere else. Two minutes max.")

h2('The Close (40:00-43:00)')
h3('Homework (read verbatim)')
p('"Here\'s what I want you to do before the next episode. Open tomorrow\'s calendar. Find the two hours when you\'re sharpest, and move the most valuable thing you do, your prospecting calls or your listing prep, into that window. Then protect it for five days straight. Not next month. This week."', italic=True)
h3('Guest close')
bullet('', '"Where can people find you, follow you, and get the book?"')
bullet('', 'nickschlekeway.com  |  The Signal newsletter: nickschlekeway.com/signal  |  Instagram @nickschlekeway  |  LinkedIn /in/nickschlekeway  |  YouTube @nickschlekewayofficial')
bullet('', 'The Essential Agent: confirm pre-show whether it\'s out and where to buy. His site also offers a free framework and a Four Pillars webinar. Ask which one to send listeners to.')
bullet('', 'Don\'t read his cell on air.')

h3("If you're running long, cut these first")
bullet('1. The bonus. ', 'It only serves team leaders and broker-owners.')
bullet('2. Q14 (411 model). ', 'Q13 and Q15 cover Clients for Life without the framework.')
bullet('3. Q8\'s setup. ', 'Go straight to Q9 with one line: "You had a buyer who checked you against Zillow at every door."')
bullet('4. Q2\'s follow-up. ', 'Keep the question, drop "the one task you never let in."')

h3('Never cut')
bullet('Q1 ', 'the hook and the cold open payoff.')
bullet('Q3 ', 'the objection that makes the calendar idea credible.')
bullet('Q6 ', 'the CRM, his own definition of the system.')
bullet('Q10 ', 'the current-moment question and the core of proof over promise.')
bullet('Q13 ', 'the best story and the only question that costs him something.')

doc.add_page_break()

# =====================================================================
# 4. RESEARCH BRIEF
# =====================================================================
h1('4. Research Brief')
p('Read this the morning of, not during the interview.', italic=True)

h2('4A. Background')
p('Nick grew up in Eagle, Idaho, and played defensive end at Boise State, starting all 13 games in 2006, the season that ended with the 2007 Fiesta Bowl. He became a Boise firefighter, got his real estate license, and founded Amherst Madison in 2013 with, by his account, almost everyone telling him it was a bad idea. The firm grew past 100 agents by 2020 and about 170 now. He earned a master\'s in real estate from Georgetown and has written for Inman since 2017. In 2025 Boise State named him an Outstanding Alumni. His book is The Essential Agent.')

h2('4B. Career Timeline')
p('Verified or company-dated entries only. We found no dates for his fire department service or his license.', italic=True)
table(['Year', 'Role / Company', 'Notable'], [
    ['2006', 'Boise State football', 'Started all 13 games at defensive end. Season ended with the Jan 1, 2007 Fiesta Bowl win.'],
    ['2013', 'Amherst Madison', 'Founded in Boise.'],
    ['2014', 'Idaho Business Review', 'Accomplished Under 40 honoree, age 29.'],
    ['2017', 'Inman', 'First contributor bylines ("Why I hate cubicles," "So, you want to be unemployed?").'],
    ['2018', 'Inc. 5000', 'No. 715. A Giving Circle\'s first year raised over $112,000.'],
    ['2019', 'Inc. 5000 / Front Street Brokers', 'No. 28, and No. 1 in real estate per company press. Merged with Front Street Brokers. Joined Luxury Portfolio International.'],
    ['2020', 'Amherst Madison', '100th licensed agent. HQ at 592 Benjamin.'],
    ['2021', 'Amherst Madison', 'McCall office. $1.27B volume and 2,000+ closings (company press).'],
    ['2022', 'RealTrends Top 500', 'No. 342 (first appearance), based on 2021 volume. Company says four straight years, 2022-2025.'],
    ['2025', 'Boise State COBE', 'Outstanding Alumni.'],
    ['2026', 'Inman / book', 'Feb Inman piece on running a brokerage in 2026. The Essential Agent (release date unclear).'],
], widths=[0.7, 1.8, 4.3])

h2('4C. What Makes Him Interesting for This Audience')
bullet('He argues with the standard advice: ', 'calling time blocking the worst advice he ever got goes against what most coaches teach. That disagreement is the hook.')
bullet('He has to teach it: ', 'he runs a 170-agent brokerage with an in-house new-agent course, so his frameworks have been tested on agents who aren\'t him.')
bullet('He wrote the post-settlement playbook: ', 'his Feb 2026 Inman piece says touring first is dead and promises don\'t recruit. That\'s the proof-over-promise idea with a date on it.')
bullet('He failed first: ', '30 offers in six months, none accepted (as reported; confirm pre-show). It\'s a backup for Q5, not a question.')
bullet('He plays the long game: ', 'the ten-year client who came back with $7 million is the best Clients for Life story we\'ve had.')

h2('4D. Key Data Points')
table(['Stat', 'Source', 'Confidence'], [
    ['Founded 2013', 'amherst-madison.com About page', 'High'],
    ['RealTrends Top 500, No. 342, first time, based on 2021 volume', 'Company press release, Newswire, Apr 12, 2022', 'High'],
    ['$1.27B volume and 2,000+ closings in 2021', 'Same release', 'Medium (self-reported)'],
    ['Inc. 5000: No. 715 (2018), No. 28 (2019), No. 1692 (2021)', 'Company press releases', 'Medium'],
    ['"No. 1 in Real Estate Category" on the 2019 Inc. 5000', 'Company press title (page now 404)', 'Medium'],
    ['Five straight years on Inc. 5000, 2018-2022', 'Company About page (the Boise State bio says "Inc. 500")', 'Medium'],
    ['About 170 agents', 'nickschlekeway.com', 'Medium (self-reported)'],
    ['$6B lifetime sales', 'Intake, company bio, Boise State bio', 'Guest supplied'],
    ['$7B lifetime sales', 'nickschlekeway.com homepage', 'Conflicts with $6B'],
    ['Top 1% / top 0.05% / top 0.4% nationally', 'Inman bio / company bio / his 2022 quote', 'Conflicting'],
    ['#1 luxury brokerage in Idaho', 'Company site, no ranking body named', 'Unverified'],
    ['30 offers in six months, none accepted', 'Inman, Sept 14, 2026 (written by the podcast hosts)', 'Reported'],
    ['Buyer agreements required before touring since Aug 17, 2024', 'NAR settlement rules, cited in his Feb 2026 Inman piece', 'High'],
], widths=[3.2, 2.3, 1.3])

h2('4E. Previous Media Appearances')
bullet('Real Estate Insiders Unfiltered, "Agent Series 55: Average Is Invisible" (Sept 14, 2026): ', 'average is invisible, the rookie mentality, leading by example, becoming disposable to clients, "say old things to new people." Inman wrote it up the same day.')
bullet('Idaho Cutthroat Business podcast, Ep. 25 (July 1, 2022, Boise Metro Chamber): ', 'growing up in Eagle, sports, Boise State, fighting fire, starting in real estate.')
bullet('Idaho Business Review (June 2019 profile; Jan 2020 interview): ', 'team building and charity; downtown Boise multifamily.')
bullet('A culture podcast, "Convenience vs. Connection" (date unknown; page 404). ', '')
bullet('Inman, "7 hard-earned lessons from a firefighter-turned-broker" (Dec 19, 2023), his own byline. ', 'The firefighter story is well told. Don\'t make it a question.')
bullet('No prior Keeping It Real appearance. ', 'Elliot Hoyte from Amherst Madison was a guest in May 2020.')

h2('4F. Their Own Words')
p('His intake is primary and carefully written. The Inman Sept 2026 piece was written by the podcast hosts, so treat lines from it as reported.', italic=True)
table(['Quote', 'Where and when', 'Confidence', 'How D.J. uses it'], [
    ['"Rigid blocks ignore the thing that actually drives production, which is energy."', 'His intake', 'Verbatim', 'Hold for Q1 if he gives a short answer. Read it back.'],
    ['"You can\'t install a motor in someone who doesn\'t have one."', 'His intake', 'Verbatim', 'Built into the bonus question.'],
    ['"I worked ten years to become an overnight success."', 'His intake', 'Verbatim', 'Payoff for Q13. Read it back if he doesn\'t say it.'],
    ['"I cannot recruit on promises anymore."', 'Inman, Feb 10, 2026, his byline', 'Verbatim', 'Opens Q10.'],
    ['"The old approach of touring first and talking later is dead."', 'Inman, Feb 10, 2026, his byline', 'Verbatim', 'Q10 setup.'],
    ['"I love it when people tell me I can\'t do something."', 'Idaho Business Review, June 14, 2019', 'Reported', 'Hold in reserve for Q11 (the new agent nobody believes). Paraphrase it.'],
], widths=[2.4, 1.5, 1.0, 1.9])

h2('4G. Audience Relevance')
table(['Segment', 'What they get'], [
    ['Individual agents', 'An energy-based calendar with one rule that never moves, what belongs in a CRM, a Friday number, and a post-close plan.'],
    ['Team leaders', 'A weekly plan-and-CRM review they can run with every agent, and (bonus) how to test for "the motor" before hiring.'],
    ['Broker-owners', 'Why promises no longer recruit, and how a founder installs a system in 170 agents without outside capital.'],
    ['New agents', 'What proof looks like with two closings, and how to build the skill of pricing a house on the spot.'],
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
rich([('Facebook: ', True), ('Every coach tells you to time block every hour of your day. Nick Schlekeway built one of the top independent brokerages in the country and says it\'s the worst advice he ever got. He\'s here to show you what top producers run on instead. Drop your questions in the comments!', False)])
rich([('Instagram: ', True), ('Your calendar should run on energy, not time blocks. Live with @nickschlekeway. #KeepingItReal #RealEstatePodcast #RealEstateAgent', False)])
rich([('TikTok: ', True), ('Your time blocks fall apart by Tuesday? Here\'s why. #realestateagent #productivity #realestatetips', False)])
rich([('YouTube: ', True), ('Nick Schlekeway, founder of Amherst Madison in Boise, joins Keeping It Real with D.J. Paris to lay out the operating system top real estate agents run on: an energy-based calendar, a business plan and CRM you actually use, proof clients can verify, and a system for clients for life.', False)])
rich([('LinkedIn: ', True), ('Most agents never get taught the system top producers run on. Nick Schlekeway, founder of Amherst Madison and author of The Essential Agent, walks through it piece by piece: the calendar, the plan, the proof and the client journey.', False)])

h2('5C. Hashtags')
bullet('Universal: ', '#KeepingItReal #RealEstatePodcast #DJParis #RealEstateLife #RealEstateAgent')
bullet('Episode: ', '#RealEstateCoaching #TimeBlocking #RealEstateBusinessPlan #TheEssentialAgent #BoiseRealEstate #AgentProductivity #RealEstateBroker')
bullet('Guest tags: ', 'Instagram @nickschlekeway, LinkedIn /in/nickschlekeway, YouTube @nickschlekewayofficial, Facebook nick.schlekeway')

# =====================================================================
# 6. YOUTUBE CHAPTERS
# =====================================================================
h1('6. YouTube Chapter Markers')
table(['Timestamp', 'Chapter title'], [
    ['0:00', 'Why Rigid Time Blocks Fail Real Estate Agents'],
    ['2:00', 'Rapid Fire: Best and Worst Advice From a Brokerage Founder'],
    ['3:00', 'What Happens When Agents Time Block Every Hour'],
    ['5:30', 'A Real Day: Scheduling Around Your Energy'],
    ['8:00', 'The Stop-and-Start Cycle That Kills Real Estate Businesses'],
    ['10:30', 'How to Rebuild Tomorrow\'s Calendar Tonight'],
    ['12:00', 'What Belongs in a Real Estate Business Plan'],
    ['15:00', 'What Your CRM Is Missing'],
    ['18:30', 'The One Number to Check Every Friday'],
    ['20:00', 'The Buyer Who Checked Zillow at Every Door'],
    ['22:00', 'How to Price a House on the Spot'],
    ['24:30', 'What Agents Must Prove After the MLS Changes'],
    ['27:00', 'How a New Agent Builds Proof With No Sales'],
    ['29:30', 'One Piece of Proof to Build This Week'],
    ['31:00', 'The Client Who Came Back Years Later With $7 Million'],
    ['34:30', 'The 411 Referral Model for Past Clients'],
    ['37:30', 'What to Do in the 30 Days After Closing'],
    ['40:00', 'Homework and Where to Find Nick Schlekeway'],
], widths=[1.0, 5.8])

doc.add_page_break()

# =====================================================================
# 7. STRESS TEST, COUNCIL, EP POLISH
# =====================================================================
h1('7. Stress Test, Council Review and EP Polish')
h2('7A. Stress Test')
table(['#', 'What broke', 'Fix applied'], [
    ['1', 'Fact conflict: lifetime sales are $6B (intake, company bio) and $7B (his own homepage).', 'No dollar total appears in anything D.J. reads. Q11 says "billions."'],
    ['2', 'Fact conflict: Top 1% (intake), top 0.05% (company bio), top 0.4% (his own 2022 quote).', 'Kept out of every title, the cold open and the descriptions. On the card as "let him say it."'],
    ['3', 'Unverified: "#1 luxury brokerage in Idaho" has no named ranking body.', 'Kept off air copy. Descriptions say "one of the top independent brokerages."'],
    ['4', 'Spent topic: "Average Is Invisible," his #3 suggestion, was a full episode on Real Estate Insiders Unfiltered on Sept 14, 2026.', 'Not a block or a question. Listed as overasked. Core topic moved to the Agent Operating System, his #1 suggestion.'],
    ['5', 'Core topic mismatch: his intake defines the operating system as calendar, CRM, business plan and daily habits. The first draft never asked about the CRM.', 'Added Q6 (the CRM). Cut the Thermostat Effect question to make room.'],
    ['6', 'Spent question: RF2 spends "time block every hour," which is the hook.', 'Q1 is written as a callback ("You just said..."). Note on the card and in Rapid Fire.'],
    ['7', 'Spent question: RF1 spends "hire slow, fire fast."', 'Moved to a bonus question, asked only if there\'s time.'],
    ['8', 'Drift risk: two brokerage people talking shop about recruiting and hiring.', 'Hiring question cut from Block 4 to the bonus. Drift guard on the card.'],
    ['9', 'Drift risk: the firefighter-to-founder story, which he\'s told on two podcasts and in his own Inman piece.', 'Not a question. The intro covers it.'],
    ['10', 'Unverifiable: the 30-offers story comes from an article the podcast hosts wrote, and it\'s a negotiation story, not a planning one.', 'Removed as Block 2\'s opener. Now a pre-show check and a backup on Q5 only.'],
    ['11', 'Stale current-moment question: buyer agreements date to Aug 2024, more than two years ago.', 'Q10 now leads with the January 2026 MLS policy changes from his own Inman piece, with buyer agreements as background.'],
    ['12', 'Block 4 covered four angles (the client, referrals, hiring, after closing). Q13 and the old Q16 overlapped.', 'Block 4 is now three questions in order: the story, the referral system, the 30 days after closing.'],
    ['13', 'Missed mechanism: his Zillow story ends with a skill (a confident number on the spot) that nobody asked about.', 'Added Q9: how an agent builds that skill.'],
    ['14', 'Dodgeable: Q3 can be answered "discipline." Q7 can be answered "closings." Q13 can turn into a story about luck.', 'Follow-ups demand the rule, a leading number, and "did you stay in touch, or did he just remember you?"'],
    ['15', 'Gotcha risk: Q11 brings up his own track record as a skeptic\'s objection.', 'Framed as the new agent\'s voice. Says "billions," not a number.'],
    ['16', 'Sensitivity: the ten-year client went through a divorce.', 'Q13 starts with "Without getting into his personal life." Note: don\'t raise it.'],
    ['17', 'Title risk: if he softens on air to "rigid blocks are bad," "Stop Time Blocking" oversells.', 'Title and live title now say "Why Rigid Time Blocks Fail."'],
    ['18', 'Homework asked for two things (the two hours and a Friday number).', 'Cut to one action: the two-hour block, protected for five days.'],
    ['19', 'Book status unclear: listings say Oct 2026 and Jan 2027, his site says Aug 2026.', 'Pre-show check. No release date in any copy.'],
    ['20', 'House rule: the template\'s #RealtorLife tag uses the trademarked word generically.', 'Swapped to #RealEstateLife.'],
], widths=[0.3, 3.1, 3.4])

h2('7B. Council Review')
h3('Member notes')
table(['Member', "What they'd change"], [
    ['Hormozi', 'Q4, Q7, Q9 and Q12 are the take-home. A calendar, a number, a skill, a proof. Make sure each gets a concrete answer, not a philosophy.'],
    ['MrBeast', 'Opening on "the worst advice was time blocking" is a great hook, but only if Q1 lands in the first three minutes. Don\'t let the intro run long.'],
    ['Brendan Kane', 'Title 1 is a contrarian insight hook. Title 2 is a fear hook. Test them against each other.'],
    ['Donald Miller', 'He\'s the guide. The hero is the agent whose calendar falls apart by Tuesday. The homework proves it.'],
    ['Byron Lazine', 'Q10 is the take: "I cannot recruit on promises anymore," tied to this year\'s MLS changes. Clip it.'],
    ['Eric Simon', 'The Zillow buyer is the share. Every agent has had a client fact-check them mid-sentence.'],
    ['Chris Do', 'Q13 (the quiet years) is the one that costs him something. Protect it. Keep the 30-offers story ready for Q5.'],
], widths=[1.5, 5.3])
p('The disagreement: Byron wants to lead with proof over promise because it\'s tied to the settlement. Kane wants the time-blocking hook because it\'s contrarian and evergreen. Decision: lead with time blocking (it\'s his own worst-advice answer, so Rapid Fire sets it up for free) and A/B test the proof title.', italic=True)

h3('Title (pick one, keep others for A/B)')
table(['#', 'Title', 'Ingredient', 'Curiosity mechanism'], [
    ['1', 'Why Rigid Time Blocks Fail: The Operating System Top Producers Actually Run On (Nick Schlekeway)', 'Insight', 'Breaks a belief, then promises the replacement.'],
    ['2', 'Your Clients Don\'t Believe You Yet. A Brokerage Founder on How to Prove It (Nick Schlekeway)', 'Insight / fear', '"Yet" opens the gap.'],
    ['3', 'From Boise Firefighter to Brokerage Founder: The System Nobody Teaches Agents (Nick Schlekeway)', 'Personality', 'What did a firefighter learn that agents don\'t?'],
], widths=[0.3, 3.3, 1.2, 2.0])
p('Recommended: #1. It holds up over time, it argues with advice every agent has heard, and Rapid Fire sets it up.', italic=True)

rich([('Cold-open hook (sharpened): ', True), ('"The most common productivity advice in real estate is to time block every hour of your day. Today\'s guest built one of the top independent brokerages in the country, and he says that advice is the worst he ever got. We\'re going to talk about that today. Stay tuned."', False, True)])

h3('The Clip Engine')
table(['Q#', 'Question', 'Berger emotion', 'Heath gap'], [
    ['1', 'Time blocking every hour was your worst advice. What happened when you tried it?', 'Surprise, validation', 'Contradicts what agents were told.'],
    ['8-9', 'The buyer who checked you against Zillow at every door, and how you learned to price a house on the spot.', 'Amusement, then awe', 'Every agent has had this buyer. The twist: it made him better.'],
    ['13', 'A client vanished for years, then bought $7 million through you.', 'Awe', 'Ten years, fifteen hours of work. "An overnight success."'],
], widths=[0.4, 2.8, 1.6, 2.0])

h3('Live-description scrub')
table(['Platform', 'Verdict and fix'], [
    ['Facebook', 'Fixed. Removed "$6 billion" and "#1 luxury." Now says "one of the top independent brokerages."'],
    ['Instagram', 'Keep. Short, one idea, tags him.'],
    ['TikTok', 'Keep. A question every agent answers "yes" to.'],
    ['YouTube', 'Keep. Search terms: real estate agent, business plan, calendar, clients for life.'],
    ['LinkedIn', 'Keep. Names the book for a professional audience.'],
], widths=[1.3, 5.5])

rich([('Arc fix: ', True), ('The sag risk is Block 2, which is the most abstract (plans and numbers). It now opens on the "hundreds of agents" line and a plan nobody opens by March, moves to the CRM, and ends on a single Friday number. If it still drags, use the 30-offers story as a scene.', False)])
h3('Why it should work')
bullet('Curiosity (Heath): ', 'Agents have been told to time block for years. "That\'s the worst advice" makes them ask "then what?"')
bullet('Share driver (Berger): ', 'Team leaders will send Q4 and Q7 to their agents. Agents will send the Zillow clip to each other.')
bullet('Retention (MrBeast): ', 'Every block ends on something to do this week, and Rapid Fire sets up the opener.')
rich([('The dissent: ', True), ('Byron still thinks proof over promise wins because of the settlement angle. A/B title 2 against title 1 on the thumbnail test.', False)])

h2('7C. EP Polish (pass 3)')
bullet('', 'Dropped "Average Is Invisible" as a block after finding he did a full episode on it two months ago. Moved the core topic to the Agent Operating System.')
bullet('', 'Rewrote Q1 as a callback to Rapid Fire so his worst-advice answer becomes the hook instead of being spent.')
bullet('', 'Took every sales figure and ranking out of the titles, the cold open and the descriptions after finding three different "top %" claims and two different lifetime totals.')
bullet('', 'Cut the firefighter origin story as a question. It now shows up through Q15 (Boise Fire advice) only.')
bullet('', 'Reframed Q11 as a new agent\'s objection so it doesn\'t read as D.J. challenging his numbers.')
bullet('', 'Added permission lines to Q5, Q7, Q13 and Q15 only.')
bullet('', 'Swapped #RealtorLife for #RealEstateLife and used the full show name in the YouTube description.')
bullet('', 'Second review: added a CRM question (Q6) so the episode covers all four parts of his own operating system definition, and cut the Thermostat Effect question.')
bullet('', 'Second review: moved "hire slow, fire fast" to a bonus question and cut Block 4 to three questions with no overlap.')
bullet('', 'Second review: added Q9 on pricing a house on the spot, the skill his Zillow story ends on.')
bullet('', 'Second review: moved the current-moment question to the January 2026 MLS changes, and opened Block 2 on the plan instead of the unconfirmed 30-offers story.')
bullet('', 'Second review: changed Q11 to "billions," cut the homework to one action, and softened the lead title to "Why Rigid Time Blocks Fail."')

doc.save("/Users/djparis/GitHub Projects/keeping-it-real-content-system/guest-prep/Nick_Schlekeway_Interview_Prep.docx")
print("Saved Nick_Schlekeway_Interview_Prep.docx")
