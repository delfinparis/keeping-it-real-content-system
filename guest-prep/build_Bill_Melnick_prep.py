#!/usr/bin/env python
# Builds the KIRP interview prep .docx for Bill Melnick, Elyse Harney Real Estate (Salisbury, CT)
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



LIVE_TITLE = "Ralph Lauren Exec to a $12M County Record: Bill Melnick on Selling the Lifestyle"
LIVE_BACKUP = "He Left Ralph Lauren in His 50s and Started Over in Real Estate: Bill Melnick"

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
r = sub.add_run('Interview Prep: Bill Melnick')
r.bold = True
r.font.size = Pt(20)
sub2 = doc.add_paragraph()
sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub2.add_run('Elyse Harney Real Estate  |  Salisbury, CT (Litchfield County)  |  Target runtime 43 minutes')
r.italic = True
r.font.size = Pt(10)

# =====================================================================
# 1. QUICK REFERENCE CARD
# =====================================================================
h1('1. Quick Reference Card')
p('One page. Glance at this during the interview.', italic=True, space=8)

h3('Who he is')
bullet('Name: ', 'Bill (William) Melnick. Luxury agent, Elyse Harney Real Estate, main office in Salisbury, CT.')
bullet('Markets: ', 'Northwest Connecticut, mostly Litchfield County (Salisbury, Sharon, Cornwall, Kent). Licensed in CT, MA and NY.')
bullet('Before real estate: ', '28 years at Ralph Lauren, ending as Chief Merchandising Officer (his intake and his brokerage bio). Started real estate at Harney in 2019.')
bullet('Personal (public on Harney materials): ', 'He and his husband Stephen came to Sharon as weekenders in 2013, bought and restored an antique saltbox, then moved up full-time. Serves on the Sharon Land Trust board.')
bullet('Guest type: ', 'A, producing luxury agent. The risk is a lovely hour about Connecticut. Keep pulling it back to what an agent in any market can steal.')

h3('Verified numbers (safe to say on air)')
bullet('Ivan Lendl estate: ', '445 acres in Cornwall and Goshen. Sold January 25, 2024 for $12 million, the highest residential sale ever recorded in Litchfield County. Previous record was $11.5 million in Kent in 2008.')
bullet('It sat a long time: ', 'First listed around 2014 at $19.8 million. Cut to $16.4 million in 2021. Final ask $14.995 million. Lendl bought it in the 1980s for $4.2 million.')
bullet('He co-listed it ', 'with Elyse Harney Morris. Always say "you and Elyse" or "your team." Never say he sold it alone.')
bullet('Three California buyers in 2025 ', 'after the wildfires (citybiz, April 2026).')
bullet('He coined "anti-Hamptons" ', 'for Litchfield County (Realtor.com, February 2026, and the Daily Mail).')

h3('Guest supplied, do not state as verified')
bullet('', '207 plus transactions and $144 million career volume. His own number. His agent page now shows 212 closed. Say "over 200 deals" and let him give the dollar figure.')
bullet('', 'Top 1% in Litchfield County, #2 in Northern Litchfield. Brokerage bio only, no ranking source named.')
bullet('', 'Wall Street Journal, New York Times and Fox Business. We could not find those pieces. Mansion Global (owned by the WSJ) covered the Lendl sale. Say "you\'ve been all over the national press" unless he confirms outlets pre-show.')

h3('Episode')
bullet('The Core Topic: ', 'How a Ralph Lauren merchandiser sells the life, not the square footage, and how any agent can steal that for pricing, presentation and their own sphere.')
bullet('Overasked questions to avoid: ', '"How did you go from Ralph Lauren to real estate?" (every press piece opens with it). "Why is Litchfield the anti-Hamptons?" "How much has the market gone up since COVID?" (he always says about 30%).')
bullet('The "I\'ve interviewed hundreds" moment: ', 'Q11 only. "I\'ve interviewed hundreds of agents, and the one listening right now is thinking: sure, he had a Ralph Lauren Rolodex."')
bullet('Live stream title: ', LIVE_TITLE + ' (' + str(len(LIVE_TITLE)) + ' characters)')
bullet('Watch out for: ', 'Rapid Fire will spend his best advice (manage up, down and side to side) and his worst advice (hand everything to AI). Say "Love it, and we\'re coming back to that." Callbacks are Q7 and Q13. If he tells the beaver story in Rapid Fire Q4, skip Q16 and use its backup.')
bullet('Watch out for: ', 'Both press sources say "26 years as Chief Merchandising Officer." He says 28 years at the company. Say "28 years at Ralph Lauren" and let him give his title arc.')
bullet('Do not read his cell number on air. ', 'Point people to Instagram and the Harney site.')
rich([('ASK THE SHORT VERSION.  COUNT TO THREE BEFORE YOU RESPOND.', True)], space=4)

doc.add_page_break()

# =====================================================================
# 2. EPISODE FRAMEWORK
# =====================================================================
h1('2. Episode Framework')
h2('2A. Title Options')
table(['#', 'Title', 'Why it works'], [
    ['1', 'Ivan Lendl\'s Estate Sat for 10 Years. A Former Ralph Lauren Exec Helped Sell It. (Bill Melnick)', 'Opens a gap (what changed?), celebrity name, verified facts only.'],
    ['2', 'The Ralph Lauren Playbook for Selling Houses: Bill Melnick on Selling the Life, Not the Square Footage', 'Promise-led. Every agent can apply it. Strong for search.'],
    ['3', 'He Left Ralph Lauren in His 50s. Now He Holds Litchfield County\'s $12M Record. (Bill Melnick)', 'Reinvention hook for the career-changer segment. Credit Elyse in show notes.'],
], widths=[0.3, 3.9, 2.6])

h2('2B. Cold Open Hook')
p('"Ivan Lendl\'s Connecticut estate went on the market at almost $20 million and sat there for the better part of a decade. It finally sold for $12 million, and that still broke the county record, and one of the two agents on it spent 28 years at Ralph Lauren. We\'re going to talk about that today. Stay tuned."', italic=True)

h2('2C. Episode Arc')
rich([('Core Topic: ', True), ('Selling the life, not the square footage. What 28 years of merchandising taught Bill about pricing, presenting and positioning a home, and how he turned a Manhattan sphere into a business in his 50s.', False)])
rich([('Why this topic: ', True), ('Every press piece on Bill is about the Litchfield market. Nobody has asked him how the merchandising brain actually works on a listing, and that is the part a Chicago agent can use Monday.', False)])
table(['Block', 'Angle', 'Time'], [
    ['Rapid Fire', 'Four standard questions', '0:00-2:00'],
    ['1', 'The merchandiser\'s eye', '2:00-11:00'],
    ['2', 'The price conversation (Lendl)', '11:00-20:00'],
    ['3', 'Starting over with a sphere', '20:00-30:00'],
    ['4', 'The co-primary buyer', '30:00-40:00'],
    ['Close', 'Homework and where to find Bill', '40:00-43:00'],
], widths=[1.0, 3.8, 1.5])

doc.add_page_break()

# =====================================================================
# 3. INTERVIEW QUESTIONS
# =====================================================================
h1('3. Interview Questions')
p('Questions are numbered 1 through 17 across all blocks so you can call a number out loud.', italic=True)

h2('Rapid Fire (0:00-2:00, read as written, no follow-ups)')
for i, t in enumerate(['Best real estate advice you\'ve ever received?',
                       'Worst real estate advice you\'ve ever received?',
                       'One tool or app you can\'t run your business without?',
                       'What would surprise people most about your day-to-day?'], 1):
    rich([('RF' + str(i) + '. ', True), (t, True)], space=2)
rich([('PRODUCER NOTE: ', True), ('He sent best and worst in his intake. After RF1 and RF2 say "Love it, and we\'re coming back to that." Callbacks are Q7 (manage up) and Q13 (AI).', False, True)])

# ---- BLOCK 1 ----
h2('Block 1: The Merchandiser\'s Eye (2:00-11:00)')
p('Audience note: Individual agents. This is the part of Bill nobody can copy from a market report.', italic=True, space=2)
p('Arc: the eye, the prep, the limit, the ordinary house.', italic=True)

q(1, 'You spent 28 years at Ralph Lauren, and Ralph never really sold shirts. He sold a life you wanted to step into. When you walk into a listing appointment now, what do you see in that house that the agent before you walked right past?',
  'Give me one house. What did you see, and what did the other agent miss?',
  'The specific lens: sightlines, the story of the room, what gets edited out. A method, not taste.',
  'Individual agents',
  short='What do you see in a house that other agents walk right past?')

q(2, 'Walk me through the last listing you took, from the first walk-through to the photo shoot. What did you change, what did you take out, and what did it cost the seller?',
  'Name the one room and the one change that mattered most.',
  'The actual prep checklist, the budget, and who does the work (Bill, a stager, the seller).',
  'Individual agents, new agents',
  short='Last listing you prepped. What changed, what got cut, what did it cost?')

q(3, 'You\'ve said buyers aren\'t buying square footage, they\'re buying frontage, views and an experience you can\'t replicate. A lot of agents believe the comps are the comps, period. Where does the lifestyle story stop working and price per foot win?',
  'Tell me about a time the story didn\'t save the price.',
  'The honest limit of positioning. Credibility for the whole episode.',
  'Individual agents',
  short='Where does the lifestyle story stop working and the comps win?')

q(4, 'Somebody listening has a $450,000 three-bedroom in the suburbs going live next week. No lake, no 200-year-old barn. What is the Ralph Lauren move for that house?',
  'One thing they do Monday. What is it, and how long does it take?',
  'A translation of the luxury method to an ordinary listing. The clip for 90% of the audience.',
  'Individual agents, new agents (perspective flip to the mass market)',
  short='Ordinary $450K house, live next week. What\'s the Ralph Lauren move?')

bridge('So the story sells the house, but only if the price isn\'t fighting it. Let\'s talk about the listing that tested that harder than any other.')

# ---- BLOCK 2 ----
h2('Block 2: The Price Conversation (11:00-20:00)')
p('Audience note: Every agent with an overpriced seller. Which is every agent.', italic=True, space=2)
p('Arc: the record, the number, the famous seller, the exact words.', italic=True)

q(5, 'Ivan Lendl\'s estate first went on the market around 2014 at $19.8 million. It sold in January 2024 for $12 million, and that still set the county record. You and Elyse Harney Morris had it at the end. Where did you come into that story, and what was the conversation that finally got it sold?',
  'What was the one thing that was different the year it sold?',
  'Bill\'s timeline on the listing, what changed (price, marketing, buyer pool), and how the deal came together.',
  'Individual agents, team leaders',
  permission='Tell me if there\'s anything here you can\'t talk about, but',
  short='Listed near $20 million, sold at $12. What conversation got it done?',
  note='Credit Elyse on air. Do not ask who the buyer was. It closed to Wyoming LLCs and the buyer asked for anonymity.')

q(6, 'You\'ve said pricing is everything, even at that end of the market. At $12 million there are no real comps. How do you actually land on a number when nothing like it has ever sold?',
  'What were the three data points you actually used?',
  'The method for pricing without comps: land value, replacement cost, buyer pool size, absorption. Works for any unusual listing.',
  'Individual agents',
  short='No comps exist. How do you land on the number?')

q(7, 'In the rapid fire you said the best advice you ever got was to manage up, down and side to side. How do you manage up with a seller who is a world-famous champion and has heard for years that his house is worth more than the market says?',
  'What did you say in the room? The actual sentence.',
  'How a corporate skill (managing a powerful boss) becomes the seller conversation. The payoff of the Rapid Fire callback.',
  'Individual agents, team leaders',
  permission='You can keep this general if you need to, but',
  short='How do you manage up with a famous seller who thinks it\'s worth more?')

q(8, 'Give an agent the exact words. Their seller has been sitting 90 days, overpriced, and still attached to the number. What do you say at the kitchen table?',
  'Say it to me like I\'m the seller.',
  'A word-for-word price-reduction script. Roleplay it live if he\'s game.',
  'Individual agents, new agents',
  short='Overpriced seller, 90 days in. What are your exact words?')

bridge('That\'s how you get a seller to the right price. But first you have to get the listing, and you started in your fifties with zero real estate contacts.')

# ---- BLOCK 3 ----
h2('Block 3: Starting Over With a Sphere (20:00-30:00)')
p('Audience note: Anyone whose business depends on people they already know. Also the career changers, who are a big share of new licensees.', italic=True, space=2)
p('Arc: the leaving, the system, the pushback, the broker, the line.', italic=True)

q(9, 'You told Digital Journal that a lot of your friends were going through the same thing, especially people who\'d been working for corporations. Was leaving Ralph Lauren your call, and what did that first year feel like?',
  'What was the moment you knew real estate was the answer and not just a thing to do?',
  'The honest reason and the fear. The vulnerable beat that earns the rest of the episode.',
  'New agents, career changers',
  permission='Tell me if this is too personal, but',
  short='Was leaving Ralph Lauren your call?')

q(10, 'You say you never saw yourself as a salesperson. It was relationships, staying in touch, one relationship leading to the next. What is the actual system? How many people, how often, and how: a call, a note, a dinner?',
  'How many people did you reach out to last week, and how?',
  'Cadence, tools, and the number. Do not accept "I just stay in touch."',
  'Individual agents, new agents',
  short='Relationships leading to relationships. What\'s the actual cadence?')

q(11, 'I\'ve interviewed hundreds of agents, and the one listening right now is thinking: sure, he had a Manhattan Rolodex from 28 years at Ralph Lauren. My sphere is my cousin and my old manager at Starbucks. What do you say to that agent?',
  'Who in your first 20 deals was NOT someone from fashion or New York?',
  'Whether the method works without a rich sphere. Name the objection out loud.',
  'New agents, individual agents',
  short='Your sphere was Ralph Lauren. What about the agent whose sphere isn\'t?')

q(12, 'Brokers listening are going to hire a 55-year-old career changer this year. You were that hire at Elyse Harney. What did the brokerage do right with you, and what did you need that nobody gave you?',
  'What\'s the one thing a broker should do in that agent\'s first 90 days?',
  'Onboarding advice for experienced second-career agents. Perspective flip to broker-owners and team leaders.',
  'Broker-owners, team leaders',
  short='What should a broker do for the 55-year-old career changer they just hired?')

q(13, 'In the rapid fire you said the worst advice you got was to turn almost everything over to AI. Where exactly is your line? What do you let AI do, and what is the one relationship task an agent should never hand off, starting this week?',
  'Name one thing you did with AI this month and one thing you never would.',
  'A clear line between leverage and the personal touch, ending on a do-this-week action.',
  'All segments',
  short='What do you let AI do, and what should it never touch?')

bridge('So the sphere built the business. And that sphere turns out to be the exact buyer who is changing your market right now: New Yorkers who don\'t live in one place anymore.')

# ---- BLOCK 4 ----
h2('Block 4: The Co-Primary Buyer (30:00-40:00)')
p('Audience note: Any agent near a lake, a ski town, a college, or a big city. The buyer who lives in two places is everywhere now.', italic=True, space=2)
p('Arc: the new buyer, the pipeline, the beaver, the one question.', italic=True)

q(14, 'You and Stephen came to Sharon as weekenders in 2013 and ended up living there full-time. You were the co-primary buyer before you had a name for it. What\'s the difference between a second-home buyer and a co-primary buyer, and why should an agent in Chicago or Dallas care?',
  'What does a co-primary buyer ask for that a weekender never does?',
  'His term defined, the behaviors that change (schools, office, year-round use), and how it applies in other markets. Fold in the California wildfire buyers if he goes there.',
  'Individual agents',
  short='Second-home buyer versus co-primary buyer. What\'s different, and why should every agent care?')

q(15, 'Hotchkiss, Salisbury School, Berkshire, Indian Mountain. Parents buy to be near a kid and some stay for decades. Is there an actual pipeline there? How do you meet those families before they call another agent?',
  'Who introduced you to your last school-family client?',
  'A niche-farming method: institutions as referral sources. Translates to hospitals, universities, corporate HQs.',
  'Individual agents, team leaders',
  short='How do you meet prep-school parents before another agent does?')

q(16, 'Country real estate has problems a Chicago agent never sees. You once lost a deal to a beaver. What happened?',
  'What did you learn about protecting a deal from something you can\'t control?',
  'The laugh, then the lesson: inspection and site risk on rural and second-home properties.',
  'All segments',
  short='You lost a deal to a beaver. What happened?',
  note='Backup if he told it in Rapid Fire: "What\'s a deal you lost that was actually your fault?" Use the same permission words as Q9.')

q(17, 'Agents everywhere have clients who are quietly splitting time between two places. What is the one question an agent should ask to find out whether a weekender is about to become co-primary?',
  'What do you do with the answer?',
  'A single discovery question any agent can use in their next buyer consult.',
  'Individual agents',
  short='What one question tells you a weekender is becoming co-primary?')

# ---- CLOSE ----
h2('The Close (40:00-43:00)')
h3('Homework (read verbatim)')
p('"Here\'s what I want you to do before the next episode. Pick your five favorite past clients. For each one, write one sentence about the life they bought, not the house. The Saturday morning, the commute, the kid\'s school. Then text one of them this week and bring that sentence up. Not next month. This week."', italic=True)
h3('Guest close')
bullet('', '"Bill, where can people find you, follow you, or send you a referral in Connecticut?"')
bullet('Instagram: ', '@bill_melnick_real_estate')
bullet('Web: ', 'harneyrealestate.com/agent/bill-melnick')

h3('If you\'re running long, cut these first')
bullet('1. Q12 (broker hire). ', 'Smallest audience segment. Good, but not the core topic.')
bullet('2. Q15 (prep schools). ', 'Very local. Q14 already carries the co-primary idea.')
bullet('3. Q6 (pricing without comps). ', 'Q8 delivers the usable pricing script.')
bullet('4. Q3 (where the story stops). ', 'Only if Q1 and Q2 already produced a limit.')
h3('Never cut')
bullet('', 'Q1 (the merchandiser\'s eye), Q5 (Lendl), Q8 (exact words), Q11 (the objection), Q14 (co-primary).')

doc.add_page_break()

# =====================================================================
# 4. RESEARCH BRIEF
# =====================================================================
h1('4. Research Brief')
p('Read the morning of. Not during the interview.', italic=True)

h2('4A. Background')
p('Bill spent 28 years at Ralph Lauren in merchandising, ending as Chief Merchandising Officer. He and his husband Stephen started coming to Sharon, CT as weekenders in 2013, restored an antique saltbox, and moved up full-time. He joined Elyse Harney Real Estate in 2019 in his fifties, co-listed the county-record Ivan Lendl sale in January 2024, and now works mostly $1.5 million and up across Northwest Connecticut.')

h2('4B. Career Timeline')
table(['Year', 'Role / Company', 'Notable'], [
    ['Until 2019', 'Ralph Lauren, merchandising, ending as Chief Merchandising Officer', '28 years (his count). Earlier roles not public.'],
    ['2013', 'Weekender in Sharon, CT', 'Bought and restored an antique saltbox'],
    ['2019', 'Joins Elyse Harney Real Estate', 'Realtor.com says 2018. Ask.'],
    ['Jan 2024', 'Co-lists Ivan Lendl estate', '$12M, Litchfield County residential record'],
    ['2025', 'California relocation buyers', 'Three deals after the wildfires'],
    ['2026', 'National press run', 'Realtor.com "anti-Hamptons," Daily Mail, citybiz, Leading Estates of the World'],
], widths=[1.0, 3.2, 2.6])

h2('4C. What Makes Him Interesting for This Audience')
bullet('Career changer who won fast: ', 'He started in his fifties and co-listed a county record within five years. Proof that the second career is not a handicap.')
bullet('A merchandiser\'s eye: ', 'He thinks about houses the way a brand thinks about a store. Positioning is a skill agents rarely get taught.')
bullet('Pricing a one-of-one: ', 'The Lendl estate took a decade and a $7.8 million drop from its first ask. Every agent has a version of that seller.')
bullet('Sphere-built, not lead-bought: ', 'He says his business is relationships leading to relationships. KIR listeners always want the mechanism behind that sentence.')
bullet('He lived the trend: ', 'He was the weekender who went full-time. He can speak to the buyer and as the buyer.')

h2('4D. Key Data Points')
table(['Stat', 'Source', 'Confidence'], [
    ['Lendl estate sold $12M, Jan 25, 2024, county residential record', 'Lakeville Journal; The Real Deal', 'High'],
    ['445 acres (152 Cornwall, 293 Goshen); prior record $11.5M Kent 2008', 'Lakeville Journal', 'High'],
    ['First listed ~2014 at $19.8M; $16.4M in 2021; final ask $14.995M', 'The Real Deal; Lakeville Journal', 'High'],
    ['Co-listed with Elyse Harney Morris; buyer agent from William Raveis', 'Lakeville Journal', 'High'],
    ['28 years at Ralph Lauren, ending as CMO', 'Intake; Harney bio', 'Medium (press says "26 years as CMO")'],
    ['Joined Harney in 2019', 'Harney; citybiz', 'Medium (Realtor.com says 2018)'],
    ['207+ transactions, $144M+ career volume', 'Intake only (agent page shows 212 closed)', 'Unverified'],
    ['Top 1% Litchfield County; #2 Northern Litchfield', 'Harney bio', 'Unverified'],
    ['Three California transactions in 2025', 'citybiz, April 2026', 'Medium'],
    ['Litchfield values up ~30% since the pandemic', 'citybiz; Digital Journal (Bill\'s claim)', 'Medium'],
    ['Litchfield median list $650K, 85 DOM vs East Hampton $2.8M', 'Realtor.com, Feb 2026', 'High'],
    ['Quoted in WSJ, NYT; appeared on Fox Business', 'Intake only', 'Unverified'],
], widths=[3.3, 2.3, 1.2])

h2('4E. Previous Media Appearances')
bullet('Realtor.com (Julie Taylor), Feb 14, 2026: ', 'Coined "anti-Hamptons." Commute, crowds, price per acre versus the Hamptons.')
bullet('Daily Mail (Benjamin Curry), 2026: ', 'Anti-Hamptons, California wildfire buyers, Wall Street bonus money.')
bullet('citybiz (two pieces) and Digital Journal, early 2026: ', 'Career reinvention at 50, market up 30%, $1.5M to $2.5M sweet spot, Lendl.')
bullet('Leading Estates of the World, July 31, 2026: ', 'Trophy properties, pricing, discretion.')
bullet('The Real Deal, Mansion Global, Lakeville Journal, Jan-Feb 2024: ', 'Lendl sale news coverage.')
bullet('Note: ', 'Many of the 2026 pieces are KeyCrew Media placements syndicated to press-release sites. KeyCrew\'s "Verified Expert" label is a PR product, not an award. Do not call it an honor on air.')
bullet('Podcasts: ', 'No prior podcast appearances found, and no prior KIR appearance.')

h2('4F. Their Own Words')
table(['Quote', 'Where and when', 'Confidence', 'How D.J. uses it'], [
    ['"They\'re not just buying square footage. They\'re buying frontage, views and an experience that can\'t be replicated."', 'Salisbury market piece, Sept 2026', 'Reported', 'Paraphrase to set up Q3.'],
    ['"Pricing is everything, even at that end of the market."', 'Leading Estates of the World, July 2026', 'Reported', 'Read back to open Q6.'],
    ['"Trophy properties require a completely different playbook. You have to be proactive. You can\'t wait for the right buyer to find you."', 'citybiz, April 2026', 'Reported', 'Reserve. If Q5 goes vague, read it and ask "What did proactive look like on Lendl?"'],
    ['"If everything starts to feel automated or AI-generated, I think you lose some of what people are actually hiring you for."', 'His intake', 'Verbatim', 'Read it back in Q13 if he hedges.'],
    ['"That was the first one I lost to a beaver."', 'His intake', 'Verbatim', 'The button line for Q16. Let him deliver it.'],
    ['"I never really thought of myself as a traditional salesperson."', 'His intake', 'Verbatim', 'Read back to open Q10.'],
], widths=[2.4, 1.4, 0.9, 2.1])

h2('4G. Audience Relevance')
table(['Segment', 'What they get'], [
    ['Individual agents', 'A method to position any listing, a price-reduction script, and one question for dual-home buyers.'],
    ['Team leaders', 'How to price one-of-one listings and farm through institutions.'],
    ['Broker-owners', 'How to onboard the experienced second-career agent (Q12).'],
    ['New agents', 'Proof you can start late, plus a sphere cadence to copy.'],
], widths=[1.6, 5.2])

doc.add_page_break()

# =====================================================================
# 5. LIVE STREAM TITLE, DESCRIPTIONS AND HASHTAGS
# =====================================================================
h1('5. Live Stream Title, Descriptions and Hashtags')
h2('5A. Live Stream Title')
quoted('Live stream title:', LIVE_TITLE + '  (' + str(len(LIVE_TITLE)) + ' characters)')
quoted('Backup:', LIVE_BACKUP + '  (' + str(len(LIVE_BACKUP)) + ' characters)')
p('This does not have to match the published episode title. Pick that after the interview.', italic=True)

h2('5B. Platform Descriptions')
rich([('Facebook: ', True), ('Bill Melnick spent 28 years at Ralph Lauren. Then he started over in real estate in his fifties and helped sell Ivan Lendl\'s estate for a county record. We\'re talking about how to sell the life, not the square footage. Drop your questions in the comments!', False)])
rich([('Instagram: ', True), ('Ralph Lauren exec turned luxury agent. How to sell the life, not the house. @bill_melnick_real_estate #KeepingItReal #LuxuryRealEstate #CareerChange', False)])
rich([('TikTok: ', True), ('He lost a deal to a beaver. He also broke a county record. #realtortok #luxuryrealestate #realestateagent', False)])
rich([('YouTube: ', True), ('Bill Melnick of Elyse Harney Real Estate joins the Keeping It Real Podcast. He spent 28 years at Ralph Lauren before real estate, co-listed Ivan Lendl\'s $12 million Litchfield County estate, and breaks down how to price, present and position a home by selling the lifestyle.', False)])
rich([('LinkedIn: ', True), ('Bill Melnick left a Chief Merchandising Officer role at Ralph Lauren to start over in real estate. Today we cover how brand and merchandising skills turn into pricing power, and how he built a business on his existing network.', False)])

h2('5C. Hashtags')
bullet('Universal: ', '#KeepingItReal #RealEstatePodcast #DJParis #RealtorLife #RealEstateAgent')
bullet('Episode: ', '#LuxuryRealEstate #LitchfieldCounty #SecondHome #CareerChange #ListingPresentation #SphereOfInfluence #ConnecticutRealEstate')
bullet('Guest tags: ', '@bill_melnick_real_estate, Elyse Harney Real Estate (@harneyrealestate, confirm handle)')

# =====================================================================
# 6. YOUTUBE CHAPTERS
# =====================================================================
h1('6. YouTube Chapter Markers')
table(['Timestamp', 'Chapter title'], [
    ['0:00', 'Ivan Lendl\'s Estate Sat for a Decade. Here\'s What Sold It.'],
    ['2:00', 'Rapid Fire: Best and Worst Real Estate Advice'],
    ['4:00', 'What a Ralph Lauren Merchandiser Sees in a House'],
    ['6:00', 'How to Prep a Listing Like a Luxury Brand'],
    ['8:00', 'When the Lifestyle Story Stops Beating the Comps'],
    ['10:00', 'The Ralph Lauren Move for a $450K House'],
    ['12:00', 'Selling Ivan Lendl\'s $12M Connecticut Estate'],
    ['15:00', 'How to Price a Home With No Comps'],
    ['17:00', 'Managing Up With a Famous Seller'],
    ['19:00', 'Exact Words for an Overpriced Seller'],
    ['21:00', 'Leaving Ralph Lauren and Starting Over at 50-Something'],
    ['23:00', 'The Sphere of Influence System That Built His Business'],
    ['26:00', 'What If Your Sphere Isn\'t Rich?'],
    ['28:00', 'What Brokers Should Do for Career-Changer Agents'],
    ['29:30', 'What AI Should Never Do in Real Estate'],
    ['31:00', 'The Co-Primary Home Buyer, Explained'],
    ['34:00', 'Farming Prep-School Families'],
    ['36:30', 'The Deal He Lost to a Beaver'],
    ['38:30', 'One Question That Spots a Co-Primary Buyer'],
    ['40:00', 'Homework and Where to Find Bill Melnick'],
], widths=[1.0, 5.8])

doc.add_page_break()

# =====================================================================
# 7. STRESS TEST, COUNCIL, EP POLISH
# =====================================================================
h1('7. Stress Test, Council Review and EP Polish')
h2('7A. Stress Test')
table(['#', 'What broke', 'Fix applied'], [
    ['1', 'Fact conflict: press says "26 years as CMO," Bill says 28 years at the company.', 'All copy says "28 years at Ralph Lauren." Flagged on the card; Bill gives his own title arc.'],
    ['2', 'Fact conflict: start year 2019 (Harney) vs 2018 (Realtor.com).', 'Doc uses 2019, timeline notes the conflict, never stated as a year on air.'],
    ['3', 'The draft said Bill "sold" the Lendl estate. He co-listed it with Elyse Harney Morris.', 'Q5, cold open and titles now say "you and Elyse" or "one of the two agents."'],
    ['4', 'Unverifiable: WSJ, NYT and Fox Business, and $144M volume.', 'Marked guest-supplied. Kept out of titles, cold open and descriptions.'],
    ['5', 'Spent questions: his best and worst advice come out in Rapid Fire.', 'Built callbacks into Q7 and Q13 and put the "coming back to that" line on the card.'],
    ['6', 'Drift risk: a Litchfield market update (30% growth, anti-Hamptons) is his press default.', 'Listed both as overasked. Block 4 frames co-primary as a buyer type every agent sees, not a Connecticut stat.'],
    ['7', 'Dodgeable: Q10 sphere answer can be "I just stay in touch."', 'If-vague follow-up demands a number from last week.'],
    ['8', 'Gotcha risk: Q9 on leaving Ralph Lauren could read as prying about a layoff.', 'Permission clause added and framed around his own Digital Journal quote.'],
    ['9', 'Runtime: 17 questions plus Rapid Fire is over the 16 ceiling.', 'Q12 is first on the cut list; four-question cut list written.'],
], widths=[0.3, 3.0, 3.5])

h2('7B. Council Review')
h3('Member notes')
table(['Member', 'What they\'d change'], [
    ['Hormozi', 'Q4 is the money question for 90% of listeners. Protect it. The market stats are fluff.'],
    ['MrBeast', 'The sag is minutes 20 to 30 if Q9 turns into a memoir. Keep it to one question and move.'],
    ['Brendan Kane', 'Title 1 is the concept plus stat ingredient. Test it against the reinvention title.'],
    ['Donald Miller', 'The hero is the agent with an ordinary listing, not Bill. The homework has to prove it.'],
    ['Eric Simon', 'The beaver is the share. Every agent has a "deal died for a stupid reason" story.'],
    ['Chris Do', 'Q9 is the only question that costs him something. Do not cut it for time.'],
    ['Jon Youshaei', 'Chapters are specific and searchable. Keep "Exact Words for an Overpriced Seller."'],
], widths=[1.5, 5.3])
p('Disagreement: Kane wants to lead with the Lendl gap. Chris Do wants the reinvention story. Decision: lead with Lendl in the cold open and title for clicks. Keep reinvention as the Block 3 emotional beat, where it earns more.', italic=True)

h3('Title (pick one, keep others for A/B)')
table(['#', 'Title', 'Ingredient', 'Curiosity mechanism'], [
    ['1', 'Ivan Lendl\'s Estate Sat for 10 Years. A Former Ralph Lauren Exec Helped Sell It. (Bill Melnick)', 'Stat + concept', 'What changed? Gap opens before the answer.'],
    ['2', 'The Ralph Lauren Playbook for Selling Houses (Bill Melnick)', 'Insight', 'What does fashion know about houses?'],
    ['3', 'He Left Ralph Lauren in His 50s. Now He Holds a $12M County Record. (Bill Melnick)', 'Personality + stat', 'Reinvention arc.'],
], widths=[0.3, 3.3, 1.2, 2.0])
p('Recommended: #1. It uses only verified facts and names a celebrity, which is the best click driver for a guest listeners don\'t know yet.', italic=True)

rich([('Cold-open hook (sharpened): ', True), ('"Ivan Lendl\'s Connecticut estate went on the market at almost $20 million and sat for the better part of a decade. When it finally sold, it broke the county record, and one of the two agents on it spent 28 years at Ralph Lauren. We\'re going to talk about that today. Stay tuned."', False, True)])

h3('The Clip Engine')
table(['Q#', 'Question', 'Berger emotion', 'Heath gap'], [
    ['16', 'You lost a deal to a beaver. What happened?', 'Amusement (high arousal)', 'Absurd setup, payoff line in his intake.'],
    ['8', 'Overpriced seller, 90 days in. Your exact words?', 'Anxiety, then relief', 'Every agent wants the script they dread using.'],
    ['11', 'Your sphere was Ralph Lauren. What about the agent whose isn\'t?', 'Indignation, then hope', 'Names the listener\'s objection before answering it.'],
], widths=[0.4, 2.8, 1.6, 2.0])

h3('Live-description scrub')
table(['Platform', 'Verdict and fix'], [
    ['Facebook', 'Keep. Credits the team ("helped sell").'],
    ['Instagram', 'Keep. Short and tags him.'],
    ['TikTok', 'Keep. The beaver line is the native hook.'],
    ['YouTube', 'Keep. Guest, brokerage, Lendl and show name are all searchable.'],
    ['LinkedIn', 'Keep. The business angle is the network, not the house.'],
], widths=[1.3, 5.5])

rich([('Arc fix: ', True), ('The sag risk is Block 3 turning into career memoir. Q9 is one question with a tight short version, and Q10 demands a number right away.', False)])
h3('Why it should work')
bullet('Curiosity (Heath): ', 'A decade on the market plus a record sale is a contradiction the listener has to resolve.')
bullet('Share driver (Berger): ', 'The beaver clip is funny and the Q8 script is useful. Both are easy to forward.')
bullet('Retention (MrBeast): ', 'Every block ends on a do-it-tomorrow question, and the Rapid Fire sets up two callbacks.')
rich([('The dissent: ', True), ('Chris Do still thinks the reinvention title wins with the career-changer audience. A/B title 3 against title 1 on the YouTube thumbnail test.', False)])

h2('7C. EP Polish (pass 3)')
bullet('', 'Changed every "Bill sold the Lendl estate" to credit Elyse Harney Morris, after the stress test caught the co-listing.')
bullet('', 'Removed $144M and the WSJ, NYT and Fox Business claims from the titles, cold open and descriptions because they couldn\'t be verified.')
bullet('', 'Moved the AI question into Block 3 as its do-it-tomorrow close, so the worst-advice callback lands next to the sphere discussion.')
bullet('', 'Promoted the beaver story from a spare anecdote to Q16, with a backup in case Rapid Fire spends it.')
bullet('', 'Added Q4 (the $450K house) so the luxury method translates to the mass-market listener.')
bullet('', 'Rewrote the homework to produce a written sentence and a text sent this week instead of "think about your clients."')
bullet('', 'Added permission clauses to Q5, Q7 and Q9 only.')

doc.save("/Users/djparis/GitHub Projects/keeping-it-real-content-system/guest-prep/Bill_Melnick_Interview_Prep.docx")
print("Saved Bill_Melnick_Interview_Prep.docx")
