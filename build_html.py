# -*- coding: utf-8 -*-
"""Generate standalone HTML topic decks (GitHub Pages friendly) from LinkedIn 101."""
import os

OUT = os.path.dirname(os.path.abspath(__file__))
BADGES = [("Students", "var(--blue)"), ("Early Career", "var(--green)"), ("Mid Career", "var(--orange)")]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# --------- components (return HTML fragments) ------------------------- #
def head(eyebrow, title, sub=None):
    h = f'<p class="eyebrow">{esc(eyebrow)}</p><h1 class="h1">{esc(title)}</h1>'
    if sub:
        h += f'<p class="sub">{esc(sub)}</p>'
    return h


def grid(cards, cols, bar=True):
    out = [f'<div class="grid cols-{cols}">']
    for c in cards:
        accent = c.get("accent", "var(--blue)")
        cls = "card bar" if bar else "card"
        if c.get("topbar"):
            cls = "card topbar"
        em = f'<span class="em">{c["emoji"]}</span> ' if c.get("emoji") else ""
        out.append(
            f'<div class="{cls}" style="--accent:{accent}">'
            f'<div class="ct">{em}{esc(c["title"])}</div>'
            f'<div class="cd">{esc(c["body"])}</div></div>')
    out.append("</div>")
    return "".join(out)


def numbered(items, cols):
    out = [f'<div class="grid cols-{cols}">']
    for n, t, d in items:
        out.append(
            f'<div class="card"><div class="row">'
            f'<div class="nb">{n}</div><div>'
            f'<div class="ct" style="color:var(--blue)">{esc(t)}</div>'
            f'<div class="cd">{esc(d)}</div></div></div></div>')
    out.append("</div>")
    return "".join(out)


def stats(items):
    out = ['<div class="grid cols-4">']
    for n, l in items:
        out.append(f'<div class="stat"><div class="num">{esc(n)}</div>'
                   f'<div class="lab">{esc(l)}</div></div>')
    out.append("</div>")
    return "".join(out)


def columns(cols):
    out = ['<div class="grid cols-3">']
    for col in cols:
        items = "".join(
            f'<div><div class="it-t">{esc(t)}</div><div class="it-d">{esc(d)}</div></div>'
            for t, d in col["items"])
        out.append(
            f'<div style="--accent:{col["color"]}">'
            f'<div class="colhead"><div class="ct">{esc(col["title"])}</div>'
            f'<div class="cd">{esc(col["sub"])}</div></div>'
            f'<div class="colbody">{items}</div></div>')
    out.append("</div>")
    return "".join(out)


def callout(title, body, soft=False):
    cls = "callout bar soft" if soft else "callout bar"
    t = f'<div class="h">{esc(title)}</div>' if title else ""
    return f'<div class="{cls}">{t}<p>{esc(body)}</p></div>'


def chips(badges):
    c = "".join(f'<span class="chip" style="--c:{col}">{esc(l)}</span>' for l, col in badges)
    return f'<div class="chips">{c}</div>'


def takeaways(points, quote):
    li = "".join(f'<li><span class="tick">✓</span><span>{esc(p)}</span></li>' for p in points)
    q = f'<div class="quote">{esc(quote)}</div>' if quote else ""
    return head("In summary", "Key takeaways") + f'<ul class="check">{li}</ul>' + q


def objectives(intro, items):
    rows = "".join(
        f'<div class="row"><div class="nb">{n}</div>'
        f'<div class="ot">{esc(t)}</div></div>' for n, t in enumerate(items, 1))
    return head("Learning objectives", "What you'll walk away with", intro) + \
        f'<div class="obj">{rows}</div>'


def arrowlist(items):
    li = "".join(f'<li><span class="ar">→</span><span>{esc(t)}</span></li>' for t in items)
    return f'<ul class="dots-list">{li}</ul>'


# --------- slide + doc wrappers -------------------------------------- #
def S(theme, inner, tag, page):
    return (f'<section class="slide {theme}"><div class="pad">{inner}</div>'
            f'<div class="wm">Cyhana Williams © 2026</div>'
            f'<div class="ftag">{esc(tag)}</div><div class="fpage">{page}</div></section>')


def title_slide(kick, big, lead, tag):
    inner = (f'<div class="kbar"></div><p class="kick">{esc(kick)}</p>'
             f'<h1 class="big">{esc(big)}</h1><p class="lead">{esc(lead)}</p>{chips(BADGES)}')
    return S("grad", inner, tag, "")


def doc(title, slides):
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · LinkedIn 101</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css"></head>
<body><div class="deck"><div class="stage">{"".join(slides)}</div>
<div class="controls">
<button class="nav prev" aria-label="Previous">‹</button>
<div class="dots"></div>
<button class="nav next" aria-label="Next">›</button>
<div class="pageno"><span id="cur">01</span> / <span id="tot">01</span></div>
<button class="pbtn" onclick="window.print()" title="Save as PDF / Print this deck">⤓ PDF</button>
<a class="home" href="index.html">⌂ All topics</a></div></div>
<script src="deck.js"></script></body></html>'''


def write(fname, html):
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(html)


# ===================================================================== #
TAG = "LinkedIn 101 · "


def topic01():
    t = TAG + "Topic 01 — Why LinkedIn Matters"
    s = []
    s.append(title_slide("Topic 01 · Foundations", "Why LinkedIn Matters",
             "Before building a profile, understand what LinkedIn is for and why it has "
             "become the front door to the professional world.", t))
    s.append(S("light", objectives("By the end of this topic you will be able to:",
              ["Explain the main reasons professionals join LinkedIn",
               "Recognise how overlapping goals create the most opportunity",
               "Quote the platform's scale and the hidden job market"]), t, "02"))
    reasons = [
        {"emoji": "🔍", "title": "Job Search & Internships", "accent": "var(--blue)",
         "body": "Browse roles, apply directly, or get discovered by recruiters."},
        {"emoji": "🤝", "title": "Connections & Networking", "accent": "var(--blue)",
         "body": "Build relationships with peers, alumni, mentors, and collaborators."},
        {"emoji": "📢", "title": "Personal Branding", "accent": "var(--orange)",
         "body": "Craft your professional identity — how the world sees you."},
        {"emoji": "📣", "title": "Marketing & Visibility", "accent": "var(--purple)",
         "body": "Promote a product, service, or organisation to a pro audience."},
        {"emoji": "💰", "title": "Investors & Partners", "accent": "var(--purple)",
         "body": "Connect with funders, co-founders, clients, and partners."},
        {"emoji": "🎤", "title": "Speaking & Thought Leadership", "accent": "var(--green)",
         "body": "Get booked for panels, podcasts, and events by being visible."},
        {"emoji": "📚", "title": "Learning & Research", "accent": "var(--teal)",
         "body": "LinkedIn Learning, industry leaders, and trend tracking."},
    ]
    s.append(S("light", head("Before we dive in", "Why do people join LinkedIn?",
              "Most people tick more than one reason — and the magic happens where they overlap.")
              + grid(reasons, 3)
              + callout("", "💡 People who use LinkedIn for several reasons at once consistently "
                        "get the most opportunities."), t, "03"))
    s.append(S("dark", head("Why it matters", "LinkedIn by the numbers")
              + stats([("1B+", "Members worldwide"), ("67M", "Companies listed"),
                       ("87%", "Of talent pros use it to hire"), ("200+", "Countries & territories")])
              + callout("The hidden job market",
                        "About 70% of jobs are never publicly posted — they are filled through "
                        "networks. LinkedIn is how you reach roles before they hit a job board.", soft=True),
              t, "04"))
    s.append(S("dark", takeaways(
        ["LinkedIn is a job board, a network, and a personal-brand platform at once.",
         "Using it for multiple overlapping goals unlocks the most opportunity.",
         "With 1B+ members and 87% of recruiters active, presence is not optional.",
         "Most roles are filled through networks — show up before the job is posted."],
        "“70% of jobs are never publicly posted — LinkedIn is how you reach them.”"), t, "05"))
    write("topic-01.html", doc("Why LinkedIn Matters", s))
    return ("Why LinkedIn Matters", "Why LinkedIn is the front door to the professional world.", "2–3", 5, "topic-01.html")


def topic02():
    t = TAG + "Topic 02 — Personal Branding"
    s = []
    s.append(title_slide("Topic 02 · Section 01", "Personal Branding 101",
             "Your brand is what people say about you when you're not in the room. "
             "Start where you are — and build up.", t))
    s.append(S("dark", objectives("By the end of this topic you will be able to:",
              ["Define what a personal brand is and why it matters",
               "Match branding actions to your current network size",
               "Apply consistency, proof, and social proof to build trust"]), t, "02"))
    cols = [
        {"title": "🟢 Beginner", "color": "var(--green)", "sub": "0–100 connections · build a foundation",
         "items": [("Define your niche", "Pick 1–2 areas to be known for. “UX + fintech” beats “design.”"),
                   ("Be consistent everywhere", "Same name, photo, tone across LinkedIn, résumé, email."),
                   ("Show, don't just tell", "Add portfolio links and project media — proof beats claims.")]},
        {"title": "🔵 Intermediate", "color": "var(--blue)", "sub": "100–500 connections · build visibility",
         "items": [("Post 1–3× per week", "Share lessons, wins, or questions. Consistency beats virality."),
                   ("Give before you ask", "Comment with insight and share resources before any ask."),
                   ("Engage daily", "Comments you leave on others' posts are content too.")]},
        {"title": "🟣 Advanced", "color": "var(--purple)", "sub": "500+ connections · grow reputation",
         "items": [("Collect recommendations", "2–3 strong written recs boost credibility fast."),
                   ("Refresh every 3–6 months", "Update skills, roles, headline; toggle “Open to Work.”"),
                   ("Lead the conversation", "Move from sharing to thought leadership in your niche.")]},
    ]
    s.append(S("light", head("Section 01 · Personal Branding", "Branding tips by level",
              "Pick the stage that matches your network, then work the tactics for it.")
              + columns(cols), t, "03"))
    s.append(S("light", head("Section 01 · Personal Branding", "The five habits of a strong brand",
              "Small, consistent actions compound into reputation over time.")
              + arrowlist([
                  "Define a niche identity — be searchable and memorable for 1–2 specific things.",
                  "Stay consistent across every channel — consistency is what builds trust.",
                  "Provide proof of work — portfolio links, media, and decks beat claims.",
                  "Give value before you ask — congratulate, comment, and share resources.",
                  "Gather social proof — recommendations from people who know your work."]), t, "04"))
    s.append(S("dark", takeaways(
        ["Your brand is your reputation — manage it deliberately.",
         "Match tactics to your stage: foundation → visibility → reputation.",
         "Consistency and proof of work build trust faster than self-description.",
         "Give value first; recommendations seal credibility."],
        "“Your network is a reflection of your brand — build it with intention.”"), t, "05"))
    write("topic-02.html", doc("Personal Branding", s))
    return ("Personal Branding", "Build a credible brand at any stage of your network.", "5", 5, "topic-02.html")


def topic03():
    t = TAG + "Topic 03 — Profile Setup"
    s = []
    s.append(title_slide("Topic 03 · Section 02", "Setting Up Your Profile",
             "Photo, banner, headline, and mutual connections decide whether someone "
             "connects with you or scrolls past — before they ever click.", t))
    s.append(S("light", objectives("By the end of this topic you will be able to:",
              ["Choose a profile photo that earns 21× more views",
               "Lay out every element of your profile header correctly",
               "Complete the six sections of an All-Star profile"]), t, "02"))
    photo = [
        {"title": "✓ Great — Headshot", "accent": "var(--green)",
         "body": "Clear face, looking at camera · neutral background · well-lit & sharp · smart-casual attire."},
        {"title": "✓ Great — Framing", "accent": "var(--green)",
         "body": "Dressed for your industry · confident posture · recent (2–3 yrs) · face fills 60–70% of frame."},
        {"title": "✗ Avoid — Mistakes", "accent": "var(--red)",
         "body": "Blurry / low-res · cropped from a group photo · sunglasses, hats, filters · no photo at all."},
    ]
    s.append(S("light", head("Section 02 · Profile Setup", "Your profile photo",
              "Profiles with a photo get 21× more views and 9× more connection requests.")
              + grid(photo, 3), t, "03"))
    anatomy = [
        ("1", "Banner (1584×396px)", "Show your field or niche. Use Canva — search 'LinkedIn banner'."),
        ("2", "Profile photo", "Headshot, well-lit, plain background; face fills 60–70% of frame."),
        ("3", "Name + verification", "Real, full name. Add pronouns and the audio-name feature."),
        ("4", "Headline (220 chars)", "Not a job title — Role | Value Prop | Passion. Shows in search."),
        ("5", "Followers & connections", "Connections show trust, followers show reach. Aim for 500+."),
        ("6", "Open to Work / Hiring", "Toggle the green banner when looking; limit to recruiters only."),
    ]
    s.append(S("light", head("Section 02 · Profile Setup", "Profile header anatomy",
              "Six elements decide your first impression. Get every one right.")
              + numbered(anatomy, 2), t, "04"))
    checks = [
        {"emoji": "📷", "title": "Profile photo", "body": "Professional headshot, good lighting, plain background. Smile."},
        {"emoji": "🌐", "title": "Background banner", "body": "Show your field or brand. Canva templates make it easy."},
        {"emoji": "⭐", "title": "Headline", "body": "Role | Value Prop | Passion/Goal — not just a job title."},
        {"emoji": "📖", "title": "About / summary", "body": "3–5 first-person sentences: who you are + what you want."},
        {"emoji": "💼", "title": "Experience", "body": "Include internships, part-time jobs, volunteering, campus roles."},
        {"emoji": "🏅", "title": "Skills", "body": "Add 5–10 relevant skills and ask peers to endorse you."},
    ]
    s.append(S("dark", head("All-Star profile", "The six sections that matter",
              "Complete all six and LinkedIn surfaces you far more often in recruiter searches.")
              + grid(checks, 3, bar=False), t, "05"))
    s.append(S("dark", takeaways(
        ["A photo earns 21× more views and 9× more connection requests — never skip it.",
         "Your banner, photo, name, and headline are visible before anyone clicks.",
         "Use the headline formula: Role | Value Prop | Passion — not a bare job title.",
         "Completing all six sections unlocks All-Star and recruiter visibility."],
        "“Your photo, name, headline, and mutuals decide who connects — or scrolls past.”"), t, "06"))
    write("topic-03.html", doc("Profile Setup", s))
    return ("Profile Setup", "Photo, header anatomy, and the All-Star checklist.", "6–8", 6, "topic-03.html")


def topic04():
    t = TAG + "Topic 04 — Headline & Summary"
    s = []
    s.append(title_slide("Topic 04 · Section 03", "Headline & Your Story",
             "Your headline is what shows up in search. Your About section tells the "
             "story behind it. Here is the formula for both.", t))
    s.append(S("dark", objectives("By the end of this topic you will be able to:",
              ["Write a headline using the Role | Value Prop | Passion formula",
               "Rewrite weak headlines into searchable, memorable ones",
               "Draft a punchy first-person About section"]), t, "02"))
    examples = [
        ("Student", "var(--blue)", "Student at University of Michigan",
         "CS Student | Full-Stack Intern @ Google | Building accessible web apps"),
        ("Early Career", "var(--orange)", "Looking for opportunities",
         "Marketing Coordinator | Content Strategy | Helping B2B brands grow through storytelling"),
        ("Mid Career", "var(--purple)", "Software Engineer",
         "Software Engineer @ Stripe | Open-source contributor | Passionate about fintech infrastructure"),
    ]
    exhtml = '<div class="formula">Formula:&nbsp;&nbsp;Role&nbsp; | &nbsp;Value Prop&nbsp; | &nbsp;Passion / Goal</div>'
    for label, col, bad, good in examples:
        exhtml += (f'<div class="ex"><span class="chip" style="--c:{col};font-size:1cqw">{esc(label)}</span>'
                   f'<div class="bad">✗ {esc(bad)}</div><div class="good">✓ {esc(good)}</div></div>')
    s.append(S("light", head("Section 03 · Your Story", "The headline formula") + exhtml, t, "03"))
    about = [
        {"emoji": "1", "title": "Who you are", "body": "Open with your current role or focus and the value you bring.", "accent": "var(--blue)"},
        {"emoji": "2", "title": "What you've done", "body": "Highlight 2–3 concrete wins, projects, or experiences.", "accent": "var(--blue)"},
        {"emoji": "3", "title": "What you want next", "body": "End with your goal — the roles, people, or work you want.", "accent": "var(--blue)"},
    ]
    s.append(S("dark", head("Section 03 · Your Story", "Your About section",
              "Write in the first person. Tell your story in 3–5 punchy sentences.")
              + grid(about, 3, bar=False)
              + callout("", "💡 Keep it human. First person, short sentences, and a clear ask "
                        "read far better than a formal third-person bio.", soft=True), t, "04"))
    s.append(S("dark", takeaways(
        ["Headline = Role | Value Prop | Passion — it is what appears in search results.",
         "Replace vague lines like “Looking for opportunities” with specific value.",
         "Write your About section in the first person, in 3–5 punchy sentences.",
         "Structure it: who you are → what you've done → what you want next."],
        "“Don't describe a job title — tell people the value you create.”"), t, "05"))
    write("topic-04.html", doc("Headline & Summary", s))
    return ("Headline & Summary", "The formula for a headline and About section that convert.", "9", 5, "topic-04.html")


def topic05():
    t = TAG + "Topic 05 — Networking"
    s = []
    s.append(title_slide("Topic 05 · Section 04", "Building Your Network",
             "Start with people you know. Grow with purpose. A strong network is the "
             "single biggest driver of opportunity on LinkedIn.", t))
    s.append(S("light", objectives("By the end of this topic you will be able to:",
              ["Apply the four principles of strategic networking",
               "Prioritise who to connect with first",
               "Send personalised connection requests using proven templates"]), t, "02"))
    pr = [
        {"emoji": "🔗", "title": "Personalise every request", "accent": "var(--blue)",
         "body": "Mention how you know them or why you want to connect. Generic requests get ignored."},
        {"emoji": "💬", "title": "Value first, ask second", "accent": "var(--green)",
         "body": "Comment on a post or congratulate a win before asking for anything."},
        {"emoji": "📈", "title": "Target 2nd-degree connections", "accent": "var(--orange)",
         "body": "Shared mutuals create instant common ground and make outreach feel natural."},
        {"emoji": "🔔", "title": "Follow target companies", "accent": "var(--purple)",
         "body": "Track openings and culture; engage with their posts to get noticed."},
    ]
    s.append(S("light", head("Section 04 · Networking", "Four principles of strategic networking")
              + grid(pr, 2)
              + callout("Who to connect with first",
                        "Classmates → Professors → Alumni → Past internship teammates → Speakers at events you attend."),
              t, "03"))
    tpls = [
        ("Peer / Classmate", "var(--blue)",
         "“Hi [Name], we're both studying [field] at [University]. I've seen your work on [project] and "
         "would love to stay connected as we navigate post-grad life. Hope to keep in touch!”"),
        ("Alumni Outreach", "var(--purple)",
         "“Hi [Name], I'm a [year] student at [University] studying [major]. Your path from [University] to "
         "[Company] is really inspiring — I'd love to connect and learn from your journey. No pressure at all!”"),
        ("Recruiter / Professional", "var(--green)",
         "“Hi [Name], I came across your profile while researching [Company]. I'm really interested in "
         "[role/field] and your work on [specific thing] stood out. I'd love to connect and follow along.”"),
    ]
    tplhtml = ""
    for label, col, body in tpls:
        tplhtml += (f'<div class="tpl"><span class="chip" style="--c:{col};font-size:1cqw">{esc(label)}</span>'
                    f'<div class="body">{esc(body)}</div></div>')
    s.append(S("dark", head("Templates", "The perfect connection message",
              "Personalised requests are accepted far more often. Adapt these to your situation.")
              + tplhtml, t, "04"))
    s.append(S("dark", takeaways(
        ["Always personalise — say how you know them or why you're reaching out.",
         "Give value before you ask; engage with their content first.",
         "Target 2nd-degree connections to leverage shared mutuals.",
         "Start close (classmates, professors, alumni) and grow outward with intent."],
        "“Generic requests get ignored — a single personal sentence changes everything.”"), t, "05"))
    write("topic-05.html", doc("Networking", s))
    return ("Networking & Messages", "Principles plus copy-paste connection templates.", "10–11", 5, "topic-05.html")


def topic06():
    t = TAG + "Topic 06 — Content & Engagement"
    s = []
    s.append(title_slide("Topic 06 · Section 05", "Content & Engagement",
             "Stay consistent — you don't need to go viral to be seen. Engagement and a "
             "weekly post keep you visible to the people who matter.", t))
    s.append(S("light", objectives("By the end of this topic you will be able to:",
              ["Build a simple, sustainable engagement routine",
               "Choose content ideas that reliably perform",
               "Structure a post that stands out in the feed"]), t, "02"))
    ladder = [
        {"emoji": "👍", "title": "React", "accent": "var(--blue)", "topbar": True,
         "body": "React to 3–5 posts a day. Keeps you visible in the feed."},
        {"emoji": "💬", "title": "Comment", "accent": "var(--green)", "topbar": True,
         "body": "1–2 thoughtful sentences. Comments strongly boost visibility."},
        {"emoji": "🔄", "title": "Share", "accent": "var(--orange)", "topbar": True,
         "body": "Reshare industry news or articles and add your own take."},
        {"emoji": "✏️", "title": "Post", "accent": "var(--purple)", "topbar": True,
         "body": "One original post a week — lessons, wins, questions, insights."},
    ]
    s.append(S("light", head("Section 05 · Content", "Engaging with content",
              "Four habits, from lowest to highest effort — all keep you visible.")
              + grid(ladder, 4)
              + callout("⚡ Easy first post",
                        "“3 things I learned from my internship at [Company].”  Personal + honest = high "
                        "engagement. You don't need a big audience to start."), t, "03"))
    ideas = [
        {"emoji": "💡", "title": "Lessons learned", "body": "“3 things my internship taught me about X.”", "accent": "var(--blue)"},
        {"emoji": "📈", "title": "Career wins", "body": "New job, promotion, or a project milestone.", "accent": "var(--green)"},
        {"emoji": "💬", "title": "Hot takes", "body": "A contrarian opinion on a trend in your field.", "accent": "var(--orange)"},
        {"emoji": "📖", "title": "Resources / lists", "body": "“5 free tools every designer should know.”", "accent": "var(--purple)"},
        {"emoji": "🔧", "title": "Behind the scenes", "body": "Day-in-the-life or a process breakdown.", "accent": "var(--teal)"},
        {"emoji": "❓", "title": "Questions", "body": "Ask your network — high comment bait.", "accent": "var(--blue)"},
    ]
    s.append(S("light", head("Section 05 · Content", "Content ideas that perform")
              + grid(ideas, 3), t, "04"))
    s.append(S("dark", head("Section 05 · Content", "Five ways to make a post stand out",
              "The structure of a post matters as much as the idea behind it.")
              + arrowlist([
                  "Hook first — your opening line is everything; LinkedIn truncates after 2–3 lines.",
                  "Use white space — short, punchy paragraphs beat walls of text. One idea per line.",
                  "Add an image or graphic — posts with visuals get 2× more engagement.",
                  "End with a question or CTA — “What's your take?” drives comments.",
                  "Use 3–5 relevant hashtags at the end, not in the body. #Design #CareerTips #UX"]), t, "05"))
    s.append(S("dark", takeaways(
        ["Consistency beats virality — show up in the feed every day.",
         "React, comment, share, and post one original piece a week.",
         "Lead with a hook, use white space, and add a visual for 2× engagement.",
         "End every post with a question or CTA to drive comments."],
        "“You don't need to go viral to be seen — you need to be consistent.”"), t, "06"))
    write("topic-06.html", doc("Content & Engagement", s))
    return ("Content & Engagement", "An engagement routine and posts that stand out.", "12–13", 6, "topic-06.html")


def topic07():
    t = TAG + "Topic 07 — Job Search"
    s = []
    s.append(title_slide("Topic 07 · Section 06", "Job Search & Applying",
             "LinkedIn is where most roles are filled. Find openings before they hit the "
             "job board — and apply in a way that gets noticed.", t))
    s.append(S("dark", objectives("By the end of this topic you will be able to:",
              ["Set up alerts and find hidden openings via hashtags",
               "Apply strategically and research hiring managers",
               "Use referrals and follow-ups to stand out"]), t, "02"))
    employers = ["SAP", "Siemens", "BMW Group", "Bosch", "Deutsche Bank", "Mercedes-Benz",
                 "Deutsche Telekom", "Allianz", "Zalando", "Bayer"]
    pills = '<div class="pills">' + "".join(f'<span class="pill">{esc(e)}</span>' for e in employers) + "</div>"
    s.append(S("dark", head("Section 06 · Job Search", "The scale of the opportunity",
              "LinkedIn is the dominant professional network in many markets — here is Germany / DACH.")
              + stats([("16M+", "Users in Germany (2023)"), ("#1", "Network in DACH"),
                       ("3M+", "Active job listings (DE)"), ("67M", "Companies worldwide")])
              + callout("Major employers active on LinkedIn", "", soft=True).replace("<p></p>", pills),
              t, "03"))
    steps = [
        ("01", "Set up job alerts", "Search role + location → 'Set Alert'. Be first to apply to new postings."),
        ("02", "Search hiring hashtags", "#hiring #vacancy #opportunity #nowhiring #jobopening — find posts the board misses."),
        ("03", "Use 'Easy Apply' wisely", "Great for volume, but apply on company sites for competitive roles."),
        ("04", "Research hiring managers", "Find them before applying and personalise to their team."),
        ("05", "Ask for referrals", "A 1st/2nd-degree connection at the company hugely boosts your chances."),
        ("06", "Follow up thoughtfully", "A brief, confident message after applying sets you apart."),
    ]
    s.append(S("light", head("Section 06 · Job Search", "Six steps to a smarter job search")
              + numbered(steps, 2), t, "04"))
    s.append(S("dark", head("Section 06 · Job Search", "The hidden job market: hashtags",
              "Many recruiters post openings directly in their feed — these never appear on the job board.")
              + arrowlist([
                  "Search #hiring, #vacancy, #opportunity, #nowhiring, #jobopening in the search bar.",
                  "Recruiter posts include role, location, level, and an invitation to comment or DM.",
                  "Engage early — comment or DM the hiring manager while the post is fresh.",
                  "Tag or refer a great fit — visible engagement gets you noticed by the recruiter."]), t, "05"))
    s.append(S("dark", takeaways(
        ["Set alerts so you're first to apply to new postings.",
         "Search hiring hashtags to reach openings that never hit the job board.",
         "Research the hiring manager and personalise before you apply.",
         "Referrals are one of the top hiring channels — always ask a connection."],
        "“Referrals are consistently one of the top hiring channels — use your network.”"), t, "06"))
    write("topic-07.html", doc("Job Search", s))
    return ("Job Search & Applying", "Find hidden openings and apply so you get noticed.", "14", 6, "topic-07.html")


def topic08():
    t = TAG + "Topic 08 — Staying Safe Online"
    s = []
    s.append(title_slide("Topic 08 · Safety", "Staying Safe Online",
             "A strong presence also means a safe one. Spot scams, lock down your account, "
             "and avoid the behaviour that gets profiles restricted.", t))
    s.append(S("dark", objectives("By the end of this topic you will be able to:",
              ["Recognise the most common LinkedIn scams and fake profiles",
               "Secure your account with 2FA and good password hygiene",
               "Avoid the behaviours that get profiles restricted"]), t, "02"))
    scams = [
        {"emoji": "👤", "title": "Too-good-to-be-true offers", "accent": "var(--red)",
         "body": "Unsolicited DMs offering high salaries for vague roles with no interview are almost always scams."},
        {"emoji": "💸", "title": "Requests for money / gift cards", "accent": "var(--red)",
         "body": "Legitimate recruiters never ask you to pay fees, buy equipment, or send payment."},
        {"emoji": "🔗", "title": "Suspicious links in messages", "accent": "var(--red)",
         "body": "Never click unknown links in DMs — even from connections. Hover before clicking."},
        {"emoji": "🧑‍💻", "title": "Fake recruiter profiles", "accent": "var(--red)",
         "body": "Few connections, stock photo, no history, recent account — verify on the company site."},
        {"emoji": "💬", "title": "Romance / trust scams", "accent": "var(--red)",
         "body": "Scammers build rapport over weeks before a financial ask. Be wary of overly personal DMs."},
        {"emoji": "🛡️", "title": "When in doubt, slow down", "accent": "var(--red)",
         "body": "Urgency is a tactic. Verify independently before sharing anything or acting."},
    ]
    s.append(S("dark", head("Stay safe online", "Scams & fake profiles to watch for")
              + grid(scams, 3, bar=False), t, "03"))
    protect = [
        {"emoji": "🔐", "title": "Enable 2FA", "accent": "var(--green)",
         "body": "Settings → Sign in & Security → Two-step verification. Use an authenticator app over SMS."},
        {"emoji": "🔑", "title": "Strong, unique password", "accent": "var(--green)",
         "body": "Never reuse your email password. Use a manager like Bitwarden or 1Password."},
        {"emoji": "📧", "title": "Watch for phishing", "accent": "var(--green)",
         "body": "LinkedIn never asks for your password by email. Log in via the official site."},
        {"emoji": "👁️", "title": "Review active sessions", "accent": "var(--green)",
         "body": "Settings → Security → Where you're signed in. Remove devices you don't recognise."},
        {"emoji": "🔒", "title": "Control visibility", "accent": "var(--green)",
         "body": "Settings → Visibility — choose who sees your connections, email, and activity."},
        {"emoji": "✅", "title": "Two minutes, today", "accent": "var(--green)",
         "body": "Most of these take under five minutes — set them up before anything else."},
    ]
    s.append(S("light", head("Stay safe online", "Protect your account")
              + grid(protect, 3), t, "04"))
    restrict = [
        {"emoji": "🤖", "title": "Bot-like behaviour", "body": "Mass connection requests sent too fast trip spam filters.", "accent": "var(--orange)"},
        {"emoji": "📛", "title": "Fake name / impersonation", "body": "False names or fictional profiles violate the User Agreement.", "accent": "var(--orange)"},
        {"emoji": "📢", "title": "Spam / aggressive promo", "body": "Repeated unsolicited sales messages or duplicated content.", "accent": "var(--orange)"},
        {"emoji": "🚫", "title": "Prohibited content", "body": "Hate speech, harassment, misinformation, or adult content.", "accent": "var(--orange)"},
        {"emoji": "📋", "title": "Multiple accounts", "body": "One person = one profile. Extra personal profiles break policy.", "accent": "var(--orange)"},
        {"emoji": "🔔", "title": "Too many rejections", "body": "Many “I don't know this person” marks restrict your connecting.", "accent": "var(--orange)"},
    ]
    s.append(S("dark", head("Stay safe online", "Why profiles get restricted",
              "Stay within LinkedIn's User Agreement — these behaviours trigger restrictions or bans.")
              + grid(restrict, 3, bar=False), t, "05"))
    s.append(S("dark", takeaways(
        ["If an offer seems too good to be true, it almost certainly is.",
         "Never pay fees or click unknown links — recruiters won't ask you to.",
         "Turn on 2FA and use a unique password today; it takes two minutes.",
         "Avoid bot-like mass requests and fake details — they get profiles restricted."],
        "“Legitimate recruiters never ask you to pay — protect your account first.”"), t, "06"))
    write("topic-08.html", doc("Staying Safe Online", s))
    return ("Staying Safe Online", "Spot scams, secure your account, avoid restrictions.", "15", 6, "topic-08.html")


def topic09():
    t = TAG + "Topic 09 — Action Plan & Resources"
    s = []
    s.append(title_slide("Topic 09 · Wrap-up", "Your Action Plan",
             "You don't need to be perfect — you just need to start. Here is exactly what "
             "to do today, this week, and this month.", t))
    cols = [
        {"title": "Today", "color": "var(--blue)", "sub": "Get the basics live",
         "items": [("Create an account", "Sign up at linkedin.com if you haven't (it's free)."),
                   ("First impression", "Set your photo, banner, and headline."),
                   ("Connect with 3–5", "People who'll recognise your name.")]},
        {"title": "This Week", "color": "var(--green)", "sub": "Flesh out the profile",
         "items": [("Write your About", "First person, 3–5 sentences."),
                   ("Add 3 roles + 5 skills", "Your top experiences and skills."),
                   ("Follow 5 companies", "Ones you admire or want to join."),
                   ("Comment on 3 posts", "Thoughtfully, in your feed.")]},
        {"title": "This Month", "color": "var(--purple)", "sub": "Build momentum",
         "items": [("Grow to 50–100", "Only people you know or have met."),
                   ("Get 2 recommendations", "From people who know your work."),
                   ("Post your first content", "Lessons, a win, or a question."),
                   ("Apply to 3 roles", "That match your goals.")]},
    ]
    s.append(S("light", head("Your action plan", "Leave here ready to act")
              + columns(cols), t, "02"))
    res = [
        {"emoji": "📘", "title": "LinkedIn Learning · Free", "body": "Free courses on LinkedIn basics, personal branding, and job searching.", "accent": "var(--blue)"},
        {"emoji": "📰", "title": "LinkedIn's Official Blog · Free", "body": "Tips on profile optimisation, algorithm changes, and career advice.", "accent": "var(--blue)"},
        {"emoji": "🎨", "title": "Canva · Free", "body": "Free banner templates — search 'LinkedIn banner' and customise.", "accent": "var(--blue)"},
        {"emoji": "🎓", "title": "Alumni Networks · Built-in", "body": "University page → Alumni → filter by company or location.", "accent": "var(--blue)"},
    ]
    s.append(S("dark", head("Keep learning", "Helpful resources")
              + grid(res, 2, bar=False), t, "03"))
    closing = ('<div class="kbar"></div>'
               '<h1 class="big">Your Network<br>Is Your Net Worth</h1>'
               '<p class="lead">You don\'t need to be perfect — you just need to start. Update your '
               'profile this week. Your future self will thank you.</p>'
               '<div style="margin-top:3cqh"><div style="font-family:Poppins;font-weight:700;'
               'font-size:1.8cqw">Cyhana Williams</div>'
               '<div style="color:var(--blue-l);font-size:1.3cqw;margin-top:.4cqh">'
               'Co-founder, African Women in GIS · linktr.ee/cyhana</div></div>')
    s.append(S("grad", closing, t, ""))
    write("topic-09.html", doc("Action Plan & Resources", s))
    return ("Action Plan & Resources", "Your 30-day plan plus free resources to keep going.", "16–17", 4, "topic-09.html")


def build_index(rows):
    cards = ""
    for i, (name, desc, src, n, fn) in enumerate(rows, 1):
        pptx = "pptx/" + fn.replace(".html", ".pptx")
        cards += (f'<div class="tcard">'
                  f'<div class="tnum">TOPIC {i:02d}</div>'
                  f'<div class="tname">{esc(name)}</div>'
                  f'<div class="tdesc">{esc(desc)}</div>'
                  f'<div class="meta">{n} slides · from parent slides {esc(src)}</div>'
                  f'<div class="tactions">'
                  f'<a class="btn-open" href="{fn}">Open deck →</a>'
                  f'<a class="btn-dl" href="{pptx}" download>⤓ .pptx</a>'
                  f'</div></div>')
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LinkedIn 101 — Topic Presentations</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css"></head>
<body><div class="idx">
<div class="kick">BUILD YOUR PROFESSIONAL PRESENCE ONLINE</div>
<h1>LinkedIn 101 — Topic Presentations</h1>
<p class="lead">Nine standalone, self-paced decks adapted from the full LinkedIn 101 session.
Use ← → or swipe to navigate each one. Built for students and early-career professionals.</p>
<div class="idxbar"><a class="btn-all" href="linkedin-101-pptx.zip" download>⤓ Download all decks (.pptx, .zip)</a></div>
<div class="cards">{cards}</div>
<footer>Cyhana Williams © 2026 · Co-founder, African Women in GIS · linktr.ee/cyhana</footer>
</div></body></html>'''
    write("index.html", html)


if __name__ == "__main__":
    builders = [topic01, topic02, topic03, topic04, topic05, topic06, topic07, topic08, topic09]
    rows = [b() for b in builders]
    build_index(rows)
    print("Generated:")
    for i, (name, desc, src, n, fn) in enumerate(rows, 1):
        print(f"  {fn:16s} Topic {i:02d} — {name} ({n} slides, src {src})")
    print("  index.html")
