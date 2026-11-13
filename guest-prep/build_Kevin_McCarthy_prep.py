#!/usr/bin/env python
# Builds the KIRP interview prep .docx for Kevin McCarthy, co-founder of Real Geeks (Dallas, TX)
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






LIVE_TITLE = "How to Get Your Website Found in ChatGPT Search (Real Geeks Co-Founder Kevin McCarthy)"
LIVE_BACKUP = "AI Wrote 38,000 Agent Web Pages. Here's What Works (Kevin McCarthy)"

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
r = sub.add_run('Interview Prep: Kevin McCarthy')
r.bold = True
r.font.size = Pt(20)
sub2 = doc.add_paragraph()
sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub2.add_run('Co-Founder, Real Geeks  |  Dallas, TX  |  Target runtime 43 minutes')
r.italic = True
r.font.size = Pt(10)

# =====================================================================
# 1. QUICK REFERENCE CARD
# =====================================================================
h1('1. Quick Reference Card')
p('One page. Glance at this during the interview.', italic=True, space=8)

h3('Who he is')
bullet('Name: ', 'Kevin McCarthy. Co-founder of Real Geeks (IDX websites, CRM, marketing and AI for agents).')
bullet('Title: ', "Sources disagree. Real Geeks' Nov 12, 2026 press release says \"co-founder and CEO/CTO.\" The intro email says co-founder and CTO. An old Inman bio says COO. On air, say \"co-founder of Real Geeks\" and ask his preferred title pre-show.")
bullet('Background: ', 'Purdue computer science grad. Moved to Hawaii in 2007 to work with Jeff Manson, a real estate agent, and they started Real Geeks there. Has taught programming classes and written open-source libraries (Inman bio).')
bullet('Company: ', 'Started in Hawaii in 2007 (company site). Moved to Dallas in 2016. Acquired by Fidelity National Financial in 2017. Employees in Hawaii and 10+ other states. The About page says "Kevin leads the company."')
bullet('Why he is here: ', 'AI Connect, launched October 2026. It lets ChatGPT, Claude or a coding agent like Claude Code edit a Real Geeks website through MCP (Model Context Protocol). Included with the base platform.')
bullet('KIR connection: ', 'Real Geeks is a current KIR sponsor. No prior Kevin appearance in the catalog. Closest past episode: Bobby Kerr, "Get Found on Google: The Real Estate Agent\'s Guide to AI Search." That one was Google Business Profile. This one is the website. Don\'t repeat Bobby\'s ground.')
bullet('Guest type: ', 'C (tech/vendor). Max 20% of questions about AI Connect. Every product question has an "if you don\'t use Real Geeks" angle.')

h3('Verified (safe to say on air)')
bullet('', 'Press release, Nov 12, 2026: since October, AI Connect has created about 38,000 new pages and posts and edited another 120,000, across hundreds of Real Geeks websites. Hundreds of clients use it each week. (Company numbers. Say "Real Geeks says.")')
bullet('', 'Client Scott Bergmann (Nebraska): "absolutely game-changing. I\'m obsessed with it." (Read this version. The wording in the intro email is slightly off.)')
bullet('', 'Client Vince Vizzaccaro (Florida): page views per visitor doubled, 1.4 to 2.9 (press release, client-reported).')
bullet('', 'Conductor 2026 benchmark: AI referrals are about 1% of real estate website traffic, and ChatGPT is about 95% of those clicks.')
bullet('', 'Kevin, Nov 2026: "I\'ve been doing this for almost 20 years."')

h3('Guest supplied, do not state as verified')
bullet('', 'Kevin\'s line that Real Geeks is "the only real estate IDX software" an AI agent can build pages on. It\'s his claim. Let him say it. Don\'t repeat it as fact.')
bullet('', 'Founding year: 2007 (company), 2008 with a 2012 official launch (old Inman bio). Say "almost 20 years," his own words.')
bullet('', 'Current ownership after 2017: not confirmed. Don\'t bring it up.')

h3('Episode')
bullet('The Core Topic: ', 'Getting an agent\'s website found by ChatGPT and AI search: what the AI actually reads, and how to build it without a webmaster or a weekend.')
bullet('Overasked questions to avoid: ', '"How did Real Geeks start on a beach in Hawaii?" (company site, Listing Bits podcast "The Story of Real Geeks"). "Will AI replace agents?" (every AI episode, KIR included). "What is IDX?"')
bullet('The "I\'ve interviewed hundreds" moment: ', 'Q13 only. "I\'ve interviewed hundreds of agents, and I can\'t remember one who said their website was where the business came from." (Only say it if it\'s true for you.)')
bullet('Live stream title: ', LIVE_TITLE + ' (' + str(len(LIVE_TITLE)) + ' characters)')
bullet('Sponsor disclosure: ', 'Say it once, early: "Real Geeks sponsors the show, and I asked Kevin on because this is the question I get most from agents."')
bullet('Watch out for: ', 'Rapid Fire Q3 (one tool you can\'t live without). He\'ll likely say Claude Code or AI Connect, which is Block 3. Say "Love it, and we\'re coming back to that."')
bullet('Drift guard: ', 'He\'s a programmer. If it turns into MCP vs. API vs. CLI, say "Explain it like I\'m an agent who\'s never opened a terminal." If it turns into a demo, say "What does the agent who doesn\'t use Real Geeks do Monday?"')
rich([('ASK THE SHORT VERSION.  COUNT TO THREE BEFORE YOU RESPOND.', True)], space=4)

doc.add_page_break()

# =====================================================================
# 2. EPISODE FRAMEWORK
# =====================================================================
h1('2. Episode Framework')
h2('2A. Title Options')
table(['#', 'Title', 'Why it works'], [
    ['1', 'How to Get Your Website Found in ChatGPT Search (Real Geeks Co-Founder Kevin McCarthy)', 'The exact question agents are typing. Searchable. Guest name plus authority.'],
    ['2', 'AI Wrote 38,000 Agent Web Pages in a Month. Here\'s What Actually Works (Kevin McCarthy)', 'Real stat plus a quality tension. Opens a gap: which ones worked?'],
    ['3', 'Your Website Has a New Visitor, and It\'s Not Human (Kevin McCarthy, Real Geeks)', 'Curiosity first. Weakest on search, strongest as a clip title.'],
], widths=[0.3, 3.9, 2.6])

h2('2B. Cold Open Hook')
p('"Agents keep asking me the same question: how do I get ChatGPT to recommend me? Today\'s guest has watched AI tools build about 38,000 real estate web pages in roughly a month, and he knows which ones actually matter. We\'re going to talk about that today. Stay tuned."', italic=True)

h2('2B-2. Guest Intro (read after the cold open)')
p('Says "co-founder" only. If he confirms CTO or CEO pre-show, add it after "co-founder."', italic=True)
rich([('Short (about 20 seconds): ', True), ('"Kevin McCarthy is the co-founder of Real Geeks, the website, CRM and marketing platform used by real estate agents across the country. A Purdue computer science grad, Kevin moved to Hawaii in 2007 to team up with a real estate agent, and the two started Real Geeks there. Almost 20 years later, he\'s still building tools for agents. His newest one, AI Connect, lets agents edit their own websites just by talking to ChatGPT or Claude."', False, True)])
rich([('Longer (show notes): ', True), ('Kevin McCarthy is the co-founder of Real Geeks, which gives real estate agents IDX websites, a CRM, marketing tools and AI. Kevin is a programmer first. He studied computer science at Purdue, has taught programming classes, and has released open-source software. In 2007 he moved to Hawaii to work with real estate agent Jeff Manson, and the two started Real Geeks there. The company moved to Dallas in 2016, and Fidelity National Financial bought it in 2017. Today Kevin leads the company. In October 2026, Real Geeks launched AI Connect, which lets agents connect ChatGPT, Claude or another AI tool to their website so they can create and update pages just by asking. Real Geeks says agents made about 38,000 new pages and posts with it in the first month.', False)])

h2('2C. Episode Arc')
rich([('Core Topic: ', True), ('Getting found in AI search: what ChatGPT reads on an agent\'s website, and how to build it in minutes instead of never.', False)])
rich([('Why this topic: ', True), ('It\'s what Kevin was told the show is about, it\'s the question listeners ask most, and he has data nobody else has (158,000 AI-made page changes). The Bobby Kerr episode covered Google Business Profile, so this stays on the website. AI Connect lives inside Block 3 as one way to do it, not the point of the episode.', False)])
table(['Block', 'Angle', 'Ends on'], [
    ['1', 'What the AI actually reads', 'The test you run on yourself tonight'],
    ['2', 'Volume vs. slop', 'The one page every agent should write first'],
    ['3', 'Your website, by conversation', 'Your first three prompts'],
    ['4', 'The case for the website at all', 'What to stop doing'],
], widths=[0.6, 2.8, 3.4])

doc.add_page_break()

# =====================================================================
# 3. INTERVIEW QUESTIONS
# =====================================================================
h1('3. Interview Questions')
p('Questions are numbered 1 to 15 across all blocks, so you can call one out by number.', italic=True)

h2('Rapid Fire (0:00-2:00, read as written, no follow-ups)')
for i, rq in enumerate([
    "Best real estate advice you've ever received?",
    "Worst real estate advice you've ever received?",
    "One tool or app you can't run your business without?",
    "What would surprise people most about your day-to-day?",
], 1):
    rich([('RF' + str(i) + '. ', True), (rq, False)], space=2)
p('Say "Love it" or "Great answer" and move on. If RF3 is Claude Code or AI Connect: "Love it, and we\'re coming back to that."', italic=True)

# ---------------- BLOCK 1
h2('Block 1: What the AI Actually Reads (2:00-12:00)')
p('Audience note: every agent, whatever website they use. This is the diagnosis.', italic=True)
p('Arc: the question, the mechanism, the myth, the test.', italic=True)

q(1, "Here's the question I get more than any other right now: \"D.J., how do I get ChatGPT to recommend me?\" You've been building agent websites for almost 20 years. When a buyer asks ChatGPT \"who's a good agent in my neighborhood,\" what is it actually looking at?",
  'Pick one neighborhood. Walk me through where the answer comes from, step by step.',
  'The real mechanism: which sources AI pulls (website, reviews, directories, portals), and how much the agent\'s own site counts.',
  'All segments',
  short="How do I get ChatGPT to recommend me? What is it actually reading?")

q(2, "Conductor's 2026 benchmark says AI is only about 1% of the traffic to real estate websites right now. An agent hears that and thinks, \"So why bother?\" What's the answer?",
  'Is 1% the wrong number to look at? What number should they look at?',
  'Whether AI visitors convert better, and whether the bigger effect is the recommendation itself, without a click.',
  'Individual agents, broker-owners',
  short="AI is about 1% of website traffic. Why should an agent care?")

q(3, "What's the biggest myth agents believe about showing up in AI search?",
  'Give me the thing you\'ve seen an agent spend money on that did nothing.',
  'A specific wasted tactic (keyword stuffing, paying for an "AI SEO" package, a pretty homepage with no text). The contrarian beat.',
  'Individual agents',
  short="Biggest myth about getting found in AI search?")

q(4, "Give me the test. An agent's listening in their car. Tonight, what do they type into ChatGPT to find out if they're invisible, and what do they look for in the answer?",
  'What exact words do they type? What counts as a pass?',
  'A repeatable self-audit: the prompt, plus asking the AI which sources it used. Sets up the homework.',
  'Individual agents, new agents',
  short="What do they type tonight to find out if they're invisible?")

bridge("So the AI is reading your website, and most sites don't give it much to read. The fix sounds like more content, and that's where it gets messy.")

# ---------------- BLOCK 2
h2('Block 2: Volume vs. Slop (12:00-22:00)')
p('Audience note: agents who already tried AI-written blog posts and saw nothing, and team leads thinking about doing it at scale.', italic=True)
p('Arc: the number, the quality line, the failure, the first page.', italic=True)

q(5, "Real Geeks says that in about a month, your clients' AI tools created roughly 38,000 new pages and posts and edited another 120,000. When you look at that pile, what separates the pages that work from the ones that are just noise?",
  'Show me one good page and one bad page. What\'s different?',
  'His quality bar: local specifics, first-hand knowledge, answering real buyer questions vs. generic filler.',
  'Individual agents, team leaders',
  short="38,000 new pages. What separates the ones that work from the noise?")

q(6, "Here's my worry, and I think a lot of agents share it. If every agent can now spin up 50 neighborhood pages in an afternoon, doesn't that just flood the internet with the same page 10,000 times? Why would Google or ChatGPT reward any of it?",
  'So what does the agent have that the AI can\'t write for them?',
  'The honest limit of AI content. What only the agent can add (real sales, opinions, photos, local quirks).',
  'All segments',
  short="If everyone can make 50 pages, why would AI reward any of them?",
  note='This is the tension question. Don\'t let him answer with "our tool is better." The answer has to be about the agent.')

q(7, "What's a mistake you've already seen, an agent letting the AI loose and it backfiring?",
  'What happened, and how did they fix it?',
  'A real failure story (wrong facts, typos at scale, off-brand voice, fair housing language). Credibility.',
  'Individual agents, broker-owners',
  permission="Don't name names, but",
  short="What's a mistake you've seen, AI loose on a website and backfiring?")

q(8, "If an agent writes exactly one page this month, what page is it and what goes on it?",
  'Give me the headline and the three things on that page.',
  'A specific page type (one neighborhood, one buyer question) with a structure an agent can copy.',
  'Individual agents, new agents',
  short="One page this month. Which page, and what goes on it?")

bridge("So the content has to come from you, and AI just does the typing. Let's talk about how the typing actually happens, because that part changed in October.")

# ---------------- BLOCK 3
h2('Block 3: Your Website, by Conversation (22:00-32:00)')
p('Audience note: Real Geeks clients get the how-to. Everyone else gets what to look for in their own platform.', italic=True)
p('Arc: the before, the how, the guardrail, the first prompts.', italic=True)

q(9, "Explain AI Connect to an agent who's never opened a line of code. What's the before and after?",
  'Before: what did changing a page take? After: what do they type?',
  'The plain-English version: connect ChatGPT or Claude, approve what it can touch, then just ask. Keep it to two minutes.',
  'Individual agents',
  short="Explain AI Connect to an agent who's never seen code. Before and after?",
  note='Callback here if RF3 was AI Connect or Claude Code.')

q(10, "I'd guess most of my listeners aren't on Real Geeks. What should they ask their website company tomorrow to find out if they can do any of this?",
  'Give me the exact question to email their provider.',
  'Portable standard: can my AI tool connect, can I control what it edits, is there change history and a draft mode.',
  'Individual agents, broker-owners',
  short="Not on Real Geeks. What do they ask their website company tomorrow?")

q(11, "Giving an AI the keys to your website makes some people nervous. What can't it touch, and what's the one thing an agent should never let it do without reading first?",
  'Has anyone had to roll back a change? What happened?',
  'The guardrails (permissions, drafts, change history, revoke) and his honest line on human review. The blog says "you should still review what your AI creates."',
  'Broker-owners, team leaders',
  short="What can't the AI touch, and what should you always read first?")

q(12, "Give me the first three prompts. An agent connects their AI tonight. What do they type, in order?",
  'Read them like you\'d type them.',
  'Three copyable prompts (fix typos sitewide, build one area page, write a post about a new listing). The do-it-tomorrow moment.',
  'Individual agents, new agents',
  short="First three prompts, in order. What do they type?")

bridge("So now any agent can keep a website current in ten minutes. Which raises the bigger question, the one I actually wanted to ask a guy who's been building these for 20 years.")

# ---------------- BLOCK 4
h2('Block 4: The Case for the Website at All (32:00-40:00)')
p('Audience note: the referral-only agent who thinks none of this applies to them, and broker-owners deciding what to pay for.', italic=True)
p('Arc: the skeptic, the shift, the stop list.', italic=True)

q(13, "I've interviewed hundreds of agents, and I can't remember one who said their website was where the business came from. It's referrals, sphere, open houses. Make the case to that agent. Why does their website matter now?",
  'Even for a referral? Walk me through a referral who looks you up first.',
  'The objection said out loud: the referral gets vetted by AI and the website before the call. Reframes the site as proof, not lead gen.',
  'Individual agents, broker-owners',
  short="Most agents say their website brings in nothing. Make the case to them.")

q(14, "You've built agent websites for almost 20 years. What's the thing you were sure about five years ago that you've completely changed your mind on?",
  'What made you change your mind?',
  'A personal reversal from the builder himself. The vulnerable beat, and it sets up what to stop doing.',
  'All segments',
  short="What were you sure about five years ago that you've changed your mind on?")

q(15, "What should agents stop doing on their websites starting today?",
  'Name one thing on most agent sites you\'d delete.',
  'A clear stop list (stale market reports, empty blog, stock photos, a homepage with no words). A clean clip to end on.',
  'Individual agents, new agents',
  short="What should agents stop doing on their websites today?")

# ---------------- CLOSE
h2('The Close (40:00-43:00)')
rich([('Homework (read verbatim): ', True)], space=2)
p('"Here\'s what I want you to do before the next episode. Open ChatGPT or Claude and type: who are the best real estate agents for [your neighborhood] in [your city]? Then ask: what sources did you use? If you\'re not in the answer, write down the three questions buyers ask you most about that neighborhood. That\'s your first page. Not next month. This week."', italic=True)
rich([('Guest close: ', True), ('"Kevin, where can people find you and learn more about Real Geeks?" Ask pre-show if there\'s a listener offer or the setup guide link to mention.', False)])

h3('If you\'re running long, cut these first')
bullet('Q14 ', '(changed his mind). Great if there\'s time, but nothing downstream depends on it.')
bullet('Q3 ', '(biggest myth). Q6 covers the same ground with more tension.')
bullet('Q2 ', '(the 1% stat). Fold it into Q13 if needed.')
bullet('Q10 ', '(ask your provider). Only cut if Q9 already covered non-Real Geeks agents.')

h3('Never cut')
bullet('Q1 ', '(what ChatGPT reads). The whole episode answers it.')
bullet('Q4 ', '(the self-test). Sets up the homework.')
bullet('Q6 ', '(why would AI reward any of it). The tension that keeps this from being an ad.')
bullet('Q12 ', '(first three prompts). The thing people screenshot.')
bullet('Q13 ', '(the referral-only agent). The objection said out loud.')

doc.add_page_break()

# =====================================================================
# 4. RESEARCH BRIEF
# =====================================================================
h1('4. Research Brief')
p('Read the morning of, not during the interview.', italic=True)

h2('4A. Background')
p("Kevin McCarthy is a Purdue computer science grad who moved to Hawaii in 2007 to work with real estate agent Jeff Manson. The two started Real Geeks to build better websites and lead tools for agents. The company moved to Dallas in 2016 and was bought by Fidelity National Financial in 2017, which said Real Geeks served individual agents at a lower price point than its sister company CINC. Kevin now leads the company. He's an engineer first: he's taught programming classes and released open-source code, and he talks about AI Connect as the feature he's most excited about in almost 20 years.")

h2('4B. Career Timeline')
table(['Year', 'Role / Company', 'Notable'], [
    ['2007', 'Moves to Hawaii, starts Real Geeks with Jeff Manson', 'Company dates its founding to 2007 (old Inman bio says 2008, official launch 2012)'],
    ['2016', 'Real Geeks', 'Company relocates to Dallas'],
    ['2017', 'Real Geeks', 'Acquired by Fidelity National Financial (July 2017)'],
    ['Jul 2026', 'Real Geeks', 'Geek AI 3.0: agentic AI assistants inside the platform'],
    ['Oct 2026', 'Real Geeks', 'AI Connect launches'],
    ['Nov 12, 2026', 'Real Geeks', 'AI Connect press release with first usage numbers'],
], widths=[1.0, 2.8, 3.0])

h2('4C. What Makes Him Interesting for This Audience')
bullet('He has the data: ', 'about 158,000 AI-made page changes in a month. Nobody else on the show has seen that much AI real estate content.')
bullet('He\'s the builder, not the marketer: ', 'a CS grad can explain how the AI reads a page in plain terms, if you hold him to it.')
bullet('Founded with an agent: ', 'Real Geeks started as a programmer plus a producing agent, so he\'s seen what agents actually use vs. what they buy.')
bullet('Timely: ', 'the press release went out Nov 12, 2026, one day before this prep. The episode rides fresh news.')
bullet('Portable lesson: ', 'the "make your AI do the website" idea works on any platform that allows it. Listeners not on Real Geeks still walk away with something.')

h2('4D. Key Data Points')
table(['Stat', 'Source', 'Confidence'], [
    ['~38,000 new pages/posts and ~120,000 edits since October launch', 'Real Geeks press release, Nov 12, 2026', 'Medium (company-reported)'],
    ['Hundreds of clients use AI Connect weekly', 'Real Geeks press release', 'Medium (company-reported)'],
    ['Client page views per visitor 1.4 to 2.9', 'Press release (Vince Vizzaccaro)', 'Medium (one client)'],
    ['AI included in the base Real Geeks platform; AI provider plan may cost extra', 'Real Geeks blog, Oct 6, 2026', 'High'],
    ['AI referrals ~1% of real estate site traffic; ChatGPT ~95% of AI clicks', 'Conductor 2026 benchmark (enterprise sites)', 'Medium'],
    ['Geek AI Text: $49/mo up to 2,500 new lead conversations', 'Real Geeks blog, Jul 1, 2026', 'High'],
    ['Acquired by Fidelity National Financial, July 2017', 'Real Geeks About page, Inman, HousingWire', 'High'],
], widths=[3.0, 2.5, 1.3])

h2('4E. Previous Media Appearances')
bullet('Listing Bits podcast: ', '"Building Real Estate Technology: The Story of Real Geeks with Kevin McCarthy." Date and topics not retrieved. Assume the origin story is covered.')
bullet('Real Estate News, Oct 16, 2026: ', 'quoted on AI Connect as a "game changer."')
bullet('Inman: ', 'has a contributor bio page, no articles found.')
bullet('Note: ', 'very little long-form interview footage turned up. Most of his public words are from the last six weeks of AI Connect launch material.')

h2('4F. Their Own Words')
table(['Quote', 'Where and when', 'Confidence', 'How D.J. uses it'], [
    ['"I\'ve never been more excited about something we\'ve created at Real Geeks, and I\'ve been doing this for almost 20 years."', 'Press release, Nov 12, 2026', 'Verbatim', 'Read it back before Q14: "So what did you have to unlearn to get here?"'],
    ['"I\'ve never been more excited about a feature we\'ve built. It\'s a game changer."', 'Real Geeks blog, Oct 6, 2026', 'Verbatim', 'Hold in reserve. Use if Q9 gets too technical: "You called it a game changer. For who, exactly?"'],
    ['Real Geeks is "the only real estate IDX software out there that you can hook up to your AI agent" to build or edit pages', 'Blog and Real Estate News, Oct 2026', 'Verbatim', 'Set up Q10. Read it back, then ask what an agent on another platform should do.'],
    ['"You should still review what your AI creates."', 'Real Geeks blog (company voice, not Kevin)', 'Verbatim (company)', 'Open Q11. Paraphrase as "your own blog says."'],
], widths=[2.4, 1.4, 0.9, 2.1])

h2('4G. Audience Relevance')
table(['Segment', 'What they get'], [
    ['Individual agents', 'A self-test tonight, one page to write first, and three prompts to start with.'],
    ['Team leaders', 'How to put content at scale on a team site without publishing junk.'],
    ['Broker-owners', 'What to ask your website vendor, and the guardrails before you let AI touch a brokerage site.'],
    ['New agents', 'A website that works before they have a single review: one neighborhood page done right.'],
], widths=[1.5, 5.3])

doc.add_page_break()

# =====================================================================
# 5. LIVE STREAM
# =====================================================================
h1('5. Live Stream Title, Descriptions and Hashtags')
h2('5A. Live Stream Title')
rich([('Live stream title: ', True), (LIVE_TITLE + ' (' + str(len(LIVE_TITLE)) + ' characters)', False)])
rich([('Backup: ', True), (LIVE_BACKUP + ' (' + str(len(LIVE_BACKUP)) + ' characters)', False)])
p('This doesn\'t have to match the published episode title. Pick that after the interview.', italic=True)

h2('5B. Platform Descriptions')
rich([('Facebook: ', True), ("Every agent wants to know how to get ChatGPT to recommend them. Real Geeks co-founder Kevin McCarthy has watched AI build about 38,000 real estate web pages since October, and he's here to tell us what works. Drop your questions in the comments!", False)])
rich([('Instagram: ', True), ("Want ChatGPT to recommend you? Real Geeks co-founder Kevin McCarthy explains how. #AISearch #RealEstateMarketing #KeepingItReal", False)])
rich([('TikTok: ', True), ("Is ChatGPT sending buyers to you or the agent down the street? #realtortips #aisearch #realestate", False)])
rich([('YouTube: ', True), ("How do real estate agents get found in ChatGPT and AI search? Real Geeks co-founder Kevin McCarthy joins D.J. Paris on the Keeping It Real Podcast to explain what AI reads on an agent's website, how to write pages that get cited, and how to update your site with AI in minutes.", False)])
rich([('LinkedIn: ', True), ("Buyers are starting their agent search in ChatGPT. Real Geeks co-founder Kevin McCarthy shares what his clients learned from about 158,000 AI-made website changes, and what agents and brokerages should do about AI search now.", False)])

h2('5C. Hashtags')
bullet('Universal: ', '#KeepingItReal #RealEstatePodcast #DJParis #RealtorLife #RealEstateAgent')
bullet('Episode: ', '#AISearch #ChatGPT #RealEstateMarketing #RealEstateWebsite #AEO #RealEstateTech #RealtorTips')
bullet('Guest tag: ', '@RealGeeks (confirm Kevin\'s personal handles pre-show; none verified)')

# =====================================================================
# 6. CHAPTERS
# =====================================================================
h1('6. YouTube Chapter Markers')
table(['Timestamp', 'Chapter'], [
    ['0:00', 'How Do Agents Get Recommended by ChatGPT?'],
    ['[post-ads]', 'Rapid Fire: Best and Worst Advice'],
    ['', 'What ChatGPT Actually Reads on Your Website'],
    ['', 'Is 1% of Traffic Worth It? The AI Search Numbers'],
    ['', 'The Biggest AI Search Myth Agents Believe'],
    ['', 'The 2-Minute Test: Are You Invisible to AI?'],
    ['', 'What 38,000 AI-Written Pages Taught Real Geeks'],
    ['', 'Why Would AI Reward Pages Anyone Can Make?'],
    ['', 'When AI Edits Go Wrong'],
    ['', 'The One Page Every Agent Should Write First'],
    ['', 'Editing Your Website by Talking to AI'],
    ['', 'What to Ask Your Website Company About AI'],
    ['', 'Guardrails: What AI Should Never Touch'],
    ['', 'Your First 3 AI Website Prompts'],
    ['', 'Does Your Website Matter if You Live on Referrals?'],
    ['', 'What a 20-Year Website Builder Changed His Mind On'],
    ['', 'What to Stop Doing on Your Website'],
    ['', 'Homework + Where to Find Kevin McCarthy'],
], widths=[1.2, 5.6])

doc.add_page_break()

# =====================================================================
# 7. STRESS TEST, COUNCIL, POLISH
# =====================================================================
h1('7. Stress Test, Council Review and EP Polish')
h2('7A. Stress Test')
table(['#', 'What broke', 'Fix applied'], [
    ['1', 'Kevin\'s title conflicts: CTO (email), CEO/CTO (press release), COO (old Inman bio).', 'Card and intro say "co-founder." Pre-show check added.'],
    ['2', 'Intro email\'s client quote isn\'t verbatim ("It\'s absolutely game changing! I am obsessed with it.").', 'Card uses the press release wording and names Scott Bergmann.'],
    ['3', 'Sponsor guest. Draft had 6 of 15 questions about the product (40%).', 'Product limited to Block 3 (Q9 and Q12 directly; Q10 and Q11 are vendor-neutral). Sponsor disclosure added to the card.'],
    ['4', 'Drift risk: technical tour of MCP vs. CLI vs. API, or a live demo.', 'Drift guard lines written on the card. Q9 forces the "never opened code" frame.'],
    ['5', 'Overlap with the Bobby Kerr AI search episode (Google Business Profile).', 'Core topic kept on the website. No GBP questions.'],
    ['6', 'Q5 dodgeable with "it depends on the agent."', 'Follow-up demands one good page and one bad page.'],
    ['7', 'Q6 could feel like an ambush of the sponsor\'s product.', 'Framed as D.J.\'s own worry that "a lot of agents share." Producer note keeps the answer on the agent, not the tool.'],
    ['8', '"Only IDX software" claim is Kevin\'s, not verified.', 'Moved to "guest supplied." Used only as a read-back in 4F.'],
    ['9', 'Runtime: 15 questions plus Rapid Fire is the ceiling for 43 minutes.', 'Cut list and never-cut list written.'],
    ['10', 'Rapid Fire Q3 likely spends Block 3.', 'Callback line on the card and a note on Q9.'],
], widths=[0.3, 3.2, 3.3])

h2('7B. Council Review')
p('Convened: Miller, Byron Lazine, Hormozi, Kane, MrBeast, Chris Do. Witnesses: Heath, Berger.', italic=True)
table(['Member', 'What they\'d change'], [
    ['Donald Miller', '"The agent is the hero, not AI Connect. Keep the product in one block. The title promises the agent\'s outcome: found in ChatGPT."'],
    ['Byron Lazine', '"The press release went out yesterday. Say the 38,000 number early. That\'s the news."'],
    ['Alex Hormozi', '"Q4 and Q12 are the gold, a test and three prompts. Make sure he says the prompts word for word."'],
    ['Brendan Kane', '"Title 1 is a search query. Title 2 is a stat hook. Run both. Don\'t ship the clever one."'],
    ['MrBeast', '"Block 4 sags if it turns philosophical. Q13 has to be a real argument, so put the skeptic in the room."'],
    ['Chris Do', '"Q14 is the only question that costs him anything. Don\'t cut it first unless you have to."'],
], widths=[1.4, 5.4])

table(['#', 'Title', 'Ingredient', 'Curiosity mechanism'], [
    ['1', 'How to Get Your Website Found in ChatGPT Search (Real Geeks Co-Founder Kevin McCarthy)', 'Insight', 'Answers a question the viewer is already asking'],
    ['2', 'AI Wrote 38,000 Agent Web Pages in a Month. Here\'s What Actually Works (Kevin McCarthy)', 'Stat', 'Huh (38,000) before the aha (what works)'],
    ['3', 'Your Website Has a New Visitor, and It\'s Not Human (Kevin McCarthy, Real Geeks)', 'Concept', 'Mystery, but needs context to land'],
], widths=[0.3, 3.4, 0.9, 2.2])
p('Recommended: #1 for YouTube search, the long-tail goal. Use #2 for the clip and the LinkedIn post.', italic=True)

rich([('Cold open (sharpened): ', True), ('Kept as written in 2B. It opens with the listener\'s question, holds back the answer, and uses the verified 38,000 number.', False)])

table(['Q#', 'Question', 'Berger emotion', 'Heath gap'], [
    ['Q4', 'What do they type tonight to find out if they\'re invisible?', 'Anxiety', 'Am I invisible? Fixed in one step.'],
    ['Q6', 'If everyone can make 50 pages, why would AI reward any of them?', 'Anger/skepticism', 'Names the doubt every agent has'],
    ['Q15', 'What should agents stop doing on their websites today?', 'Amusement', 'Stop list, everyone checks their own site'],
], widths=[0.5, 3.1, 1.3, 1.9])

table(['Platform', 'Verdict + fix'], [
    ['Facebook', 'Keep. Conversational, ends on the comment ask.'],
    ['Instagram', 'Keep. Short.'],
    ['TikTok', 'Keep. The question works as a scroll stopper.'],
    ['YouTube', 'Keep. "ChatGPT," "AI search," and the guest name all appear.'],
    ['LinkedIn', 'Keep. Business framing, uses the 158,000 number.'],
], widths=[1.2, 5.6])

rich([('Arc fix: ', True), ('Block 3 is where it\'s most likely to turn into a demo. Q10 (what to ask your own provider) sits right after Q9 to pull it back to every listener.', False)])
rich([('Why it should work: ', True), ('Heath: the cold open asks the question and holds the answer. Berger: Q4 is high-anxiety and gets shared ("check if you\'re invisible"). MrBeast: every block ends on something to do, so there\'s a payoff every 10 minutes.', False)])
rich([('The dissent: ', True), ('Kane still wants Title 2 as the primary. Test it: publish with #1, run #2 as the Shorts title, and compare views after 7 days.', False)])

h2('7C. EP Polish (pass 3)')
for line in [
    'Cut product questions from 6 to 2 direct ones, and moved them all into Block 3.',
    'Changed Kevin\'s on-air title to "co-founder" everywhere because the sources disagree.',
    'Swapped in the press release\'s verbatim client quote.',
    'Rewrote Q6 as D.J.\'s own worry so it lands as a shared problem, not a gotcha.',
    'Added the sponsor disclosure line to the card.',
    'Put the 38,000 number in the cold open and Q5 so the episode rides the Nov 12 news.',
    'Moved "the only IDX software" claim out of the verified list.',
    'Made sure every short version is under 20 words and every block ends on an action.',
]:
    bullet('', line)

doc.save("/Users/djparis/GitHub Projects/keeping-it-real-content-system/guest-prep/Kevin_McCarthy_Interview_Prep.docx")
print('saved')
