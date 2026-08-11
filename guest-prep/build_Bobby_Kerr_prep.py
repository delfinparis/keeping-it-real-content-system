#!/usr/bin/env python
# Builds the KIRP interview prep .docx for Bobby Kerr, founder of LOC8 My Business
# Built to prompts/06_interview_prep.md v4: draft -> stress test + council -> EP polish
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


def q(num, question, if_vague, reveals, serves, note=None):
    rich([(str(num) + '. ', True), (question, True)], space=2)
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
r = sub.add_run('Interview Prep: Bobby Kerr')
r.bold = True
r.font.size = Pt(24)
sub2 = doc.add_paragraph()
sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub2.add_run('Founder, LOC8 My Business  |  Google Business Profile optimization for real estate  |  Prepared August 11, 2026')
r.italic = True
r.font.size = Pt(10)

# =====================================================================
# PAGE 1 — QUICK REFERENCE CARD
# =====================================================================
h1('PAGE 1: QUICK REFERENCE CARD')
p('Glance at this during the interview. Everything else is morning-of reading.', italic=True, size=9.5)

bullet('Name: ', 'Bobby Kerr. Pronouns not publicly stated; he/him used throughout his own materials. Confirm in the green room.')
bullet('Title: ', 'Founder, LOC8 My Business, a real estate marketing agency built entirely around Google Business Profile optimization. Business address on the site: 2237 SW 4th Ct, Cape Coral, FL 33991. Phone 239.268.3852.')
bullet('Calls himself: ', '"The Google Guy" for real estate pros. Also uses "Rockstar Realtor." Certified through Google\'s marketing certification program, which he has described publicly as a 240-hour program.')
bullet('Also does: ', 'Co-host of the Always Be Cool (ABC) Podcast with Darren Copeland of Summit Lending. Performs as Bob Jovi, a 1980s Bon Jovi tribute act. Listed as COO of The Shaun Ashley Team at RE/MAX Heritage in Blue Springs, Missouri. See Landmines 2 and 3 before you say any of this on air.')
bullet('What LOC8 sells: ', 'GBP Build and Rebuild from $499 one time. Done-For-You GBP Build from $1,250 one time, which includes 25 custom services written with local keywords. Authority Membership from $297 a month, which is 32 content pieces a month, 8 posts, 8 products or offers, 8 services. Also an AI search visibility service.')
bullet('The Authority Engine: ', 'His three-step system. 1) Profile audit and build. 2) Review acceleration. 3) Local authority growth, meaning monthly optimization, citations, and AI-ready content.')
bullet('Claimed stats: ', '1,000+ agent profiles optimized across the US and Canada. 160+ markets. LOC8 itself shows 248+ five-star reviews at a 4.9 average. Read Landmine 5 before you repeat any number.')
bullet('Media he claims: ', 'FOX 4 News, The Kansas City Star, WINK News, BBB accredited. Verified outside appearance: SpeakerFlow\'s Technically Speaking, season 3 episode 42, "Google Business Is More Relevant Than You Think."')
bullet('Free stuff he gives away: ', 'A 5-Step Local Search System checklist, a free SEO training video, a complete GBP guide, and a download called "From Forgotten to Found." He also teaches live webinars and workshops weekly.')
bullet('Find him: ', 'loc8mybusiness.com | thebobbykerr.com | LinkedIn /in/thebobbykerr | Facebook, Instagram and YouTube @thebobbykerr | Facebook @loc8mybiz | info@loc8mybiz.com')
bullet('KIR connection: ', 'FIRST TIME GUEST. No prior KIR appearance found.')
bullet('Guest type: ', 'C with a D overlay. Vendor first, educator second. Product cap applies: no more than 20% of the questions can be about what he sells, and the episode has to fully pay off for an agent who never gives him a dollar. Every product answer gets a "now give me the version I do myself on a Sunday night" follow-up.')
bullet('Episode length: ', 'NOT CONFIRMED. Everything here is built to 43 minutes, four blocks. If it is 30, drop Block 3 to two questions and cut Q12 and Q4. If it is 60, Q5 and Q13 are the two that reward more room.')

rich([('THE CORE TOPIC: ', True),
      ('What an agent actually changes on their Google Business Profile this month so that Google and the AI engines hand them over as the answer, field by field, in the order he would do it.',)])

rich([('THE ONE THING THAT MAKES THIS AN EPISODE AND NOT AN AD: ', True),
      ('Everything he says will be true and almost none of it will be specific unless you make it specific. "Optimize your profile" is not an answer. "Fill out your services" is not an answer. The answer is the words he would type into the box. Every single time he gives you a category, ask for the sentence. If you leave with a checklist and no example copy, the episode failed.', False, False)])

rich([('WATCH OUT FOR (this one will bite you in minute two): ', True),
      ('He already sent his best advice and his worst advice in the intake, and both of them are load-bearing for this episode. The standardized Rapid Fire will spend them in the first two minutes and you do not follow up on Rapid Fire. So after each of those two answers, say "Love it, and we are coming back to that." Then come back to them on purpose: the worst-advice callback is Q9 and the best-advice callback is Q10. They are written out. Do not improvise the callbacks.', False, False)])

rich([('THE "I\'VE INTERVIEWED HUNDREDS" MOMENT (use once, Q15): ', True),
      ('"I have interviewed hundreds of agents on this show, and when Google comes up the answer is almost always the same. I claimed it years ago, it is fine, and anyway my business comes from referrals. That agent is listening right now and he is not wrong about his referrals. Talk to him directly."', False, False)])

rich([('LIVE STREAM TITLE (paste into Restream before you hit record): ', True),
      ('Bobby Kerr: How Agents Get Picked by Google and AI Search in 2026', False, True)])
p('65 characters. Backup: "Your Google Profile Is Your Front Door: Bobby Kerr on Winning AI Search" (71 characters). This does not have to match the published episode title. Pick that one after you hear the interview. See Section 5A.', italic=True, size=9.5)

rich([('OVERASKED, DO NOT ASK: ', True)])
bullet('', '"What is a Google Business Profile and why does it matter?" This is the opening question on every show he has been on. Your audience already knows what it is. Start at what is broken on theirs.')
bullet('', '"How do I get more reviews?" His published answer already exists: QR codes at events, and a nine-touch drip across email, text, and voicemail. Q13 and Q14 go at reviews from the angle nobody asks about, which is what the review has to say.')
bullet('', '"What is the biggest mistake agents make?" His answer is "an incomplete profile," which is a category, not a mistake. Q5 gets the same territory with a list you can actually use.')

doc.add_page_break()

h2('LANDMINES (read all seven before you record)')

rich([('1. THERE ARE TWO BOBBY KERRS AND THE OTHER ONE IS MORE FAMOUS. ', True),
      ('Search his name and the top results are frequently Bobby Kerr the Irish entrepreneur, the Insomnia Coffee founder, a Dragons\' Den investor, and the host of Down To Business on Newstalk. That is a completely different person. If any part of your intro came out of a search summary or an AI assist, check it. Do not say Dragons\' Den, do not say Insomnia Coffee, and do not say anything about Ireland.', False, False)])

rich([('2. HIS RESUME HAS TWO PUBLISHED VERSIONS AND THEY DO NOT MATCH. ', True),
      ('The bio he sent you says he started, scaled, and sold multiple real estate businesses: home inspections, mortgage, property and casualty insurance, and real estate sales. The bio he gave SpeakerFlow says his career runs casino gaming sales, middle school teaching, then real estate. His own personal site lists a home inspection company and an investment company, and describes him as co-leader of The Shaun Ashley Team at RE/MAX Heritage; a BBB listing for that team names him as COO. The mortgage brokerage and the insurance agency are in his intake and nowhere public that I could find.', False, False)])
rich([('   WHAT YOU DO: ', True),
      ('Do not read the list as verified and do not say "sold." Do not attach a year to anything. Q1 is deliberately built on a client result rather than his origin story so you never have to. If you want the resume on tape, let him say it: "Before LOC8 you ran a stack of businesses in this industry. Name them for me." Then take what he says at face value and move.', False, False)])

rich([('3. TWO HOME BASES. ', True),
      ('LOC8 lists a Cape Coral, Florida address. His real estate team, his tribute act, and his Kansas City Star mention are all Kansas City, and his old Twitter handle is KC_Bob. Both can be true and it is not the story. Do not geolocate him in the intro. If it comes up, ask "where are you sitting right now" and let him answer it.', False, False)])

rich([('4. GOOGLE KILLED THE Q&A SECTION AND HE STILL TEACHES IT. ', True),
      ('His topic pitch lists Q&A as one of the fields to fill on a complete profile. Google discontinued the Q&A API on November 3, 2025, began phasing the public Q&A section out on December 3, 2025, and new profiles are now created without it. The replacement is the Gemini-powered "Ask about this place" answer box, which generates answers in real time from the profile, the reviews, the photos, and the website. This is the single most interesting question in the episode and also the easiest one to blow. Q7 is written to land it as two practitioners comparing notes, not as a correction. If he says Q&A is still on profiles, do not argue and do not fact-check him on air. Your line is "on some it still is, on new ones it is gone, so what fills that job now," and you move. The listener hears the update either way and he keeps his dignity.', False, False)])

rich([('5. THE NUMBERS DO NOT AGREE WITH EACH OTHER. ', True),
      ('He has publicly used "1065% more likely to get calls and clicks" for profiles with 100+ photos, and his site uses "10x more client calls," "3 to 5x more profile views," and a client who got $1.2M in listings in two weeks. None of those have a traceable primary source. Separately, his SpeakerFlow bio says 1,200+ five-star reviews across his own Kansas City businesses while LOC8\'s site says 248+ reviews at 4.9. Those are two different things and stacking them sounds like a contradiction. RULE: let him say his numbers, do not repeat them back, do not put them in the intro, and never say two of them in the same sentence. The only number you say out loud is the 83% no-click figure in Q3, and that one is published research, not his.', False, False)])

rich([('6. SPONSOR EXPOSURE. ', True),
      ('His whole thesis is that the free Google page beats the paid website, and that agents who outsource content to third-party posting companies get buried. Real Geeks sells agent websites and lead generation. Courted sells agent data. Let him make his case in full, but do not co-sign it, do not add your own shot at the category, and do not let a clip go out that reads as the show saying websites are dead. The frame that keeps everybody whole is written into Q2: the profile is the front door, the website is the house, and most agents built the house and boarded up the door. Q2 also forces him to name what the website still does that the profile cannot, which is the sentence that makes the clip safe.', False, False)])

rich([('7. SOMEONE DIED IN ONE OF HIS STORIES. ', True),
      ('His intake includes a closing where the seller passed away at the table, with a loan officer named Alan in the room. A real person died in front of a room full of professionals who are all still working. HARD RULES: this is not a question in the run of show and you do not go fishing for it. If he brings it up, let him tell it, do not ask what happened to the estate, do not ask for the city, the year, the brokerage, or the title company, and do not laugh into it. Land it with one flat sentence and move: "That will stay with everybody who was in that room." If he starts identifying anyone, your line is "let us keep everybody anonymous on this one." Never cut it as a standalone clip with a caption.', False, False)])

rich([('TONE READ, DO THIS IN THE FIRST THREE MINUTES: ', True),
      ('He is a performer. He fronts a Bon Jovi tribute band, he hosts his own show, and his materials run hot on energy. That means two risks. One, he will answer in slogans, because slogans are what he does on stage and on webinars every week. Two, he will be very comfortable talking, so a soft question will cost you four minutes. The counter for both is the same and it is the only interviewing note that matters on this guest: after every answer, ask for the words. Not the principle, the words. "Say the actual line." "Type it out loud for me." If you do that six times in this episode, it is a great episode. If you do it zero times, it is a webinar.', False, False)])

doc.add_page_break()

# =====================================================================
# PAGE 2 — EPISODE FRAMEWORK
# =====================================================================
h1('PAGE 2: EPISODE FRAMEWORK')

h2('2A. Title Options')
table(['#', 'Title', 'Ships To', 'Why It Works'],
      [['1', 'Ranking Is Over. Bobby Kerr on Getting Handed to the Buyer as the Answer.',
        'Podcast feed, social cuts',
        'Kills a belief in four words, then names the replacement. No number to defend, no jargon to decode, and it works on an agent who has never heard of him.'],
       ['2', '83% of Google Searches Now End Without a Click. Bobby Kerr on How Agents Get Picked Anyway.',
        'YouTube',
        'The stat does the search and authority work, and "anyway" holds the curiosity open. The number is published research, not a guest claim, so it survives scrutiny.'],
       ['3', 'The Free Google Page You Claimed and Forgot Is Now Your Front Door (Bobby Kerr)',
        'Hold for a clip caption',
        'Best emotional hit of the three because it accuses the listener gently, but "front door" is his metaphor and it needs the episode around it to mean anything.']],
      widths=[0.3, 2.9, 1.1, 2.6])

h2('2B. Cold Open Hook')
p('Read before the ads.', italic=True, size=9.5)
rich([('"My guest today says the most valuable piece of real estate you own is not a listing, it is a free page on Google you probably have not opened since the day you claimed it. He has rebuilt more than a thousand of them for agents, and he says the ones winning right now are not ranking higher, they are getting handed to the buyer as the answer. We are going to talk about that today. Stay tuned."', False, True)])

h2('2C. Episode Arc')
rich([('Core topic: ', True), ('What an agent actually changes on their Google Business Profile this month so that Google and the AI engines hand them over as the answer.',)])
rich([('Why this topic and not the others: ', True),
      ('He could carry a whole episode on AI search theory, and it would be the fourth one your audience heard this quarter. He is the only guest you will book who has personally rebuilt a thousand of these profiles, so the thing only he can give you is the field-by-field build. Theory is free everywhere. The words he types in the box are not.',)])
rich([('The four angles: ', True),
      ('Block 1 is why this surface and not the website. Block 2 is what complete actually means, field by field, including what to do now that Q&A is gone and how not to get suspended. Block 3 is why generic content buries you and what hyperlocal looks like at the sentence level. Block 4 is reviews, specifically why the text beats the star count once an AI engine is doing the reading.',)])

doc.add_page_break()

# =====================================================================
# SECTION 3 — INTERVIEW QUESTIONS
# =====================================================================
h1('SECTION 3: INTERVIEW QUESTIONS')

h2('Structure (43 minute target)')
table(['Segment', 'Time', 'Purpose'],
      [['Rapid Fire', '0:00 to 2:00 post-intro', '4 standardized questions, no follow-ups. Read the Watch Out For note first.'],
       ['Block 1: The Front Door', '2:00 to 12:00', 'Why this surface, and why "I claimed it years ago" is the whole problem.'],
       ['Block 2: What Complete Actually Means', '12:00 to 22:00', 'The build, field by field. The Q&A change. The suspension rules.'],
       ['Block 3: Commodity vs Non-Commodity', '22:00 to 32:00', 'Why syndicated content buries a profile and what hyperlocal looks like in a sentence.'],
       ['Block 4: Reviews and Being the Answer', '32:00 to 40:00', 'Review text over star count, and the exact ask.'],
       ['The Close', '40:00 to 43:00', 'Homework, his resource, where to find him.']],
      widths=[1.9, 1.6, 3.4])

h3('RAPID FIRE (standardized, read as written, no follow-ups)')
p('1. Best real estate advice you have ever received?', bold=True, space=2)
p('2. Worst real estate advice you have ever received?', bold=True, space=2)
p('3. One tool or app you cannot run your business without?', bold=True, space=2)
p('4. What would surprise people most about your day to day?', bold=True, space=2)
rich([('PRODUCER NOTE: ', True),
      ('He pre-sent 1 and 2 and they are both central to this episode. After each, say "Love it, and we are coming back to that," then move. Do not follow up here. The callbacks are Q9 and Q10 and they are written out. For reference so you recognize them coming: his best advice is a recruiting coach telling him to stop advertising that he owned three companies, and his worst advice is "you have to be everywhere."', False, True)])

doc.add_page_break()

h2('BLOCK 1: THE FRONT DOOR (2:00 to 12:00)')
p('Audience note: every segment, but aimed at the solo producing agent who has a website they paid for and a Google profile they have not opened in two years.', italic=True, size=9.5)
p('Arc: the client result, the hierarchy, what changed in search, the first field.', italic=True, size=9.5)

q(1,
  "You have a client in Annapolis who says she picked up a brand new listing the first week after you rebuilt her profile, and a second one the week after that. I want the boring version of that story, not the highlight. What was actually on that profile before you touched it, and what was on it after?",
  "Name three fields that were empty on Monday and full on Friday.",
  "Whether the result came from a mechanism or from luck, and it hands the listener a before and after picture in the first two minutes.",
  "Individual agents, new agents.")

q(2,
  "Most of the agents listening spent real money on a website and almost nothing on the free page Google handed them. You are telling them they built the house and boarded up the front door. Make that case, and then be specific about what the website still does that the profile cannot.",
  "If an agent has 500 dollars and one weekend, which one gets it, and why?",
  "A defensible hierarchy instead of a pitch, and a sentence that keeps the clip from reading as the show saying websites are dead.",
  "All segments.",
  "This is your sponsor protection. Do not let him skip the second half of the question. If he does not name something the website still does, ask it again as its own question.")

q(3,
  "Here is the number that made me want to have this conversation. When Google puts an AI overview at the top of the page, the research says something like 83 percent of those searches end without a click to anybody's site, and inside AI Mode it is higher than that. If nobody is clicking through, where does an agent actually get chosen now, and what does that change about what you put on the profile?",
  "Walk me through it screen by screen. Buyer opens their phone, types the thing, and then what happens until my phone rings?",
  "The mechanism behind being the answer instead of ranking, which is the promise in the title.",
  "All segments.")

q(4,
  "Somebody is listening to this on a treadmill right now and has not opened their profile in two years. When they get home tonight, what is the one field they open, and what do they type into it?",
  "Give me the field name and then say the example sentence out loud.",
  "The first domino, and the first time in the episode he gives you actual copy instead of a category.",
  "Individual agents, new agents.")

bridge("So the profile is the front door and most agents have it boarded up. Let's open it. I want to go field by field through what a finished one actually looks like, because I think most people hear complete and picture the hours being right.")

doc.add_page_break()

h2('BLOCK 2: WHAT COMPLETE ACTUALLY MEANS (12:00 to 22:00)')
p('Audience note: this is the value-density block. It is the one an agent screenshots and the one a team lead sends to twelve people.', italic=True, size=9.5)
p('Arc: the list in order, the field everyone fakes, the thing that changed, the thing that gets you suspended.', italic=True, size=9.5)

q(5,
  "Define complete for me the way Google defines it, not the way an agent defines it. If you sat down at my computer with my profile open, what is the list you work down, in order?",
  "Rank the top five by impact, and tell me which one is blank most often.",
  "The actual checklist. This is the single most stealable answer in the episode and everything after it is a variation on it.",
  "All segments.",
  "NEVER CUT. If he gives you eleven items in thirty seconds, stop him and say give me the top three again slower.")

q(6,
  "Services is the field I hear you talk about more than any other, and you write twenty-five of them for a client instead of the four an agent would write. Give me a real one. For an agent who works Logan Square here in Chicago, what does a services entry look like, word for word?",
  "Say the actual line. Not the category, the line.",
  "The difference between commodity and non-commodity at the field level, in language a listener can copy tonight.",
  "Individual agents.",
  "He sells a 25-services build. That is fine, let him reference it once. Then ask: how many can an agent write themselves in an hour, and where do they get the neighborhood words from?")

q(7,
  "Here is where I want your honest read, because this stuff moves under all of us. Google pulled the public Q and A section off profiles starting at the end of last year and pushed everybody toward the AI answer box on the listing instead. Q and A has been part of the build you teach. What survived that change, what did not, and how do you feed that AI box now that you cannot seed the questions yourself?",
  "If a brand new profile does not have Q and A at all, what field takes over that job? Name it.",
  "Whether his system is current or a checklist from three years ago. This is the credibility moment of the episode, and if he answers it well it is also the most forwardable minute in it.",
  "All segments.",
  "NOT A GOTCHA, and it will read as one if you deliver it flat. Ask it leaning in, as two people comparing notes. If he says Q and A is still there, do not argue and do not correct him on air. Say: on some profiles it still is, on new ones it is gone, so what do you do there. Then move.")

q(8,
  "Last thing on the build, and it is the one that actually scares people. Agents get suspended. The name rules, the brokerage address you do not personally sit at, the service area setup. What is the safe configuration for a solo agent at a big brokerage, and what is the thing that gets people taken down that they never see coming?",
  "Give me the exact business name format for an agent named Maria Lopez at a 500 agent brokerage. Type it out loud.",
  "The compliance layer almost nobody teaches, and the reason a broker owner keeps listening.",
  "Individual agents, new agents, broker owners.")

bridge("Okay, so it's built and it's not going to get pulled down. Now it's empty, and it stays empty unless somebody feeds it. That's the part I want to spend the most time on, because I think this is where most agents outsource themselves into invisibility.")

doc.add_page_break()

h2('BLOCK 3: COMMODITY VS NON-COMMODITY (22:00 to 32:00)')
p('Audience note: this block carries both Rapid Fire callbacks. It is also the most contestable claim in the episode, so it needs the most evidence.', italic=True, size=9.5)
p('Arc: the callback, the proof, the specialty problem, the calendar, the broker version.', italic=True, size=9.5)

q(9,
  "I want to come back to your worst advice, because we did not finish it. You said the be-everywhere advice pushes agents into hiring a company to post for them, and those companies run the same content across thousands of profiles. I want to know if Google can actually tell. Not in theory. What have you watched happen to a profile running syndicated content next to one that is not?",
  "Two agents, same market, one on a content service and one writing their own. What do the profile views look like at ninety days?",
  "Whether Google knows is an observation or a belief. This is his biggest claim and the one an SEO person in the audience will push back on, so make him show his work.",
  "All segments.",
  "If he cannot produce a before and after, do not rescue him. Say: so it is a judgment call more than a measured thing. Let the answer be what it is. That honesty is the clip, and it costs you nothing.")

q(10,
  "Earlier you told me a recruiting coach made you stop advertising that you owned three companies, and that you fought him on it and he was right. Same principle down here. What does pick one thing look like on a Google profile for an agent who genuinely does buyers, sellers, rentals, and investors, and who cannot afford to turn any of it away?",
  "Does the specialty live in the services, the posts, or the reviews? Pick one and tell me why the other two are wrong.",
  "How to be specific without amputating the business, which is the objection every agent has to niching and the reason most of them never do it.",
  "Individual agents, team leaders.")

q(11,
  "Give me the calendar. How often does something new have to hit that profile before Google treats it as alive, what are the formats, and how long does it actually take an agent to do it themselves on a Sunday night?",
  "Posts per month, photos per month, videos per month. Give me the numbers.",
  "The recency mechanism, plus an honest read on whether do-it-yourself is realistic or whether this is a thing you hire out.",
  "All segments.",
  "This is where the membership pitch wants to come out. Product cap. Let him name it once, then say: now give me the version I do myself with no budget.")

q(12,
  "Flip this for a second. I recruit agents for a living, so I am listening to this as a broker. If I have 800 agents and most of their profiles are blank or wrong, is that my problem or theirs? And is there a brokerage-level version of this that does not step on the agents' own profiles?",
  "Should the brokerage profile and the agent profile say the same thing or deliberately different things?",
  "The team and brokerage architecture, which nobody covers and which is the reason a broker owner shares the episode.",
  "Broker owners, team leaders.")

bridge("So it's built, it's fed, and it's specific. The last piece is the one agents think they already understand, and I don't think they do. Let's talk about reviews, because you're telling me the number I've been chasing for years is the wrong number.")

doc.add_page_break()

h2('BLOCK 4: REVIEWS AND BEING THE ANSWER (32:00 to 40:00)')
p('Audience note: the most immediately actionable block in the episode, and the one with the highest chance of producing a screenshot.', italic=True, size=9.5)
p('Arc: the wrong metric, the exact ask, the objection, the honest timeline.', italic=True, size=9.5)

q(13,
  "You have said the text inside a review matters more than the star count. Every agent I know is chasing five stars and counting them. What is an AI engine actually doing with the words in a review, and what does a review have to say to be worth more than one more five-star Bobby was great?",
  "Write me the review you would want, out loud, for an agent who sells two-bedroom condos in one neighborhood.",
  "The most stealable tactic in the episode, and the one that reframes a metric the whole audience already tracks.",
  "All segments.",
  "NEVER CUT.")

q(14,
  "Then the hard part is asking. Most agents send please leave me a review and get great to work with. What do you say to a client, word for word, that gets them to name the neighborhood, the property type, and the problem you solved, without it feeling like you wrote it for them?",
  "Give me the text message. The actual text message, the way it would show up on their phone.",
  "A script listeners will screenshot before the episode ends.",
  "Individual agents, new agents.",
  "NEVER CUT. If he gives you a philosophy, ask again. You want a message with a send button on it.")

q(15,
  "I have interviewed hundreds of agents on this show, and when Google comes up the answer is almost always the same. I claimed it years ago, it is fine, and anyway my business comes from referrals. That agent is listening right now and he is not wrong about his referrals. Talk to him directly. Why does he care about this?",
  "He does thirty deals a year off his sphere. What does the profile do for him that his sphere does not already do?",
  "Whether this is universal or a fix for agents without a network. It names the biggest objection in the room instead of dodging it, and the answer decides whether the episode converts.",
  "All segments.",
  "NEVER CUT. This is your one hundreds moment. Do not use the phrase anywhere else.")

q(16,
  "Last one. Somebody does everything you just said. Realistically, when do they see the first thing they can point at and say that came from this, and what does that first thing usually look like?",
  "Weeks or months? And is the first signal a call, a message, or a direction request?",
  "An honest timeline, which protects him from the too-good-to-be-true read and protects your audience from quitting at week three.",
  "All segments.")

h3('THE HUMAN LANDING (optional, right before the close)')
q('17a',
  "One thing I have to ask you about before I let you go. You front a Bon Jovi tribute band. You go by Bob Jovi. Everything you just told me about being specific and not looking like everybody else is not a marketing theory for you, it is how you have run your own name for years. What did standing on a stage teach you about being memorable that no marketing book ever did?",
  "What is the moment you knew the name was working?",
  "The vulnerable beat that earns the follow, and the one moment in the episode that is about him instead of about a field on a form.",
  "All segments.",
  "ALTERNATE if the energy is low or you are tight: his home inspection story. Empty house, top closet shelf, a bank envelope with a few thousand dollars in it that only a tall guy would ever have seen, handed straight to the buyer's agent. The button is that the listing agent owned a home inspection company himself and had walked that house. Ask it as: what is the strangest thing you ever found in an empty house?")

h2('THE CLOSE')
rich([('HOMEWORK (read verbatim): ', True),
      ('"Here is what I want you to do before the next episode. Open your Google Business Profile, go to the services section, and write out every service you actually offer, named the way a client would say it, with your neighborhoods inside the words. If you have fewer than ten, you have got homework. Not next month. This week."', False, True)])
p('Why this one: it is free, it takes under thirty minutes, done is countable, and it is the exact field Q6 gave them the example copy for. If Q6 produces a better field, swap it, but keep the counting. The counting is what makes it done.', italic=True, size=9.5)

rich([('GUEST CLOSE: ', True), ('"Where can people find you, and what do you want them to do first?" He has several free giveaways: the 5-Step Local Search System checklist, a free training video, a full GBP guide, and the From Forgotten to Found download. Ask him to name ONE. Four offers is the same as none, and it is also the exact mistake this episode is about.',)])

h3('If you are running long, cut these first')
bullet('1. Q12, the broker flip. ', 'It is the furthest from your largest audience segment, and Block 3 still ends on an implementation question without it.')
bullet('2. Q17a, the human landing. ', 'Warmest thing in the episode, but the close survives without it and the homework does not.')
bullet('3. Q4. ', 'If Q2 already produced the first field, this is the same answer twice. The homework covers it anyway.')
bullet('4. Q3. ', 'Only if the AI framing already came out inside Q2. If it did not, keep it, because the title is built on it.')

h3('Never cut')
bullet('Q5. ', 'The list in order. Without it there is no episode, only opinions.')
bullet('Q7. ', 'The Q and A change. This is the only minute of this episode that could not have been recorded two years ago.')
bullet('Q13. ', 'Review text over star count. The reframe.')
bullet('Q14. ', 'The exact ask. The screenshot.')
bullet('Q15. ', 'The objection said out loud. This is the one that decides whether anybody acts.')

doc.add_page_break()

# =====================================================================
# SECTION 4 — RESEARCH BRIEF
# =====================================================================
h1('SECTION 4: RESEARCH BRIEF')
p('Morning-of reading. Not for during the interview.', italic=True, size=9.5)

h2('4A. Background')
p('Kerr is the founder of LOC8 My Business, a marketing agency built entirely around Google Business Profile optimization for real estate professionals, run from a Cape Coral, Florida address. His own materials are consistent on one thing and inconsistent on almost everything else: he has run a stack of small businesses before this, he collected an unusual number of Google reviews doing it, he went and got Google certified, and he turned that into a service business for agents. The parts that do not line up across sources are which businesses, in what order, and whether he still owns any of them. See Landmine 2. He is also a working performer, which is relevant rather than trivia: the tribute act and the podcast are the proof case for the thing he teaches, which is that being specific and unmistakable beats being everywhere.')

h2('4B. Career Timeline (verified entries only)')
table(['When', 'Role / Company', 'Source and note'],
      [['Undated', 'Founder, home inspection company', 'His own site. Intake says he later sold it. No public record of the sale.'],
       ['Undated', 'Founder, investment company', 'His own site.'],
       ['Current or recent', 'COO and co-leader, The Shaun Ashley Team, RE/MAX Heritage, Blue Springs MO', 'BBB listing plus his own site. Conflicts with the intake line that he sold his sales business. Do not say either version.'],
       ['Undated', 'Google marketing certification, described by him as a 240-hour program', 'Guest-supplied via SpeakerFlow.'],
       ['Ongoing', 'Co-host, Always Be Cool (ABC) Podcast, with Darren Copeland of Summit Lending', 'Apple, Spotify, Amazon, YouTube. 100+ episodes. Start year not verified, so do not say one.'],
       ['Ongoing', 'Founder, LOC8 My Business, Cape Coral FL', 'Company site. Founding year not published.'],
       ['Ongoing', 'Performs as Bob Jovi, 1980s Bon Jovi tribute act', 'His own site.']],
      widths=[1.2, 2.6, 3.1])
p('Mortgage brokerage and property and casualty insurance agency: intake only. Both are load-bearing in his best-advice story. Let him tell it. Do not introduce them as fact.', italic=True, size=9.5)

h2('4C. What Makes Him Interesting to This Audience')
bullet('He has done the reps, not just the research. ', '1,000+ agent profiles rebuilt across 160+ markets in the US and Canada. That means he can answer at the field level instead of the strategy level, which is exactly the altitude your audience wants and almost never gets from a marketing guest.')
bullet('He is on the right side of a real change. ', 'Whitespark\'s 2026 local search survey puts Google Business Profile signals at roughly a third of local pack ranking, more than reviews, on-page SEO, and backlinks combined, and it added AI search visibility as its own ranking category this year. This is not a trend piece, it is a scoreboard change.')
bullet('The surface is free and almost nobody has finished it. ', 'Every other marketing episode you run ends with "and it costs this much." This one ends with a field an agent fills in tonight for nothing. That is rare and it makes the homework land.')
bullet('He ran the businesses his clients run. ', 'Inspections, lending, insurance, sales. Whatever the exact list turns out to be, he is not a marketer who discovered real estate. He talks like somebody who has been on a closing.')
bullet('He is the proof of his own thesis. ', 'A guy who calls himself the Google Guy and performs as Bob Jovi is not going to get confused with any other vendor. Q17a turns that into the human beat of the episode instead of a fun fact.')

h2('4D. Key Data Points')
table(['Stat', 'Source', 'Confidence'],
      [['1,000+ agent profiles optimized, 160+ markets, US and Canada', 'LOC8 site, matches his intake', 'Medium, self-reported but consistent'],
       ['248+ five-star reviews, 4.9 average on LOC8', 'LOC8 site', 'Medium, checkable live'],
       ['1,200+ five-star reviews across his own Kansas City businesses', 'SpeakerFlow bio', 'Medium, and a different claim than the one above'],
       ['Pricing: $499 build, $1,250 done-for-you, $297 a month membership', 'LOC8 site', 'High'],
       ['10x more client calls, 3 to 5x more profile views', 'LOC8 site', 'Unverified marketing claim. Do not repeat.'],
       ['$1.2M in listings within two weeks for one client', 'LOC8 site', 'Unverified. The Annapolis two-listings version in Q1 is the safer telling.'],
       ['1065% more likely to get calls and clicks with 100+ photos', 'Said by him on SpeakerFlow', 'Unverified, widely circulated with no primary source. Do not echo it.'],
       ['83% of searches with an AI overview end with no click, 93% in AI Mode', 'Published 2026 research reported in real estate trade coverage', 'Medium to high. This is the one number you say on air.'],
       ['GBP signals are roughly 32% of local pack ranking', 'Whitespark 2026 Local Search Ranking Factors', 'High'],
       ['Public Q and A discontinued: API Nov 3 2025, public section phasing out from Dec 3 2025', 'Google support documentation and industry coverage', 'High. This is the basis for Q7.'],
       ['Gemini grounds local answers in Google Maps data across 250M+ verified places', 'Google, 2026', 'High'],
       ['ChatGPT local answers lean on Bing Places, Yelp, and Foursquare more than on GBP directly', 'Multiple local search analyses, 2026', 'Medium. Useful if he overclaims about ChatGPT reading his GBP. Do not correct him, just ask which engines read what.']],
      widths=[2.9, 2.4, 1.6])

h2('4E. Previous Media Appearances')
bullet('SpeakerFlow, Technically Speaking, season 3 episode 42, "Google Business Is More Relevant Than You Think." ', 'His fullest published interview. Covered: Google Business as a social platform rather than a review box, photos and video, posts, offers, events, Q and A, QR codes at live events, and a nine-touch review drip across email, text, and voicemail. Note that this appearance predates the Q and A removal, which is why Q7 exists.')
bullet('Always Be Cool (ABC) Podcast, his own show with Darren Copeland. ', '100+ episodes, Kansas City business, sports, and real estate guests, including a former Royals player. Tagline is Always Be Cool equals live by the golden rule. Worth one sentence of acknowledgment, not a segment.')
bullet('Claimed but not independently verified: FOX 4 News, The Kansas City Star, WINK News. ', 'All three appear on his site with no links. Do not read them in the intro as verified. "He has been featured in local press in Kansas City and Florida" is safe if you want the line at all.')
bullet('Weekly live webinars and workshops on Google-first visibility. ', 'Guest-supplied. This is why he will answer in trained slogans. See the tone read.')

h2('4F. Audience Relevance')
table(['Segment', 'What they get from this episode'],
      [['Individual agents', 'A free surface they already own, a field-by-field build, example copy they can type tonight, and a review ask with a send button.'],
       ['Team leaders', 'How to make a team specific without amputating the business, and how team and individual profiles should differ.'],
       ['Broker-owners', 'Whether 800 blank agent profiles are the brokerage\'s problem, and the suspension rules that keep agents from getting taken down at scale.'],
       ['New agents', 'The cheapest visibility available to somebody with no database, plus the name and address rules before they set the profile up wrong.']],
      widths=[1.5, 5.4])

doc.add_page_break()

# =====================================================================
# SECTION 5 — LIVE STREAM TITLE, DESCRIPTIONS & HASHTAGS
# =====================================================================
h1('SECTION 5: LIVE STREAM TITLE, DESCRIPTIONS & HASHTAGS')

h2('5A. Live Stream Title')
rich([('Live stream title: ', True), ('Bobby Kerr: How Agents Get Picked by Google and AI Search in 2026', False, True), (' (65 characters)',)])
rich([('Backup: ', True), ('Your Google Profile Is Your Front Door: Bobby Kerr on Winning AI Search', False, True), (' (71 characters)',)])
p('Both work cold, both use only verified research, and neither carries a number he would have to defend. This does not have to match the published episode title. Pick that one from Section 2A after you hear the interview.', italic=True, size=9.5)

h3('Facebook Live')
p('Bobby Kerr has rebuilt Google Business Profiles for more than a thousand real estate agents, and he says the ones winning right now are not the ones ranking higher. They are the ones Google and the AI engines hand over as the answer. We are going through the profile field by field, live. Drop your questions in the comments!')

h3('Instagram Live')
p('The free Google page you claimed and forgot is now your front door. Bobby Kerr on how agents get picked. #KeepingItReal #RealEstateAgent #GoogleBusinessProfile')

h3('TikTok Live')
p('Your Google profile is doing more for your business than your website, and you have not opened it in two years. #realtor #realestateagent #localseo')

h3('YouTube Live')
p('Bobby Kerr, founder of LOC8 My Business, has optimized Google Business Profiles for more than 1,000 real estate agents across the US and Canada. On this episode of the Keeping It Real Podcast, he walks D.J. Paris through what a complete profile actually looks like field by field, why the text inside a review beats the star count, what changed when Google removed the Q and A section, and how agents get cited by AI search engines. Google Business Profile optimization, local SEO, and AI search visibility for realtors.')

h3('LinkedIn Live')
p('Search is changing faster than most agents have changed their marketing. Bobby Kerr, founder of LOC8 My Business, joins D.J. Paris to break down how a Google Business Profile now feeds both the local map pack and AI answer engines. We also get into the brokerage question: what a broker does about hundreds of agent profiles that are blank, wrong, or one policy violation away from suspension.')

h3('Hashtag Sets')
bullet('Universal: ', '#KeepingItReal #RealEstatePodcast #DJParis #RealtorLife #RealEstateAgent')
bullet('Episode-specific: ', '#GoogleBusinessProfile #LocalSEO #AISearch #RealEstateMarketing #MapPack #GBP #AnswerEngineOptimization')
bullet('Guest tags: ', '@thebobbykerr on Facebook, Instagram and YouTube. LinkedIn /in/thebobbykerr. Company page @loc8mybiz on Facebook. Sites: loc8mybusiness.com and thebobbykerr.com. He also has an X account, which we do not post to.')

doc.add_page_break()

# =====================================================================
# SECTION 6 — YOUTUBE CHAPTER MARKERS
# =====================================================================
h1('SECTION 6: YOUTUBE CHAPTER MARKERS')
p('Estimates. Adjust after recording. Each title is written to be searchable on its own.', italic=True, size=9.5)
table(['Timestamp', 'Chapter Title'],
      [['0:00', 'Ranking Is Not the Game Anymore. Being the Answer Is.'],
       ['2:00', 'Rapid Fire: Best and Worst Advice Bobby Kerr Ever Got'],
       ['4:00', 'The Agent Who Got Two Listings Two Weeks After Fixing Her Google Profile'],
       ['7:00', 'Google Business Profile vs Your Website: Where the 500 Dollars Should Go'],
       ['9:30', '83% of AI Searches End With No Click. So Where Do Agents Get Chosen?'],
       ['11:30', 'The One Field to Open Tonight'],
       ['12:00', 'What a Complete Google Business Profile Actually Looks Like, In Order'],
       ['15:30', 'How to Write Services for Your Neighborhood, Word for Word'],
       ['18:00', 'Google Removed the Q and A Section. What Feeds the AI Answer Box Now?'],
       ['20:00', 'How Real Estate Agents Get Their Google Profile Suspended'],
       ['22:00', 'Can Google Tell When Your Content Was Copied to a Thousand Other Agents?'],
       ['25:30', 'How to Pick One Specialty Without Turning Away Business'],
       ['28:00', 'The Posting Calendar: How Often a Profile Has to Be Fed'],
       ['30:30', '800 Agents, 800 Blank Profiles. Whose Problem Is That?'],
       ['32:00', 'Why the Words in a Review Beat the Star Count'],
       ['35:00', 'The Exact Text Message That Gets a Client to Write a Useful Review'],
       ['37:30', 'For the Agent Who Says My Business Comes From Referrals Anyway'],
       ['39:00', 'How Long Before Any of This Actually Shows Up'],
       ['40:00', 'Bob Jovi: What a Tribute Band Taught Him About Being Memorable'],
       ['41:30', 'Homework and Where to Find Bobby Kerr']],
      widths=[1.1, 5.8])

doc.add_page_break()

# =====================================================================
# SECTION 7 — STRESS TEST, COUNCIL, EP POLISH
# =====================================================================
h1('SECTION 7: STRESS TEST, COUNCIL REVIEW & EP POLISH')

h2('7A. Stress Test')
table(['#', 'What broke', 'Fix applied'],
      [['1', 'His resume has two published versions and the intake adds a third. The first draft opened on his origin story, which meant D.J. would have had to assert a career path nobody can verify.',
        'Q1 was rebuilt on a client result instead of his background, and the intro carries no business list. Landmine 2 gives the one safe way to get the resume on tape, which is to let him say it.'],
       ['2', 'Name collision. The most-searched Bobby Kerr is an Irish entrepreneur and broadcaster. Any AI-assisted intro will contaminate.',
        'Landmine 1 added, with the three phrases never to say.'],
       ['3', 'Unverifiable stats everywhere. 1065%, 10x calls, 3 to 5x views, $1.2M in two weeks, and two different review counts that read as a contradiction.',
        'Landmine 5 sets the rule: let him say them, never repeat them, never stack two. 4D marks each one. No guest-supplied number appears in the cold open, the titles, or the live descriptions. The only number D.J. says is the 83% figure, which is published research.'],
       ['4', 'Rapid Fire spends both of the questions this episode is built on, and D.J. does not follow up on Rapid Fire.',
        'Watch Out For note on page 1 with the exact holding line, plus two written callbacks at Q9 and Q10 so the recovery is not improvised.'],
       ['5', 'Drift risk: this becomes a product demo. He sells a build, a done-for-you, and a monthly membership, and every question in Block 2 has a price tag attached to the honest answer.',
        'Product cap stated on page 1, plus producer notes on Q6 and Q11 that force the do-it-yourself version after he names the product once.'],
       ['6', 'Q9 as drafted was dodgeable. Google can tell the difference between original and copied content is a belief statement he can answer with a story.',
        'Rewritten to demand an observed before and after at ninety days, with a producer note telling D.J. not to rescue him if he cannot produce one.'],
       ['7', 'Gotcha risk on the Q and A question. As first written it read as an ambush, and ambushing a first-time guest in minute eighteen kills the second half of the interview.',
        'Q7 reframed as two practitioners comparing notes, with the exact recovery line written out and a landmine that forbids fact-checking him on air.'],
       ['8', 'Runtime. The draft ran nineteen questions plus Rapid Fire against a 43 minute target with a guest who teaches webinars for a living.',
        'Cut to sixteen plus one optional human landing. Cut list and never-cut list written.'],
       ['9', 'Sponsor exposure. His thesis is that the free page beats the paid website, and two sponsors sell in that neighborhood.',
        'Landmine 6, and the second half of Q2 makes him name what a website still does. That sentence is what makes the clip safe to ship.'],
       ['10', 'A death in one of his intake stories, with a first name and a room full of identifiable professionals.',
        'Landmine 7. It is deliberately not in the run of show, with hard rules if he raises it and a written line to land it.']],
      widths=[0.3, 3.2, 3.4])

h2('7B. Council Review')

h3('Member notes')
table(['Member', 'What they would change'],
      [['Alex Hormozi', 'Block 2 is the whole product. Q5 and Q6 are where an agent gets paid for listening. Every other question should be measured against whether it earns its ten minutes next to those two.'],
       ['MrBeast', 'The sag is minute twenty-two, right when the build finishes and the content talk starts. That bridge has to re-hook, not summarize. Make it accuse the listener of something.'],
       ['Brendan Kane', 'Title 1 is the insight device, title 2 is the stat device. Run both, they are not competing for the same click. But three of your first four titles started with a number, which means you were reaching for the same ingredient twice.'],
       ['Donald Miller', 'The hero is the agent with the blank profile, not the guy with the agency. Half the draft titles named his company. None of them do now. Grunt test on title 1: ranking is over, be the answer instead. Passes.'],
       ['Byron Lazine', 'The Q and A removal is the take. That is a real change with a real date on it, and it is the only thing in this episode a competitor show has not already run. Do not bury it at minute eighteen without flagging it in the description.'],
       ['Justin Welsh', 'Do not break the format for the Bob Jovi story. It is charming and it is not the episode. Keep it optional, keep it last, cut it before you cut the homework.'],
       ['Jon Youshaei', 'Every chapter title has to sell alone. Optimize Your Profile is not a chapter. How Real Estate Agents Get Their Google Profile Suspended is a chapter. Fix all twenty or fix none.'],
       ['Chris Do', 'Q9 costs him something to answer honestly and Q17a costs him something to answer at all. Those are the only two places in this episode where he is a person instead of a system. Protect both.']],
      widths=[1.4, 5.5])

h3('Witnesses called')
bullet('Chip and Dan Heath, on the curiosity claim: ', 'Title 1 opens the gap before it closes it. Ranking is over is the huh, being handed to the buyer is the aha, and the mechanism stays behind the click. The rejected draft, The Google Business Profile Checklist for Realtors, front-loaded the punchline and left nothing to find out. Curse of knowledge check: the cold open assumes the listener knows what a Google Business Profile is, which is fair, and assumes nothing about who Bobby Kerr is, which is required, because he is not a name your audience recognizes yet.')
bullet('Jonah Berger, on the sharing claim: ', 'The arousal here is anxiety, not awe. An agent hears 83% no click and feels behind, which shares well and converts to the homework. Social currency is in Q14: the agent who forwards the review-ask script looks like the one who found it. Valuable virality check: retell the takeaway in one sentence, "reviews should say the neighborhood and the problem you solved, not just five stars," and the point survives intact. That is the clip.')

h3('Title (pick one to run, keep the others to A/B)')
table(['#', 'Title', 'Ingredient', 'Curiosity mechanism'],
      [['1', 'Ranking Is Over. Bobby Kerr on Getting Handed to the Buyer as the Answer.', 'Insight', 'Kills a belief in the first four words, then withholds the mechanism.'],
       ['2', '83% of Google Searches Now End Without a Click. Bobby Kerr on How Agents Get Picked Anyway.', 'Stat', 'The number creates the threat, anyway promises the escape and does not describe it.'],
       ['3', 'The Free Google Page You Claimed and Forgot Is Now Your Front Door (Bobby Kerr)', 'Text and personality', 'Second person accusation. Strongest emotionally, weakest cold, because front door means nothing until he explains it.']],
      widths=[0.3, 3.1, 0.9, 2.6])
p('Recommended: #1 for the podcast feed and the social cuts, #2 for YouTube. They use different ingredients so they are a real A/B rather than two versions of one idea. Goal on this episode is reach, not the guest relationship, because he is a vendor and a first-timer with no audience overlap to protect.', italic=True)

h3('Cold-Open Hook (sharpened)')
p('"My guest today says the most valuable piece of real estate you own is not a listing, it is a free page on Google you probably have not opened since the day you claimed it. He has rebuilt more than a thousand of them for agents, and he says the ones winning right now are not ranking higher, they are getting handed to the buyer as the answer. We are going to talk about that today. Stay tuned."', italic=True)
p('Changed from the draft: the draft said 1,000 profiles and 10x more calls in the same breath. The 10x is unverified and it made the whole open sound like an ad. It is gone. The gap now closes on the phrase handed to the buyer as the answer, which is also the title.', italic=True, size=9.5)

h3('The Clip Engine')
table(['Q#', 'Question', 'Berger emotion', 'Heath gap'],
      [['14', 'The exact text message that gets a client to write a review that names the neighborhood and the problem.', 'Social currency, high. The agent who shares this looks like the one who found it.', 'Names the failed version everybody sends first, then withholds the fix until he says it out loud.'],
       ['13', 'Why the words in a review beat the star count.', 'Anxiety plus surprise. It devalues a metric the entire audience already tracks.', 'Takes something the listener thought was finished and reopens it.'],
       ['7', 'Google removed the Q and A section. What feeds the AI answer box now?', 'Anxiety, high arousal. Something they were told to do no longer exists.', 'A dated, checkable change, which makes the gap real rather than rhetorical.']],
      widths=[0.4, 2.6, 2.0, 1.9])

h3('Live-Description Scrub')
table(['Platform', 'Verdict and fix'],
      [['Facebook', 'Keep. Field by field, live is the promise that earns a comment. Question prompt is in.'],
       ['Instagram', 'Fixed. The draft was three sentences and IG buries anything past the first. Cut to one accusation plus three tags.'],
       ['TikTok', 'Fixed. The draft opened on Bobby Kerr, which means nothing to a stranger scrolling. It now opens on you have not opened it in two years.'],
       ['YouTube', 'Keep, and it is deliberately the longest. It is the only description doing search work, so Q and A removal and AI search visibility both stay in it by name.'],
       ['LinkedIn', 'Fixed. The draft was the Facebook copy in a suit. It now leads with the broker question, which is the only angle on this episode that is native to LinkedIn.']],
      widths=[1.1, 5.8])

h3('Arc Fix')
p('MrBeast is right about minute twenty-two. The draft bridge out of Block 2 was a summary, and a summary at the halfway mark is where a listener decides they got the point and leaves. The bridge is now written to accuse: it is empty, and it stays empty unless somebody feeds it, and this is where most agents outsource themselves into invisibility. That is a re-hook, not a hand-off, and it buys the second half of the episode. Second fix from the same note: Q15, the objection question, moved from Block 1 to Block 4. In the draft it sat early, which meant the biggest reason to quit listening was raised before he had earned the right to answer it.')

h3('Why It Should Work')
bullet('Curiosity mechanism (Heath): ', 'Ranking is a word every agent thinks they understand. The title takes it away in four words and does not replace it until the episode does.')
bullet('Share driver (Berger): ', 'Q14 hands the listener a script with a send button. Scripts get forwarded because forwarding one makes the sender look useful, which is social currency, not generosity.')
bullet('Retention move (MrBeast): ', 'Four blocks, each ending on something to do tonight, and a bridge at the sag point that accuses instead of summarizes.')

h3('The Dissent')
p('Hormozi will not sign off on Block 3. His position is that commodity versus non-commodity content is the softest ten minutes in the episode, that Q9 rests on a claim the guest probably cannot evidence, and that those minutes belong to more of Q5, the field-by-field build, which is the only part of this an agent can act on with certainty. The counter is that Block 3 is where both Rapid Fire callbacks live, and dropping it strands his best story. THE EXPERIMENT: watch what happens at Q9. If he cannot produce an observed before and after, that is the answer, and on the next vendor guest we cut the belief block entirely and run six build questions instead of four.')

h2('7C. EP Polish (pass 3)')
bullet('', 'Rebuilt Q1 off the Annapolis client result instead of his origin story, because his origin story has three versions and none of them can be stated on air.')
bullet('', 'Pulled every guest-supplied number out of the cold open, the three titles, the live stream title, and all five platform descriptions. The 10x more calls line was in the draft cold open and it made the show sound like an infomercial.')
bullet('', 'Moved Q15, the referrals objection, from Block 1 to Block 4, so the biggest reason to stop listening gets raised after he has earned the right to answer it.')
bullet('', 'Rewrote the Block 2 to Block 3 bridge from a summary into an accusation, because minute twenty-two was the sag.')
bullet('', 'Rewrote Q7, the Q and A question, from a correction into a comparing-notes question, and added the exact recovery line for the case where he says the feature is still there.')
bullet('', 'Rewrote Q9 to demand an observed ninety-day before and after instead of accepting a story, and added the note telling D.J. not to rescue him.')
bullet('', 'Added the second half to Q2, what the website still does, purely to protect the sponsor category and the clip.')
bullet('', 'Cut three questions to fit 43 minutes, and wrote the cut order and the never-cut list.')
bullet('', 'Demoted the Bob Jovi question to an optional human landing with an alternate, on Welsh\'s note, and gave it the cash-in-the-closet story as the swap.')
bullet('', 'Rewrote all twenty chapter markers so each one is a searchable headline on its own. Four of the drafted ones were labels, not headlines.')
bullet('', 'Rewrote the Instagram, TikTok, and LinkedIn descriptions, which were all the Facebook copy with the edges filed off.')
bullet('', 'Swept the whole document for em dashes, curly quotes, and AI-speak. Zero em dashes remain.')

doc.save('/Users/djparis/GitHub Projects/keeping-it-real-content-system/guest-prep/Bobby_Kerr_Interview_Prep.docx')
print('saved')
