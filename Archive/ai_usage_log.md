# AI Usage Log

## Entry 1

### Date
May 19, 2026

### AI Tool Used
Claude (Anthropic)

### What I Asked AI
"This is my cs class work and I really want to treat this a a opportunity to practice my building skills for future projects, so i kinda want to challenge my self for lane 4 but what kind of project can i work on this time, also what are the relationship between lanes, is lane 4 build on top of lane3 by former containing the latter skills"
(Attached: screenshot of the four-lane assignment table from class.)

### Why I Asked
I wanted to understand the structure of the assignment before choosing a project. I was specifically confused about whether the lanes formed a difficulty ladder (Lane 4 = Lane 3 + extra) or whether they were separate categories. I also wanted external project ideas to react to, since I find it easier to refine an existing idea than to generate one from scratch.

### What AI Gave Me
1. A clarification that the lanes are categories, not a skill ladder. Lane 4 is defined by complexity and combination, not by being a strict superset of the others.
2. Four Lane 4 project ideas tailored to my background: an AP Stats practice dashboard, a film photography EXIF logbook, a PaoPal matching simulator, and a tarot pattern journal.
3. A recommendation toward the AP Stats dashboard for strategic reasons (overlaps with my May exam prep).

### What I Used
- The clarification about lane structure. This changed how I read the rubric.
- The general framing that Lane 4 = combining skills from multiple lanes.

### What I Changed or Rejected
- I rejected all four of Claude's specific project ideas. None of them felt personally exciting in the moment. I noticed I responded better to ideas that connected to something tactile I was currently living with (the vinyl player I just bought) rather than ideas that were strategically optimal.

### What I Still Do Not Fully Understand
Where the boundary actually is between Lane 2 and Lane 4. A "personal utility" with one API call sounds like Lane 2, but a "personal utility" with multiple filters and external links sounds like Lane 4. The line is fuzzy.

### My Next Step
Pitch my own idea (vinyl recommendation site) and stress-test it against Claude.

---

## Entry 2

### Date
May 19, 2026

### AI Tool Used
Claude (Anthropic)

### What I Asked AI
"is lane four algorithms related? if so then i'm actually not interested, My ideas are since i just bought a Vinyl record player, so i kinda want to build a website that provide different filter for the user and giving suggestions on which album might the user like potentially, also linking a taobao link or a amazon link underneath? I'm thinking it's better to fetch like, as much songs as I can to my website but check for the feasibility for me, it would definitely cost me more on storing the data right? but wait no where's it gonna be store? it's a front-end thing. also if i'm going to fetch the test-play for the song, it's against the copyright right? what about the album cover with a link to spotify/applemusic and user can listen on that, well what's the different between my website and spotify or applemusic? my uniqueness would be the way that the music is delivered, like we're used to listen the music song by song instead of album by album, so maybe make the website more aesthetic? like make it like a gallery? challenge my idea and brainstorm with me."

### Why I Asked
I had a rough idea I was emotionally attached to but I had not pressure-tested it. I wanted Claude to push back on the weak parts instead of just praising the concept. I also had several scattered technical anxieties (storage, copyright, differentiation) that I wanted resolved before I committed to the project.

### What AI Gave Me
1. Clarification that Lane 4 is not algorithm-specific.
2. Technical answers: I do not need to store songs (use APIs), 30-second previews via Spotify API are legal, full songs are not.
3. A sharp challenge on my "make it more aesthetic" answer to differentiation. Claude pointed out that this is a vibe, not a value proposition.
4. The reframe that became the actual project thesis: Spotify is song-and-shuffle-optimized, vinyl culture is album-and-intentional-listening-optimized, and the filter dimensions should match the vinyl ethos (mood, side balance, listening context) rather than copying genre filters.
5. A warning that "fetch as much as I can" is the wrong instinct because curation is the product.

### What I Used
- The "Spotify is structurally song-based, mine should be album-based" framing. This became the core of the project.
- The filter dimension ideas (front-to-back listening, side balance, mood-based, cover aesthetic).
- The technical clarifications about Spotify API previews being legal.
- The pushback against fetching everything.

### What I Changed or Rejected
- I have not yet decided whether to keep the Taobao link. Claude noted Taobao vinyl listings can be sketchy. I will research this before deciding.
- I dropped the "fetch as much as possible" instinct entirely. The catalog will now be curated, not comprehensive.

### What I Still Do Not Fully Understand
- The exact Spotify Web API auth flow (client credentials vs OAuth). I know one is simpler but I have not actually tried either.
- Whether the Spotify preview URLs are stable over time or whether they expire.

### My Next Step
Confirm with Claude which lane this project officially fits, then move toward writing a PRD.

---

## Entry 3

### Date
May 19, 2026

### AI Tool Used
Claude (Anthropic)

### What I Asked AI
"i like this idea. and i think it can practice me a lot of skills that i can use in future projects. back to the assignment, which lane this suits?"

### Why I Asked
I wanted explicit confirmation that the project fits Lane 4 before investing time in a PRD. I also wanted the reasoning, not just the answer, so I could use it to justify the project to my teacher.

### What AI Gave Me
A clear Lane 4 classification with five supporting reasons: it combines Lane 1 and Lane 2 skills with extra complexity, I have relevant prior project experience, the architecture is feasible, it avoids the forbidden ML zone, and the value proposition is defensible. Claude also gave me a one-sentence pitch I could use when justifying the project to my teacher.

### What I Used
All five justification points. They went almost directly into the "Why Lane 4" section of the PRD.

### What I Changed or Rejected
Nothing substantive at this step. This was a confirmation step, not a creative one.

### What I Still Do Not Fully Understand
Whether my teacher will accept "rule-based filtering over a curated taxonomy" as enough intelligence for Lane 4, or whether they will want something more algorithmic. This is a real open question I should raise in the PRD.

### My Next Step
Ask Claude to draft the full PRD in markdown.

---

## Entry 4

### Date
May 19, 2026

### AI Tool Used
Claude (Anthropic)

### What I Asked AI
"now write the prd forme in markdown format without using the — punctuation"

### Why I Asked
I had all the conceptual pieces but I wanted a structured PRD document I could iterate on, rather than building one from scratch. The em dash constraint was a stylistic preference (I find Claude overuses them and it makes the writing feel AI-generated).

### What I Used
The overall PRD structure (Problem, Target User, Goals/Non-Goals, Core Features, Technical Approach, Why Lane 4, Milestones, Success Criteria, Risks, Open Questions). The technical sections (data schema, copyright handling, stack choices) were accurate enough to keep mostly as written.

### What I Changed or Rejected
- I plan to rewrite Section 2 (Problem) and Section 7 (Why Lane 4) in my own voice, since Claude flagged that those would be the ones my teacher reads most carefully and they currently sound too polished for a student PRD.
- I need to revisit the catalog size promise (150 albums). After the MVP conversation, this feels ambitious.

### What I Still Do Not Fully Understand
Whether the four-week milestone plan is realistic given my AP exam schedule and other coursework. I should map it against my actual calendar.

### My Next Step
Ask Claude to scope the MVP, because the full PRD vision feels too big to start with.

---

## Entry 5

### Date
May 19, 2026

### AI Tool Used
Claude (Anthropic)

### What I Asked AI
"what would my mvp be"

### Why I Asked
I had a tendency to plan the full product and try to build it all at once, which usually results in nothing shipping. I wanted Claude to help me cut the scope aggressively so I could build a working version first and expand later.

### What AI Gave Me
A radically reduced MVP: 30 albums (not 150), only two filter dimensions (mood and runtime), no favorites, no localStorage, no Spotify preview embed, just outbound links to Spotify. Claude also gave me a clear "done" definition (a friend can apply two filters, see a few albums, click through to Spotify, and tell me whether the curation feels right) and a suggested build order for everything that comes after the MVP. Plus a warning that the curation work itself takes longer than expected (around 5 minutes per album), and a recommendation to do that work before writing any code.

### What I Used
The cut list almost in full. The MVP scope (30 albums, 2 filters, outbound link only) feels achievable.

### What I Changed or Rejected
I am not sure yet whether to do the 30-album tagging before or in parallel with the coding. Claude recommended before. I might do 10 first to see if I enjoy the process.

### What I Still Do Not Fully Understand
Whether 30 albums is enough for the filter results to feel useful. With only 30 albums and two filters of multiple values each, some filter combinations will return zero results, which could feel broken to a user.

### My Next Step
1. Update the PRD to reflect the MVP scope (or attach the MVP scope as a separate working note).
2. Start tagging 10 albums by hand and see how the curator-note format feels in practice.
3. Set up a Spotify Web API account and confirm I can fetch album metadata before committing further.
