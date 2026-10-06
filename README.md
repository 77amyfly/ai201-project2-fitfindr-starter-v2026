# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

FitFindr is a thrifting assistant. A user describes what they want in plain language, such as "a vintage graphic tee under $30, size M", and the agent searches the listings for matches. It then works out what the best match would go with, using the user's existing wardrobe if they have one, and writes a short caption for the find. The user gets back the matching listing, an outfit idea built around it, and a caption they could post or save.
<!-- Three or four sentences: what a user asks for, and what they get back. -->

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Finds listings that matching a description, and optionally a size and a price ceiling.
- **Inputs:** `description` (str), `size` (str or None), `max_price` (float or None). `None` means don't filter on that input. A size matches when it equals one of the parts of the listing's size, ignoring case, where the size is split on `/` and spaces ("M" matches "S/M" and "M/L" but not "US 9" or "W30 L30").
- **Returns:** A list of listing dicts, best keyword match first. Each dict has `id` (str), `title` (str), `description` (str), `category` (str), `style_tags` (list of str), `size` (str), `condition` (str), `price` (float), `colors` (list of str), `brand` (str or None), `platform` (str).
- **When it has nothing:** Returns an empty list `[]`.


### `suggest_outfit`

- **What it does:** Suggests one or two outfits that combine the thrifted item with the user's wardrobe.
- **Inputs:** `new_item` (dict, first listing dict from search_listings), `wardrobe` (dict with an `items` key holding a list of dicts, each with `id` (str), `name` (str), `category` (str), `colors` (list of str), `style_tags` (list of str), `notes` (str or None))
- **Returns:** A non-empty string with one or two outfit suggestions, naming the wardrobe pieces by their `name`.
- **When it has nothing:** If `wardrobe["items"]` is empty, returns a non-empty string of general styling advice for `new_item`, without naming any wardrobe pieces.


### `create_fit_card`

- **What it does:** Writes a short caption someone would post about the find, using the item and the outfit suggestion.
- **Inputs:** `outfit` (str, the string returned by suggest_outfit), `new_item` (dict, first listing dict from search_listings)
- **Returns:** A string of two to four sentences, written like a real post rather than a product description, that mentions the item, its `price` and its `platform` once each, and is specific about the vibe.
- **When it has nothing:** If `outfit` is empty or only whitespace, still returns a caption, and for how to wear the item it gives general styling advice based on `new_item` , without naming any wardrobe pieces.
---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns [], put a message in `session["error"]` that names what the user could change (the price limit, the size, or the keywords), leave `session["fit_card"]` as `None`, and stop. Otherwise put the first result in `session["selected_item"]` and go to `suggest_outfit`, then `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex<!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** `parsed` (description, size, max_price) → `search_results` → `selected_item` → `outfit_suggestion` → `fit_card`.<!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$    python app.py ask 'vintage graphic tee under $30'

Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Outfit 1: Pair the Y2K Baby Tee — Butterfly Print with your Baggy straight-leg jeans, dark wash and Chunky white sneakers. Add the Black crossbody bag for an easy, streetwear-inspired look that highlights the fitted crop of the top against the loose denim. 

Outfit 2: Style the tee with your Wide-leg khaki trousers and complete the outfit using the Black cropped zip hoodie thrown over top. Finish with your Black combat boots to mix Y2K sweetness with a slightly grungier edge.

  Fit card: Found this cute little butterfly tee on depop for only $18 and I am obsessed. It is giving major early 2000s mallrat energy, especially paired with baggy dark wash jeans and chunky white sneakers. Can not wait to wear it all spring.
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033','title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'],'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015','title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on thechest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

**Outfit 1: Casual Streetwear**
Pair the Vintage Levi's 501 Jeans with the white ribbed tank top layered under the black cropped zip hoodie. Add the chunky white sneakers and the black crossbody bag for an effortless, everyday look.

**Outfit 2: Vintage Layered**
Style the Vintage Levi's 501 Jeans with the oversized grey crewneck sweatshirt worn over the white ribbed tank top. Cinch the jeans with the brown leather belt and finish with the black combat boots and the vintage black denim jacket for a textured, vintage-inspired outfit.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Finally scored the holy grail of denim on depop and my life is officially complete. These vintage 501s have that exact lived-in medium wash and knee fading that looks like they were broken in for decades. For $38, they were an absolute steal and look so good just thrown on with crisp white sneakers and a beat-up tee.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**


- *What I asked for:* My first test of `search_listings('graphic tee', max_price=30)` returned items that weren't graphic tees, including cargo pants (`lst_011`). I asked Claude to work out why.
- *What came back:* Claude said the keyword matching was a plain substring check across `title`, `description` and `style_tags`, so words inside a listing's `description` could match by accident. 
- *What I changed:* I removed `description` from the text the search matches against and added `colors`, so it now matches on `title`, `colors` and `style_tags`. Running the same query again returned only graphic tees and a graphic hoodie.

**Moment 2**

- *What I asked for:* For the "How the query is parsed" part of my README, I asked Claude to compare the three options (regex, string splitting, asking the model) and say which was better. I had been leaning toward the model.
- *What came back:* A comparison table. Claude said regex was the best fit for my project: it gives the same result every time, which my criterion 2 (an impossible query stops, 5 of 5) depends on, it adds no model call to a run that already makes two, and the example queries all use a fixed pattern like "under $30" and "size M". It said the model would handle looser phrasing but could parse the same sentence differently on different runs.
- *What I changed:* I dropped the model option and wrote the parsing with regex in `agent.py`. 


<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
