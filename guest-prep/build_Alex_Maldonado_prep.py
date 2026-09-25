#!/usr/bin/env python
# Builds the KIRP interview prep .docx for Alex Maldonado Miranda, Circle Real Estate (Los Angeles, CA)
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
r = sub.add_run('Interview Prep: Alex Maldonado Miranda')
r.bold = True
r.font.size = Pt(20)
sub2 = doc.add_paragraph()
sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub2.add_run('REALTOR, Circle Real Estate  |  South LA, East LA, Northeast LA and Long Beach  |  Target runtime 43 minutes')
r.italic = True
r.font.size = Pt(10)

# =====================================================================
# 1. QUICK REFERENCE CARD
# =====================================================================
h1('1. Quick Reference Card')
p('One page. Glance at this during the interview.', italic=True, space=8)

h3('Who he is')
bullet('Name: ', 'Alex Maldonado Miranda. Goes by Alex Maldonado. REALTOR with Circle Real Estate, California DRE #02196988.')
bullet('Office: ', "Circle Real Estate, 3250 Airflite Way, Suite 400, Long Beach. The brokerage's DRE is #02051216.")
bullet('Markets: ', 'South LA, East LA, Northeast LA and Long Beach, per his intake. His website also lists Glendale, Pasadena, Torrance, El Segundo, Northridge and Cerritos.')
bullet('Niche: ', 'First-time and first-generation buyers, the Hispanic community, and professionals buying to build wealth. Works in English and Spanish.')
bullet('Second business: ', 'Owns Maldonado Marketing, an LA agency that builds lead generation, local SEO, Google Ads and intake systems for law firms. Also markets to real estate agents and contractors.')
bullet('Education: ', 'UCLA graduate (his intake and LinkedIn both say so).')
bullet('Guest type: ', "A, newer producing agent, with a C overlay because he runs a marketing agency. Keep agency talk under 20% of the episode and always pull it back to what an agent does with it.")

h3('Verified or safe to say on air')
bullet('', 'Circle Real Estate, DRE #02196988, Long Beach office.')
bullet('', 'Focus on first-time and first-generation buyers. His site: making homeownership "clear, accessible, and achievable."')
bullet('', 'Bilingual. His site has a full Spanish version.')
bullet('', 'Free guides on his site: First-Time Buyer\'s Roadmap, Down Payment Assistance guide, Credit Score guide, LA Home Seller\'s Checklist, ADU and SB 9 guide.')
bullet('', 'FHA lets the seller cover up to 6% of the price in closing costs. Conventional with under 10% down caps it at 3%.')
bullet('', 'City of LA LIPA program lists assistance up to $161,000 for low-income first-time buyers, 0% interest, no monthly payment, shared appreciation on the back end. City of LA only, 1-unit homes, income limits apply.')

h3('Guest supplied, do not state as verified')
bullet('', '"More than 10 years of marketing experience." His agency site says founded 2016, which fits. An older page on the same site says six years. Say "a decade in marketing" and let him correct you.')
bullet('', 'His transaction count. Public records show one closed sale in the last five years, a $525,000 home in Manchester Square. Do not say that number on air. Do not ask how many deals he has done. See 4H.')

h3('Personal, publicly shared, warmth only')
bullet('', 'His site says he loves the beach, coffee, boba, reading, and his cat.')
bullet('', 'He watched his own family navigate the LA market without much guidance. That is where Q1 comes from.')

h3('Contact and social')
bullet('', 'alexmaldonadorealestate.com. Phone (323) 990-7819 per his site. Instagram @yourrealestateman.alex. YouTube @yourrealestateman_alex. Agency: maldonadomarketing.co.')

h3('Connection to KIR')
bullet('', 'No prior KIR appearance found. First time on the show. No Kale overlap, he is in LA.')
bullet('', 'No other podcast appearances found anywhere. This is likely one of his first interviews. Expect nerves in the first five minutes.')

h3('THE CORE TOPIC')
p('The closing-cost gap: first-generation buyers who saved the down payment, then hit closing costs and decided owning was out of reach, and the three places the rest of the money actually comes from (the seller, assistance programs, and the agent who knows to ask).', bold=True)

h3('Overasked questions to avoid')
bullet('', '"How did you get into real estate?" Nothing public to build on and it burns five minutes. Q1 gets the family story from a sharper angle.')
bullet('', '"What\'s the LA market doing right now?" Market updates are the drift trap for any LA guest. Not this episode.')
bullet('', '"Any tips for first-time buyers?" Every first-time-buyer agent has a canned list. Ask for the mechanism instead.')

h3('The "I\'ve interviewed hundreds" moment')
p('Q6, and nowhere else: "I\'ve interviewed hundreds of agents on this show, and almost none of them has named closing costs as the reason a first-time buyer didn\'t buy."', italic=True)

h3('Live stream title (paste into Restream before you hit record)')
p('Down Payment Saved, Closing Costs Short: Alex Maldonado\'s Fix (61 characters)', bold=True)
p('Backup: The Seller Credit First-Time Buyers Never Hear About, with Alex Maldonado (73 characters)', italic=True)
p('This is not the published episode title. Pick that after you hear the interview. Recommendation is in 7B.', italic=True)

h3('WATCH OUT FOR')
bullet('Rapid Fire will spend Block 4. ', 'He sent his worst advice in the intake: "It\'s a numbers game." That answer is the spine of Block 4. When he says it, say "Love it, and we\'re coming back to that," then run the callback at Q13 exactly as written. His best advice (put clients first, referrals follow) is safe to spend.')
bullet('Thin public track record. ', 'One public closed sale. This episode works because of what he knows, not how much he has closed. Never frame a question around volume.')
bullet('Program numbers change. ', 'Say "lists up to" for LIPA. CalHFA Dream For All was closed as of early 2026. If he says it is open, let him say it. Do not state program amounts as today\'s numbers without "last I saw."')
bullet('Lending advice on air. ', 'When he gets specific on loan rules, add one line: "and check with your lender, because this changes." Once, not every time.')
bullet('Leimert Park. ', 'Let him say it. Do not try to pronounce it before he tells the story.')

h3('THE TWO STANDING REMINDERS')
p('Ask the short version.', bold=True, space=2)
p('Count to three before you respond.', bold=True)

doc.add_page_break()

# =====================================================================
# 2. EPISODE FRAMEWORK
# =====================================================================
h1('2. Episode Framework')

h2('2A. Title Options')
table(['#', 'Title', 'Why it works'], [
    ['1', 'They Saved the Down Payment and Still Thought They Couldn\'t Buy. Alex Maldonado on the Closing-Cost Gap',
     'Specific claim plus name. Opens on a buyer every agent has met and never names the fix, so the gap stays open.'],
    ['2', 'The 6% Seller Credit First-Time Buyers Never Hear About (Alex Maldonado, Los Angeles)',
     'Number, claim, name. The 6% is the verified FHA cap. Promises a tool an agent can use on the next offer.'],
    ['3', 'Why First-Generation Buyers Think Owning Is Out of Reach, and Why They\'re Wrong (Alex Maldonado)',
     'Names the audience he serves and picks a fight with the belief. Strongest for Spanish-language and first-gen shares.'],
], widths=[0.35, 3.6, 3.1])
p('Recommended in 7B.', italic=True)

h2('2B. Cold Open Hook')
p('"Alex Maldonado works with LA buyers who already did the hard part. They saved the down payment, then they saw the closing costs and decided owning a home wasn\'t for them. He says most of them were wrong, and the money was sitting in places nobody told them to look. We\'re going to talk about that today. Stay tuned."', bold=True)

h2('2C. Episode Arc')
p('Core topic: the closing-cost gap, and how an agent gets a buyer who has the down payment but not the closing costs to the table anyway.', bold=True)
p('Why this topic: it is the one thing Alex does that most agents in the audience skip, it works in every market, and it produces a checklist the listener can use on their next offer. His marketing background is a strong second topic, so it gets one block as the "how you find these buyers" angle instead of its own episode.')
p('Four angles, one topic. Block 1 is the buyer who thinks they can\'t. Block 2 is getting the seller to pay. Block 3 is the programs nobody mentions. Block 4 is how you find these buyers without living on the phone. Every block ends on something a listener can do this week.', italic=True)

doc.add_page_break()

# =====================================================================
# 3. INTERVIEW QUESTIONS
# =====================================================================
h1('3. Interview Questions')

h2('Rapid Fire (0:00 to 2:00, standardized, read as written)')
p('1. Best real estate advice you\'ve ever received?', space=2)
p('2. Worst real estate advice you\'ve ever received?', space=2)
p('3. One tool or app you can\'t run your business without?', space=2)
p('4. What would surprise people most about your day-to-day?', space=2)
p('No follow-ups. "Love it" and move on. One exception, below.', italic=True, space=4)
rich([('THE ONE EXCEPTION: ', True), ('His worst advice is "It\'s a numbers game," and it carries Block 4. When he says it, say "Love it, and we\'re coming back to that." Then run the callback at Q13. If his answer to #3 is a phone charger, laugh, and save the Supra story for Q15.', False, True)])

# ---------------- BLOCK 1 ----------------
h2('BLOCK 1: The Buyer Who Thinks They Can\'t (2:00 to 11:00)')
p('Audience note: individual agents and new agents. Every one of them has a renter in their sphere who has quietly decided they can\'t buy.', italic=True, space=2)
p('Arc: the family, the hidden gap, the hard no, the question.')

q(1, "Your website says you watched your own family navigate the LA market without much guidance. What did that look like from where you were standing, and what's the one thing you wish somebody had told them?",
  '"How old were you, and what did you see go wrong?"',
  'The origin of the niche, told as a scene, not a mission statement. The one missing piece of information his family never got.',
  'All segments. Earns the rest of the episode.',
  short="You watched your family buy in LA without help. What did nobody tell them?",
  permission="Tell me if this is too personal, but I want to ask about your family.",
  note='After his answer lands, add one line: "And later I want to hear about Leimert Park." That is the retention tease from 7B.')

q(2, "You told me a big part of your work is buyers who have the down payment saved and nothing left for closing costs. Most people won't volunteer that. How do you find out that's where they are?",
  '"What\'s the actual question you ask, word for word?"',
  'The discovery question and when in the process he asks it. Whether the buyer usually already knows the closing-cost number or finds out late.',
  'Individual agents, new agents.',
  short="How do you find out a buyer has the down payment but not the closing costs?")

q(3, "You had a buyer set on one neighborhood she couldn't afford. Every listing she sent you was cash only, and she was on an FHA loan. At what point did you tell her, and what did you actually say?",
  '"Did she end up buying? Where?"',
  'How he tells a client no without losing the client. The script for redirecting a buyer from the dream to the possible. Whether it worked.',
  'Individual agents.',
  short="Your FHA buyer kept sending cash-only listings. What did you finally say to her?")

q(4, "For the agent listening who never talks about closing costs until the loan estimate shows up: what's the one question they should add to their first buyer meeting this week?",
  '"Give me the exact sentence."',
  'A single question the listener can steal and use on their next consult.',
  'Individual agents, new agents.',
  short="What closing-cost question should every agent add to their first buyer meeting?")

bridge("So the buyer who thinks they can't often has most of it already. Let's talk about where the rest comes from, starting with the seller.")

# ---------------- BLOCK 2 ----------------
h2('BLOCK 2: Getting the Seller to Pay (11:00 to 22:00)')
p('Audience note: individual agents working buyers in competitive markets, plus listing agents who receive these offers.', italic=True, space=2)
p('Arc: the rule, the blind spot, the objection, the settlement, the call.')

q(5, "On an FHA loan the seller can cover up to 6% of the price in closing costs. Conventional with under 10% down, it's 3%. In a market like LA, where you're competing on price, how do you ask for a credit without your offer landing at the bottom of the pile?",
  '"Do you raise the price to cover it? By how much, and what happens if it doesn\'t appraise?"',
  'The price-up, credit-back mechanics. How he protects the buyer if the appraisal comes in low. What percent he actually asks for.',
  'Individual agents.',
  short="How do you ask for a seller credit without your offer going to the bottom?",
  note='Do not accept "it depends." Ask for the last deal: price, credit amount, appraisal.')

q(6, "I've interviewed hundreds of agents on this show, and almost none of them has named closing costs as the reason a first-time buyer didn't buy. You're saying it's one of the most common ones in your world. Why does the rest of the industry miss it?",
  '"Is it the agents, the lenders, or the buyers who aren\'t saying it?"',
  'A contrarian take on who drops the ball. Ideally a specific moment where he saw an agent or lender miss it.',
  'Individual agents, team leaders.',
  short="Why does the rest of the industry miss closing costs as the deal-killer?")

q(7, "There's a listing agent listening right now, 20 years in, who reads any offer with a seller credit or a down payment assistance program as the weak offer. Slower close, more conditions, more likely to fall apart. Talk to that agent directly. What do you want them to know?",
  '"Has one of those deals ever fallen apart on you? What happened?"',
  'The objection answered head-on. Real timelines for DPA closes. What he does to make his buyer\'s offer look as safe as a conventional one.',
  'Listing agents, broker-owners.',
  short="Talk to the listing agent who thinks DPA offers are weak. What should they know?")

q(8, "Since the NAR settlement, buyer's agents are often asking the seller to cover their commission too. Does that ever end up competing with the buyer's closing-cost credit for the same seller dollars, and how do you handle it?",
  '"Walk me through the last deal where both were on the table."',
  'Whether his pay and his buyer\'s credit compete, and how he prioritizes. How he explains it to the buyer.',
  'Individual agents, broker-owners.',
  short="Since the settlement, do your commission and the buyer's credit fight for the same seller money?",
  permission="Do you mind if I ask about your own pay here?",
  note='Do not state a rule on whether seller-paid commission counts toward the concession cap. Lender guidance varies. Let him explain what he has seen.')

q(9, "Give the listener the actual words. When you call the listing agent before you send an offer asking for a credit, what do you say?",
  '"And what do you say when they tell you the seller won\'t do credits?"',
  'A script the listener can use on their next offer.',
  'Individual agents, new agents.',
  short="What do you say to the listing agent before you send an offer with a credit?")

bridge("The seller can cover part of the gap. For a lot of your buyers the rest comes from programs most agents have never even opened, so let's go there.")

# ---------------- BLOCK 3 ----------------
h2('BLOCK 3: The Programs Nobody Told Them About (22:00 to 31:00)')
p('Audience note: individual agents in every market. The LA numbers are the example; the process is the takeaway.', italic=True, space=2)
p('Arc: the number, the catch, your market.')

q(10, "The City of LA's LIPA program lists up to $161,000 for low-income first-time buyers, with no monthly payment. That's a real number. Why aren't more buyers using it, and why aren't more agents bringing it up?",
  '"How many of your buyers have actually closed with one of these programs?"',
  'The real reasons: income limits, city-only boundaries, slow timelines, lenders who don\'t offer it, agents who don\'t know it exists. A real count from him.',
  'Individual agents, new agents.',
  short="LA lists up to $161,000 in buyer assistance. Why isn't everybody using it?",
  note='Say "lists up to." City of LA only, 1-unit homes, income limits apply.')

q(11, "These programs aren't free money. LIPA and the county program take a share of the appreciation when the buyer sells or refinances. How do you explain that to a first-generation buyer without scaring them off, and have you ever told someone not to take it?",
  '"What\'s the math you show them?"',
  'The honest cost of assistance. Whether he has talked a buyer out of a program. This is the credibility beat of the episode.',
  'Individual agents.',
  short="These loans take a cut of the appreciation. How do you explain that honestly?")

q(12, "Most of our listeners aren't in LA. If an agent in Chicago or Dallas wants to know what's available for their buyers by Friday, where do they start, and who do they call?",
  '"Is it the lender, the city housing department, or the state housing agency first?"',
  'A repeatable research process any agent can run: city, county, state, and which lenders actually originate these loans.',
  'Individual agents in every market.',
  short="An agent outside LA wants to know their local programs by Friday. Where do they start?")

bridge("So the money is there and most agents never mention it. The last piece is how you find these buyers in the first place, and that's where your marketing background comes in.")

# ---------------- BLOCK 4 ----------------
h2('BLOCK 4: Fewer Calls, Better Calls (31:00 to 40:00)')
p('Audience note: individual agents who are grinding on volume and not converting. Also team leaders and broker-owners on Q16.', italic=True, space=2)
p('Arc: the callback, the system, the mistake, the brokerage, the cut.')

q(13, "Earlier you said the worst advice you ever got was 'it's a numbers game.' You wrote to me, 'Make fewer calls, but make them count.' What does a call that counts actually look like?",
  '"How many calls a week, and what are you doing with the time you\'re not dialing?"',
  'His actual weekly cadence. What practice, reading and script work look like in hours. How that shows up in conversion.',
  'Individual agents, new agents.',
  short="You said make fewer calls, but make them count. What's a call that counts?")

q(14, "Your marketing agency's site says, 'You don't have a lead problem. You have a system problem.' Apply that to your own real estate business. Where do your first-generation buyers actually come from, and what happens in the first hour after one raises their hand?",
  '"Which channel brought you your last three buyers?"',
  'Real lead sources (Spanish-language content, Google, sphere, referrals). His speed-to-lead and follow-up system. No agency pitch.',
  'Individual agents.',
  short="Where do your first-gen buyers come from, and what happens in the first hour?",
  note='Product rule. If this becomes a pitch for Maldonado Marketing, ask "and for the agent doing this alone with no budget?"')

q(15, "You told me you mispronounced Leimert Park in front of clients, which is not a great look for an LA agent. How do you prep for a neighborhood you didn't grow up in, so that doesn't happen again?",
  '"And the dead phone at the Supra box? What\'s in your car now?"',
  'The laugh, then the prep routine. This is the relatability clip.',
  'New agents, individual agents.',
  short="You mispronounced Leimert Park in front of clients. How do you prep now?")

q(16, "For the broker or team leader who wants to serve Spanish-speaking buyers and thinks the answer is one bilingual agent and a translated website: what are they getting wrong?",
  '"What would you build if you ran the brokerage?"',
  'What serving the Hispanic and first-gen market really takes: trust, family decision-making, Spanish-language education, partner lenders.',
  'Broker-owners, team leaders.',
  short="What do brokerages get wrong about serving Spanish-speaking buyers?")

q(17, "The listener who's making 50 calls a day and closing nothing: what should they cut this week, and what do they do with that hour instead?",
  '"Be specific. Monday at 9am, what are they doing?"',
  'A concrete swap: fewer dials, one hour of script practice or targeted follow-up. The do-it-tomorrow for the whole episode.',
  'Individual agents, new agents.',
  short="The agent making 50 calls a day and closing nothing: what should they cut?")

# ---------------- CLOSE ----------------
h2('THE CLOSE (40:00 to 43:00)')
h3('Homework (read verbatim)')
p('"Here\'s what I want you to do before the next episode: look up the down payment assistance program for your city or county, write down the maximum amount and the income limit, and text it to three renters in your sphere who\'ve told you they can\'t afford to buy. Not next month. This week."', bold=True)
h3('Guest close')
bullet('', '"Alex, where can people find you?" Expect alexmaldonadorealestate.com and Instagram @yourrealestateman.alex.')
bullet('', 'Listener resource: his free Down Payment Assistance guide and First-Time Buyer\'s Roadmap on his site. Ask him to name them. Useful mostly to LA listeners, so frame it as "if you have a client moving to LA."')

h3('If you\'re running long, cut these first')
table(['Order', 'Q#', 'Why it\'s expendable'], [
    ['1', 'Q16', 'Smallest audience segment, and Q14 already covers how he finds these buyers.'],
    ['2', 'Q8', 'Highest drift risk. Commission talk can eat five minutes and pull off the buyer.'],
    ['3', 'Q4', 'If Q2 produced his exact discovery question, Q4 is already answered.'],
    ['4', 'Q12', 'Useful but generic. Fold it into the homework instead.'],
], widths=[0.6, 0.6, 5.85])
h3('Never cut')
bullet('', 'Q2, the discovery question. It defines the episode.')
bullet('', 'Q5, the seller credit mechanics. The most usable answer in the episode.')
bullet('', 'Q7, the objection said out loud.')
bullet('', 'Q11, the honest cost of assistance. It\'s what makes him credible.')
bullet('', 'Q13, the numbers-game callback. Rapid Fire set it up; you have to pay it off.')

doc.add_page_break()

# =====================================================================
# 4. RESEARCH BRIEF
# =====================================================================
h1('4. Research Brief')
p('Read the morning of, not during the interview. LOW-INFORMATION GUEST: fewer than five independently verified facts. Much of this packet rests on his intake answers and his own websites. Those items are labeled.', italic=True)

h2('4A. Background')
p('Alex Maldonado Miranda is a Los Angeles REALTOR at Circle Real Estate and a UCLA graduate. He says he watched his own family navigate the LA market without much guidance, and he built his business around first-time and first-generation buyers, working in English and Spanish. Before and alongside real estate he built Maldonado Marketing, an LA agency that runs local SEO, Google Ads and intake systems for law firms. His stated goal: get more LA families from renting to owning without surprises.')

h2('4B. Career Timeline (verified entries only)')
table(['Year', 'Role / Company', 'Notable'], [
    ['2016', 'Founded Maldonado Marketing (per agency site)', 'Law firm lead generation, local SEO, PPC, intake systems. One page on the same site says six years, so treat as Medium.'],
    ['Current', 'REALTOR, Circle Real Estate, Long Beach office', 'DRE #02196988. License issue date not found. Ask when he got licensed.'],
    ['Not found', 'UCLA', 'Graduation year not public.'],
], widths=[0.9, 2.6, 3.55])

h2('4C. What Makes Him Interesting for This Audience')
bullet('The closing-cost gap: ', 'He focuses on buyers who have the down payment but not the closing costs. Most agents lose these buyers before they ever meet them, because the buyer disqualifies themselves.')
bullet('A marketer who sells real estate: ', 'He builds lead systems for law firms for a living. Agents get a view of lead generation from someone who does it professionally for a harder industry.')
bullet('"It\'s a numbers game" is wrong: ', 'He argues for fewer, better calls. Every agent grinding on volume will either nod or argue, and both are good for the episode.')
bullet('First-generation and Hispanic buyers: ', 'A huge, underserved buyer pool in most metros, including Chicago. Broker-owners and team leaders should hear how he builds trust with it.')
bullet('He\'s early in his career: ', 'New agents hear someone close to where they are, building a niche before building volume.')

h2('4D. Key Data Points')
table(['Stat', 'Source', 'Confidence'], [
    ['DRE #02196988, Circle Real Estate', 'His site, public agent listings', 'High'],
    ['UCLA graduate', 'LinkedIn, his intake', 'High'],
    ['Maldonado Marketing founded 2016', 'maldonadomarketing.co', 'Medium (conflicts with "six years" elsewhere on site)'],
    ['10+ years marketing experience', 'His intake', 'Guest-supplied'],
    ['1 public closed sale in prior 5 years, $525,000, Manchester Square', 'Homes.com (via search; page blocked)', 'Medium. Do not use on air.'],
    ['FHA seller concession cap: 6% of the lesser of price or appraised value', 'FHA guidelines, multiple lender sources, 2026', 'High'],
    ['Conventional concession cap: 3% under 10% down, 6% at 10 to 24% down, 9% at 25%+', 'Fannie Mae guidelines via lender sources, 2026', 'High'],
    ['City of LA LIPA: up to $161,000, 0% deferred, shared appreciation, 1-unit, City of LA only', 'LAHD 2026 first-time buyer materials', 'High (numbers reset yearly)'],
    ['LA County Home Ownership Program: up to $100,000 or 20%', 'Secondary sources, 2026', 'Medium'],
    ['CalHFA MyHome: up to 3.5% (FHA) or 3% (conventional), deferred', 'Secondary sources, 2026', 'Medium'],
    ['CalHFA Dream For All: up to 20%, lottery, closed as of early 2026', 'Secondary sources, 2026', 'Medium. Could have reopened.'],
], widths=[3.1, 2.4, 1.55])

h2('4E. Previous Media Appearances')
p('None found. No podcasts, no press, no prior KIR appearance (checked keepingitrealpod.com and the KIR content repo). This is likely one of his first interviews.')
p('Overasked questions: none documented, so the Quick Reference Card lists the generic traps for this type of guest instead.', italic=True)

h2('4F. Their Own Words')
table(['Quote', 'Where and when', 'Confidence', 'How D.J. uses it'], [
    ['"Make fewer calls, but make them count."', 'His intake, 2026', 'Verbatim', 'Read it back at Q13 to open Block 4.'],
    ['"Get more LA families from renting to owning without surprises along the way."', 'His intake bio, 2026', 'Verbatim', 'Hold in reserve. If he goes vague on Q11, ask what "without surprises" means for the shared-appreciation payback.'],
    ['"...the options they have that nobody told them about, like seller credits and down payment assistance programs."', 'His intake, 2026', 'Verbatim', 'Source of the cold open and the Block 3 title. Read it back if Block 2 stalls.'],
    ['"I\'m focused on making homeownership clear, accessible, and achievable, especially for first-time and first-generation buyers."', 'alexmaldonadorealestate.com', 'Verbatim (dash changed to a comma)', 'Optional opener if Q1 needs a softer on-ramp.'],
    ['"You don\'t have a lead problem. You have a system problem."', 'maldonadomarketing.co', 'Verbatim', 'Read it back at Q14 and ask him to apply it to himself.'],
], widths=[2.3, 1.4, 1.1, 2.25])

h2('4G. Audience Relevance')
table(['Segment', 'What they get from this episode'], [
    ['Individual agents', 'A way to rescue buyers who have disqualified themselves over closing costs, plus the seller-credit mechanics and the exact call to the listing agent.'],
    ['Team leaders', 'A lead-system view from a professional marketer, and a case for training agents on assistance programs.'],
    ['Broker-owners', 'What it really takes to serve first-generation and Spanish-speaking buyers, beyond one bilingual agent.'],
    ['New agents', 'A niche you can build before you have volume, and permission to stop treating the job as a pure numbers game.'],
], widths=[1.6, 5.45])

h2('4H. Landmines')
bullet('His production. ', 'One public sale. Asking "how many deals did you do last year" on air embarrasses him and wastes the episode. If you want a number, ask Q10\'s follow-up: how many buyers closed with a program.')
bullet('Program numbers. ', 'Amounts and income limits reset every year and programs open and close. Always "lists up to" or "last I saw."')
bullet('Lending specifics. ', 'He is not a loan officer. If he states a hard lending rule, add "and check with your lender" once.')
bullet('The Hispanic buyer framing. ', 'Let him describe his community. Do not generalize about Hispanic buyers yourself.')
bullet('Market areas. ', 'His website list (Glendale, Pasadena, Torrance) differs from his intake (South, East and Northeast LA, Long Beach). Use the intake.')

doc.add_page_break()

# =====================================================================
# 5. LIVE STREAM
# =====================================================================
h1('5. Live Stream Title, Descriptions and Hashtags')

h2('5A. Live Stream Title')
quoted('Live stream title:', 'Down Payment Saved, Closing Costs Short: Alex Maldonado\'s Fix (61 characters)')
quoted('Backup:', 'The Seller Credit First-Time Buyers Never Hear About, with Alex Maldonado (73 characters)')
p('Not the final episode title. Pick that after the interview.', italic=True)

h2('5B. Platform Descriptions')
h3('Facebook Live')
p('Your buyer saved the down payment. Then they saw the closing costs and gave up. LA agent Alex Maldonado is live with D.J. to show where the rest of the money comes from: seller credits, assistance programs and one question most agents never ask. Drop your questions in the comments!')
h3('Instagram Live')
p('Down payment saved, closing costs short? Alex Maldonado shows how buyers still get to closing. Live now. #FirstTimeHomeBuyer #KeepingItReal')
h3('TikTok Live')
p('Saved the down payment but not closing costs? You might still be able to buy. #FirstTimeHomeBuyer #RealtorTips')
h3('YouTube Live')
p('LA REALTOR Alex Maldonado joins D.J. Paris on the Keeping It Real Podcast to break down the closing-cost gap: first-time and first-generation buyers who saved the down payment but not closing costs. Seller credits, FHA and conventional concession limits, and down payment assistance programs like LA\'s LIPA.')
h3('LinkedIn Live')
p('Most agents lose first-time buyers before they ever meet them, because the buyer decides closing costs make owning impossible. Alex Maldonado, a Los Angeles REALTOR who also runs a law firm marketing agency, joins D.J. Paris to walk through seller credits, assistance programs and how he finds these buyers.')

h2('5C. Hashtag Sets')
bullet('Universal: ', '#KeepingItReal #RealEstatePodcast #DJParis #RealtorLife #RealEstateAgent')
bullet('Episode: ', '#FirstTimeHomeBuyer #FirstGenHomeBuyer #ClosingCosts #DownPaymentAssistance #LosAngelesRealEstate #LatinoHomeBuyers #SellerCredits')
bullet('Guest tag: ', 'Instagram @yourrealestateman.alex. YouTube @yourrealestateman_alex.')

# =====================================================================
# 6. CHAPTERS
# =====================================================================
h1('6. YouTube Chapter Markers')
table(['Timestamp', 'Chapter title'], [
    ['0:00', 'Saved the Down Payment, Short on Closing Costs'],
    ['post-ads', 'Rapid Fire: Best and Worst Real Estate Advice'],
    ['~3:00', 'What Nobody Told a First-Generation LA Family About Buying'],
    ['~6:00', 'How to Find Out a Buyer Can\'t Cover Closing Costs'],
    ['~9:00', 'The FHA Buyer Who Only Wanted Cash-Only Listings'],
    ['~12:00', 'How to Ask for a Seller Credit in a Competitive Market'],
    ['~15:00', 'Why Agents Miss Closing Costs as the Deal-Killer'],
    ['~17:00', 'Are Down Payment Assistance Offers Really Weaker?'],
    ['~19:00', 'Buyer Agent Commission vs Closing-Cost Credits After the NAR Settlement'],
    ['~21:00', 'What to Say to the Listing Agent Before Your Offer'],
    ['~23:00', 'LA\'s $161,000 Buyer Assistance Program Nobody Uses'],
    ['~26:00', 'The Catch in Down Payment Assistance: Shared Appreciation'],
    ['~29:00', 'How to Find Down Payment Assistance in Your Market'],
    ['~32:00', 'Why "It\'s a Numbers Game" Is Bad Advice for Realtors'],
    ['~34:00', 'Where First-Generation Buyers Actually Come From'],
    ['~36:00', 'The Leimert Park Mistake and a Dead Phone at the Lockbox'],
    ['~38:00', 'What Brokerages Get Wrong About Spanish-Speaking Buyers'],
    ['~39:00', 'Making 50 Calls a Day and Closing Nothing? Cut This'],
    ['~41:00', 'Homework and Where to Find Alex Maldonado'],
], widths=[1.0, 6.05])

doc.add_page_break()

# =====================================================================
# 7. STRESS TEST, COUNCIL, EP POLISH
# =====================================================================
h1('7. Stress Test, Council Review and EP Polish')

h2('7A. Stress Test')
table(['#', 'What broke', 'Fix applied'], [
    ['1', 'Draft Q1 asked how many deals he closed last year. Public record shows one sale.', 'Cut. Added a landmine in 4H. The only count asked is buyers closed with a program (Q10 follow-up).'],
    ['2', 'Rapid Fire spends "It\'s a numbers game," which carries Block 4.', 'Added the "coming back to that" line under Rapid Fire and the verbatim callback at Q13.'],
    ['3', 'Draft cold open said "LA gives buyers $161,000."', 'Rewritten without the number. Q10 now says "lists up to," with a producer note on limits.'],
    ['4', 'Dream For All was in the draft as an open program. It was closed as of early 2026.', 'Removed from the questions. Kept in 4D as Medium with a note.'],
    ['5', 'Marketing experience conflict: "10+ years" in intake, 2016 on agency site, "six years" on another page.', 'Card says "a decade in marketing" and lets him correct it. 4B marked Medium.'],
    ['6', 'Drift risk: LA market update and a Maldonado Marketing pitch.', 'Market update listed as an overasked trap. Producer note on Q14 with the pull-back line.'],
    ['7', 'Q5 was answerable with "it depends on the deal."', 'Added the producer note: ask for the last deal\'s price, credit and appraisal.'],
    ['8', 'Q8 (settlement) read as a gotcha about his own pay.', 'Added a permission clause and a shared-problem framing. Put first-ish in the cut list.'],
    ['9', 'Draft had 20 questions for 43 minutes.', 'Cut to 17 plus Rapid Fire, with a four-question cut list.'],
], widths=[0.35, 3.2, 3.5])

h2('7B. Council Review')
h3('Member notes')
table(['Member', 'What they\'d change'], [
    ['Alex Hormozi', 'Q5 and Q9 are the whole value of the episode. Protect them. The listener leaves with a script and a percentage.'],
    ['MrBeast', 'Block 3 is the sag risk: program talk gets dry. Q11 has to land with a real story or it dies.'],
    ['Donald Miller', 'The hero is the listener\'s buyer, not Alex. Title 1 gets that right. Title 3 makes it about beliefs, which is softer.'],
    ['Eric Simon', 'The Leimert Park story and the dead phone are the share. Don\'t bury them at minute 40. At least tease it.'],
    ['Byron Lazine', 'Q8 is the only question tied to a headline. Keep it unless you\'re really long.'],
    ['Chris Do', 'Q1 and Q11 are where he pays something honest. Take the permission clause seriously on Q1.'],
    ['Jon Youshaei', 'Chapter titles work. "The $161,000 Program Nobody Uses" is the most searchable line in the packet.'],
], widths=[1.4, 5.65])
p('Witnesses. Heath: the cold open opens the gap (they gave up) and holds the answer until Block 2. Good. Berger: the core emotion is frustration at money nobody mentioned. That\'s anger-adjacent, high arousal, and the retell survives: "the seller can pay 6% of closing costs and most buyers never ask."', italic=True)
p('The disagreement: Eric wants the funny stories early for retention. Miller and Welsh want the arc to hold. Decision: keep Q15 in Block 4, but D.J. teases it once in Block 1 (see Arc fix). The episode goal is agents sending it to agents, and the seller-credit block is what gets sent.', italic=True)

h3('Title (pick one to run, keep the others to A/B)')
table(['#', 'Title', 'Ingredient', 'Curiosity mechanism'], [
    ['1', 'They Saved the Down Payment and Still Thought They Couldn\'t Buy. Alex Maldonado on the Closing-Cost Gap', 'Insight', 'Names the buyer, withholds the fix.'],
    ['2', 'The 6% Seller Credit First-Time Buyers Never Hear About (Alex Maldonado, Los Angeles)', 'Stat', 'Specific number plus "never hear about."'],
    ['3', 'Why First-Generation Buyers Think Owning Is Out of Reach, and Why They\'re Wrong (Alex Maldonado)', 'Concept', 'Picks a fight with a belief.'],
], widths=[0.35, 3.5, 1.1, 2.1])
p('Recommended: #2. Agents are the audience and it promises a tool with a verified number. A/B against #1 for the Spanish-language and first-gen crowd.', italic=True)

h3('Cold-open hook (sharpened)')
p('"Alex Maldonado works with LA buyers who already did the hard part. They saved the down payment, then they saw the closing costs and decided owning a home wasn\'t for them. He says most of them were wrong, and the money was sitting in places nobody told them to look. We\'re going to talk about that today. Stay tuned."', bold=True)

h3('The clip engine')
table(['Q#', 'Question', 'Berger emotion', 'Heath gap'], [
    ['Q5', 'How do you ask for a seller credit without your offer going to the bottom?', 'Excitement (a new tool)', 'Every agent assumes credits lose. He says how they don\'t.'],
    ['Q7', 'Talk to the listing agent who thinks DPA offers are weak.', 'Anger', 'Direct address to a real person in the audience.'],
    ['Q15', 'You mispronounced Leimert Park in front of clients.', 'Amusement', 'The setup is the punchline; the prep routine is the payoff.'],
], widths=[0.5, 2.9, 1.5, 2.15])

h3('Live-description scrub')
table(['Platform', 'Verdict and fix'], [
    ['Facebook', 'Kept. Opens on the buyer, ends on the comment ask.'],
    ['Instagram', 'Fixed. Cut to one line and two hashtags.'],
    ['TikTok', 'Kept. Speaks to a buyer, which is who scrolls TikTok live.'],
    ['YouTube', 'Kept. Loaded with searchable terms (FHA, seller credits, LIPA).'],
    ['LinkedIn', 'Fixed. Opened on the business problem (agents losing buyers) instead of the guest.'],
], widths=[1.1, 5.95])

h3('Arc fix')
p('Block 3 sags if the program answers turn into a list. Fix: Q11 (the catch) sits in the middle of the block, not the end, so it re-hooks on tension. And after Q1 lands, D.J. says one line: "And later I want to hear about Leimert Park." That buys the funny story as a retention hook without moving it.')

h3('Why it should work')
bullet('Curiosity mechanism, Heath: ', 'The cold open says the buyers were wrong and never says why until Block 2.')
bullet('Share driver, Berger: ', 'An agent forwards "the seller can cover 6% of closing costs" to a colleague who just lost a buyer. The point survives in one sentence.')
bullet('Retention move, MrBeast: ', 'Every block ends on something the listener can use this week, plus the Leimert Park tease holds viewers into Block 4.')

h3('The dissent')
p('Hormozi still wants Q5 as the very first question after Rapid Fire, because it is the highest-value answer and some listeners will drop before minute 12. The counter is that Q1 and Q2 give the seller-credit answer its stakes. Experiment for next time: on a tactic-heavy guest, open Block 1 with the tactic and put the origin story second, and compare the 10-minute retention.')

h2('7C. EP Polish (pass 3)')
bullet('', 'Replaced a production-volume question with the family-origin Q1 after the stress test found one public sale.')
bullet('', 'Moved the numbers-game answer from Rapid Fire into a written callback at Q13 using his own intake words.')
bullet('', 'Removed the $161,000 figure from the cold open and titles, and softened it to "lists up to" in Q10.')
bullet('', 'Pulled Dream For All out of the questions because it was closed as of early 2026.')
bullet('', 'Split the old Block 2 closer into Q8 (settlement) and Q9 (the listing-agent call) so the block ends on a script, not a policy question.')
bullet('', 'Added permission clauses to Q1 (family) and Q8 (his pay), and nowhere else.')
bullet('', 'Rewrote Q12 for agents outside LA, since most of the audience is not in California.')
bullet('', 'Cut from 20 questions to 17 and wrote the cut and never-cut lists.')
bullet('', 'Added the Leimert Park tease line after Q1 to fix the Block 3 sag.')
bullet('', 'Rewrote the Instagram and LinkedIn descriptions after the scrub.')
bullet('', 'Checked every SAY THIS line is under 20 words, and removed em dashes and curly quotes throughout.')

doc.save("/Users/djparis/GitHub Projects/keeping-it-real-content-system/guest-prep/Alex_Maldonado_Interview_Prep.docx")
print("Saved Alex_Maldonado_Interview_Prep.docx")
