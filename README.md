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


**Moment 3 (unit 4)**

- *What I asked for:* How to improve the accuracy of search_listings, for example by giving different matching words different weights.
- *What came back:* Claude suggested several fixes (a category map, extra weight for title matches, whole-word matching) and explained the new problems each one would bring.
- *What I changed:* Nothing in the search. I decided that a code-only fix always trades one problem for another, and that a real fix would need a model call to parse the query, which was too complex. So I dropped that direction and used my one improvement on price parsing instead.

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
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. The same item is passed through all three tools | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. The fit card gives the price and the platform | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. The price ceiling is respected | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |


**Real output from one try**, pasted as text, naming the file and function
that produced it:


**Criterion 1** — "matching query completes", Try 1. Loop: `agent.py::run_agent`; fit card: `tools.py::create_fit_card`.

```
Fit card:

scored this little butterfly baby tee on depop for just $18 and I am obsessed with the early 2000s energy. honestly considering pairing it with my baggy dark wash jeans and chunky sneakers for the ultimate nostalgic street fit, or maybe styling it with khaki trousers and a black jacket for a more grounded vibe. either way, it is giving total mall run nostalgia and I cannot wait to wear it everywhere.

Trace:

[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    first result id=lst_002
[2] suggest_outfit
      in:  item id=lst_002 ('Y2K Baby Tee — Butterfly Print'), wardrobe items=10
      out: Outfit 1: Pair the Y2K Baby Tee — Butterfly Print with your Baggy straight-leg jeans, dark wash for a classic …
[3] create_fit_card
      in:  outfit=<524 chars>, item id=lst_002 ('Y2K Baby Tee — Butterfly Print')
      out: scored this little butterfly baby tee on depop for just $18 and I am obsessed with the early 2000s energy. hon…
```

**Criterion 2** — "impossible query stops early", Try 1. Produced by `agent.py::run_agent`.

```
- stopped early: yes — No listings matched 'designer ballgown' in size XXS under $5. Try raising the price limit, removing the size, searching for just the type of item, like 'dress'.
- selected_item: (none)
- search_results: 0

Trace:

[1] search_listings (via MCP)
      in:  description='designer ballgown', size=XXS, max_price=5.0
      out: [] (empty)
[2] branch: no results
      →    stopping before suggest_outfit; fit_card stays None
```

**Criterion 3** — "item passed through, item 1 (denim jacket)", Try 1. Produced by `agent.py::run_agent` via `trace.step()`.

```
[1] search_listings (via MCP)
      in:  description='denim jacket', size=None, max_price=None
      out: 6 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +3 more
      →    first result id=lst_007
[2] suggest_outfit
      in:  item id=lst_007 ('Denim Jacket — Light Wash, Cropped'), wardrobe items=10
      out: Outfit 1: Pair the Denim Jacket — Light Wash, Cropped with the White ribbed tank top, Baggy straight-leg jeans…
[3] create_fit_card
      in:  outfit=<411 chars>, item id=lst_007 ('Denim Jacket — Light Wash, Cropped')
      out: Scored this vintage Wrangler cropped denim jacket on Poshmark for only $42 and it instantly became the centerp…
```

**Criterion 4** — "fit card price+platfor, item 1 (denim jacket)", Try 1. Produced by `tools.py::create_fit_card`. The card contains the price `$42` and the platform `Poshmark`.

```
Scored this cropped Wrangler denim jacket on Poshmark for only $42 and I am obsessed with the boxy shoulders. Threw it on over a ribbed tank and some dark wash baggies for the ultimate double-denim streetwear look. It is basically the best blank canvas for a few patches, but honestly I love the plain light wash just as it is.
```

**Criterion 5** — all five queries. Produced by `tools.py::search_listings`, run directly in the terminal (not in `results/`), because the run log only shows the first result's price. Command shape: `python -c "from tools import search_listings; print([(r['title'], r['price']) for r in search_listings('<query>', max_price=<limit>)])"`

```
denim jacket, max_price=30:
[('High-Waisted Denim Shorts — Cutoff', 24.0), ('Straight Leg Black Jeans — Faded', 30.0), ('Denim Vest — Medium Wash, Studded', 27.0)]

sneakers, max_price=40:
[('Low-Top Canvas Sneakers — Off-White', 20.0)]

leather jacket, max_price=40:
[('Leather Belt — Brown, Braided', 12.0), ('Mini Shoulder Bag — Tan Leather', 38.0)]

band tee, max_price=20:
[('Vintage Band Tee — Faded Grey', 19.0), ('Y2K Baby Tee — Butterfly Print', 18.0)]

cargo pants, max_price=30:
[('Low-Rise Cargo Pants — Khaki', 27.0)]
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
| 1 | A matching query completes all three tools | 4 of 5 | MET | 5 of 5 tries had stopped early: no and returned a fit card. |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET | 5 of 5 tries stopped early: yes with a message naming what to change; trace had 2 steps and 0 model calls. |
| 3 | The same item is passed through all three tools | 5 of 5 | MET | For all 5 items (lst_007, lst_011, lst_019, lst_004, lst_006) the id in the search step, suggest_outfit and create_fit_card matched, in all 5 runs of each (25 runs). |
| 4 | The fit card gives the price and the platform | 4 of 5 | MET | All 25 cards (5 items x 5 runs) contained the item's price and its platform name (case ignored). |
| 5 | The price ceiling is respected | 5 of 5 | MET | Every listing returned for the 5 capped queries was at or below the ceiling; one was exactly $30 at a $30 ceiling. |

**Diagnoses**
No criterion was missed, so there is no miss to diagnose. I do not think that means the agent is solid. It means my targets were easy to meet.

- **Criterion 1 never tested its own reason.** I gave 4 of 5 because "some phrasings will miss", but I ran one query five times. Search is plain code, so five runs return the same results. I would tighten it to five different phrasings of the same request, such as "graphic tee", "band shirt" and "vintage t-shirt".
- **Criteria 3 and 5 are plain code**, so 5 of 5 was always likely. They guard against future regressions more than they test anything now.
- **A search problem my criteria did not see.** The first result is often not what the user asked for: "leather jacket" returned a track jacket, "leather jacket under $40" returned a belt, and "denim jacket under $30" returned denim shorts. Keyword matching scores a listing if any one word of the query appears in it. Every criterion still passed. This is a tool problem (search_listings), and a criterion such as "the first result's category matches the item asked for" would have caught it.
- **A measurement gap.** run_eval.py records only the first result's price, so criterion 5 could not be scored from the run log. I called search_listings directly to see every returned price.


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
python app.py ask 'vintage graphic tee under $30' --trace                

[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit
      in:  item='Y2K Baby Tee — Butterfly Print', wardrobe items=10
      out: Outfit 1: Pair the Y2K Baby Tee — Butterfly Print with your Baggy straight-leg jeans, dark wash for a classic …
[3] create_fit_card
      in:  outfit=<576 chars>, item='Y2K Baby Tee — Butterfly Print'
      out: scored this vintage butterfly baby tee on depop for only $18 and it is honestly the ultimate 2000s mood. i lov…

```


**Empty search** 
```
python app.py ask 'GMC Yukon' --trace                

[1] search_listings (via MCP)
      in:  description='GMC Yukon', size=None, max_price=None
      out: [] (empty)
[2] branch: no results
      →    stopping before suggest_outfit; fit_card stays None

```



**On the MCP move:** 
In mcp_server.py I registered search_listings with @mcp.tool(); its docstring states the size-matching rule, the price unit (US dollars), and that it returns [] when nothing matches. In agent.py I replaced the direct call with call_tool("search_listings", {...}) and removed search_listings from the tools import.

Nothing behaved differently: the same query gave the same Found line before and after ("Y2K Baby Tee — Butterfly Print — $18.0 on depop"), and the price stayed a float.
<!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

In `agent.py::run_agent`, the price parsing only. Nothing else was touched.

- **Number-first phrasings.** The original regex only found a limit when the keyword came before the number ("under $20", "up to 30"). I added a second pattern, tried only when the first finds nothing, for "20 dollars max", "$20 or less" and "20 bucks or under".
- **Currency words.** `dollars`, `bucks`, `dollors` and `usd` are now removed from the description.

**Which failure it was meant to fix:**

The price limit was silently dropped. Before the change, "20 dollars max" and "$20 or less" both parsed to `max_price=None`, so the agent searched with no ceiling and returned 3 and 10 results. The user's budget was ignored with no message.

Criterion 5 did not catch this because every criterion 5 scenario used "under $N".

I found it while checking search quality. I ruled out other candidates first (a category map, title weighting, whole-word matching) because each had problems of its own.

The currency words were also left in the description in the baseline, but that did not change the search results, so it is a side cleanup and not the main reason.


### Baseline (before the change)

Each query was run with `python app.py ask '...' --trace`. The `zzzz` prefix guarantees no match, so there are 0 model calls. Only the `in:` line matters.

```
'zzzz under $20'         in:  description='zzzz', size=None, max_price=20.0
'zzzz under 20 dollars'  in:  description='zzzz dollars', size=None, max_price=20.0
'zzzz under 20 bucks'    in:  description='zzzz bucks', size=None, max_price=20.0
'zzzz 20 dollars max'    in:  description='zzzz 20 dollars max', size=None, max_price=None
'zzzz under 5dollors'    in:  description='zzzz dollors', size=None, max_price=5.0
'zzzz $20 or less'       in:  description='zzzz 20 or less', size=None, max_price=None
```



### Run Log — After

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all three tools | 4 of 5 | MET | 5 of 5 tries had stopped early: no and returned a fit card. |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET | 5 of 5 tries stopped early: yes with a message naming what to change; trace had 2 steps and 0 model calls. |
| 3 | The same item is passed through all three tools | 5 of 5 | MET | For all 5 items (lst_007, lst_011, lst_019, lst_004, lst_006) the id in the search step, suggest_outfit and create_fit_card matched, in all 5 runs of each (25 runs). |
| 4 | The fit card gives the price and the platform | 4 of 5 | MET | All 25 cards (5 items x 5 runs) contained the item's price and its platform name (case ignored). |
| 5 | The price ceiling is respected | 5 of 5 | MET | Every listing returned for the 5 capped queries was at or below the ceiling; one was exactly $30 at a $30 ceiling. |

Each query was run with `python app.py ask '...' --trace`. The `zzzz` prefix guarantees no match, so there are 0 model calls. Only the `in:` line matters.
```
'zzzz under $20'         in:  description='zzzz', size=None, max_price=20.0
'zzzz under 20 dollars'  in:  description='zzzz', size=None, max_price=20.0
'zzzz under 20 bucks'    in:  description='zzzz', size=None, max_price=20.0
'zzzz 20 dollars max'    in:  description='zzzz', size=None, max_price=20.0
'zzzz under 5dollors'    in:  description='zzzz', size=None, max_price=5.0
'zzzz $20 or less'       in:  description='zzzz', size=None, max_price=20.0
```

**Did it help, and how do I know:**

Yes. The agent now recognizes price limits written with the number first,
like "20 dollars max" and "$20 or less". Before the change both were read as
having no limit (max_price=None). Now both give max_price=20.0.

Phrasings that already worked, like "under $20", behave the same as before.

The after run log is identical to the before one. That is expected: all 18
scenarios use "under $N", so they could not show this change. They only
confirm that nothing broke.
---

## What's Still Broken
search ranking is still weak. search_listings keeps a listing if any one word of the query matches, so "leather jacket" returns a track jacket first, and "leather jacket under $40" returns a belt first.

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


<!-- ═══════════════════════ Capstone ═══════════════════════ -->

## Capstone

## Capstone

**What This Extends**

FitFinder, my Project 2 agent (search listings, suggest outfits, write a fit
card). The extension is the operational layer: the run path, the
instrumentation, and the numbers that come out of it. Concretely, that means a
one-command local run path, structured logging of every run, and a measured
cost per run.

**The Shape**

Shape A (deploy and instrument), local run (Path B). Out of scope: no new
features, no new interface, no changes to the retrieval strategy.

**Running It**

Path B, local with logs. The start command and environment are in
RUNNING.md. I tested it from a fresh `git clone` into a new folder, following
RUNNING.md line by line: `python test.py` passed (10 passed, 0 failed) and
`python app.py ask 'vintage graphic tee under $30'` ran all three stages and
wrote a log record.

**Instrumentation**

`run_agent()` in `agent.py` is a thin wrapper around the original loop
(`_run_agent`). It times the run and writes one JSON line to `runs.jsonl`
through `runlog.py::log_run`, in a `finally` block, so a run that crashes is
recorded too. Each record holds:

- `ts`: UTC timestamp
- `input`: the user's query
- `output`: the fit card, or the error message when the run did not succeed
- `status`: `ok`, `no_results` (the empty-search branch) or `error` (an exception)
- `item_id`: the listing the agent selected, or null
- `wardrobe_items`: how many wardrobe items the run had
- `model_calls`, `prompt_tokens`, `output_tokens`: what this run used, taken
  from `generate.py`'s counters
- `ms`: end-to-end time of the run

The first entry below is a failed run: I set a wrong API key for one command
(`GEMINI_API_KEY=wrong_key python app.py ask '...'`) to confirm that a crash
leaves a record. The other ten are the cost-measurement runs from
`measure_cost.py`.

```
{"ts": "2026-11-16T04:56:49+00:00", "input": "denim jacket under $50", "status": "error", "output": "ModelUnavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.", "item_id": null, "wardrobe_items": 10, "model_calls": 1, "prompt_tokens": 0, "output_tokens": 0, "ms": 1904}
{"ts": "2026-11-16T04:58:16+00:00", "input": "vintage graphic tee under $30", "status": "ok", "output": "Still not over scoring this butterfly baby tee on depop for only $18. I am leaning all the way into the early 2000s energy by pairing it with baggy dark wash jeans and chunky white sneakers for an easy streetwear vibe. Or, honestly, it looks just as good toughened up with wide-leg khakis and combat boots.", "item_id": "lst_002", "wardrobe_items": 10, "model_calls": 2, "prompt_tokens": 755, "output_tokens": 196, "ms": 3313}
{"ts": "2026-11-16T04:58:27+00:00", "input": "90s track jacket in size M", "status": "ok", "output": "Found the ultimate vintage Champion track jacket on poshmark and I am completely obsessed with the navy and white stripes. I threw it on over a ribbed tank and baggy jeans today for the most effortless 90s streetwear vibe. Scoring this lightweight piece for just $45 feels like an absolute steal for my transitional wardrobe.", "item_id": "lst_004", "wardrobe_items": 10, "model_calls": 2, "prompt_tokens": 731, "output_tokens": 177, "ms": 2059}
{"ts": "2026-11-16T04:58:38+00:00", "input": "silk slip dress in midi length under $40", "status": "ok", "output": "Found this dreamy floral midi slip on depop for just $30 and I am obsessed. The 90s indie sleaze vibe is unmatched when you layer it over a basic white tank and beat-up blackcombat boots. For chill days, throwing an oversized grey crewneck right over it gives the ultimate grungy-cozy contrast.", "item_id": "lst_013", "wardrobe_items": 10, "model_calls": 2, "prompt_tokens": 794, "output_tokens": 215, "ms": 2306}
{"ts": "2026-11-16T04:58:49+00:00", "input": "platform sneakers size 8", "status": "ok", "output": "Score for the outfit today was finding these white chunky platform sneakers on poshmark for only $48. They have such a good late nineties vibe with the velcro straps and look so cool with wide leg khakis and a black zip hoodie. Just a little bit of yellowing on the soles, but honestly it just makes them look more authentic.", "item_id": "lst_019", "wardrobe_items": 10, "model_calls": 2, "prompt_tokens": 734, "output_tokens": 169, "ms": 1955}
{"ts": "2026-11-16T04:59:00+00:00", "input": "denim jacket under $50", "status": "ok", "output":"Still pinching myself over finding this vintage Wrangler cropped denim jacket on poshmark for only $42. The structured shoulders give it the absolute best 90s streetwear vibe, especially when thrown over a white tank and baggy dark-wash jeans for that contrast double-denim look. It is basically a blank canvas, so now I just have to decide whether to load it up with pins or leave it classic.", "item_id": "lst_007", "wardrobe_items": 10, "model_calls": 2, "prompt_tokens": 721, "output_tokens": 192, "ms": 2001}
{"ts": "2026-11-16T04:59:11+00:00", "input": "vintage graphic tee under $30", "status": "ok", "output": "scored this absolute dream of a butterfly baby tee on depop for just $18 and i am obsessed. i have it styled with some baggy dark wash jeans and chunky sneakers today for the ultimate 2000s street style moment. it has that perfect fitted crop and the colors are even better in person.", "item_id": "lst_002", "wardrobe_items": 10, "model_calls": 2, "prompt_tokens": 746, "output_tokens": 178, "ms": 1946}
{"ts": "2026-11-16T04:59:23+00:00", "input": "90s track jacket in size M", "status": "ok", "output": "Finally hunted down the ultimate 90s streetwear piece for $45 on poshmark and I am so obsessed. Just threw it on over a ribbed tank and baggy dark wash jeans with my chunky sneakers for that effortless athletic vibe. Might switch it up tomorrow with wide-leg khakis and a brown belt for the absolute best mix of retro and earth tones.", "item_id": "lst_004", "wardrobe_items": 10, "model_calls": 2, "prompt_tokens": 720, "output_tokens": 175, "ms": 3181}
{"ts": "2026-11-16T04:59:34+00:00", "input": "silk slip dress in midi length under $40", "status": "ok", "output": "Scored this gorgeous floral midi slip dress on depop for only $30 and I am obsessed. I threw it on under an oversized grey crewneck and chunky sneakers for the ultimate cozy streetwear fit. It has that effortless 90s vibe that I live for.", "item_id": "lst_013", "wardrobe_items": 10, "model_calls": 2, "prompt_tokens": 755, "output_tokens": 162, "ms": 1949}
{"ts": "2026-11-16T04:59:45+00:00", "input": "platform sneakers size 8", "status": "ok", "output": "Finally scored these chunky velcro platform sneakers on poshmark for $48 and I am obsessed with the y2k energy. They look so good with my baggy dark wash jeans, a ribbed tank, and a black denim jacket for that ultimate 90s streetwear look. The slight sole yellowing just makes them look authentically vintage.", "item_id": "lst_019", "wardrobe_items": 10, "model_calls": 2, "prompt_tokens": 726, "output_tokens": 159, "ms": 1682}
{"ts": "2026-11-16T04:59:56+00:00", "input": "denim jacket under $50", "status": "ok", "output":"Finally tracked down the ultimate boxy Wrangler jacket on poshmark for $42 and my 90s streetwear dreams are officially complete. The cropped cut is so good for throwing over a baggy grey crewneck and khaki trousers without drowning in fabric. It is basically the ultimate blank canvas and I cannot wait to live in this all spring.", "item_id": "lst_007", "wardrobe_items": 10, "model_calls": 2, "prompt_tokens": 732, "output_tokens": 188, "ms": 1913}
```

**What It Costs**

Measured with `measure_cost.py`: 10 runs (5 queries, each twice), cache off
(`AI201_CACHE=0`), 9 seconds between runs to stay under the 15 requests per
minute limit. All 10 returned `ok`, and every run made exactly 2 model calls,
so no run was served from cache or retried.

| Measure | Average per run |
|---|---|
| Model calls | 2.0 |
| Prompt tokens | 741 |
| Output tokens | 181 |
| Total tokens | 922 |
| Time | 2.23 s |

I run on the Gemini free tier, so the money spent was $0. I report cost as
tokens and seconds because those are what I measured. I did not convert
tokens to dollars because I did not look up the current price.

For 100 people a day, assuming one run each:

- Tokens: 100 × 741 = 74,100 prompt + 100 × 181 = 18,100 output = 92,200 tokens
- Model calls: 100 × 2 = 200 calls
- Compute time: 100 × 2.23 s = 223 s, about 3.7 minutes

A run that finds nothing makes no model calls (the branch stops before
`suggest_outfit`).


**Run Log and Verdicts**

Before the improvement. Each cell is the number of runs that passed.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. A fresh clone runs from RUNNING.md and can be used | `test.py` shows 10 passed, 10 of 10 queries complete | 10/10 | 10/10 | 10/10 | MET |
| 2. Every run leaves a complete log record | 10 of 10 lines with all 10 keys | 10/10 | 10/10 | 10/10 | MET |
| 3. A run that finds a listing finishes within 4 seconds | at least 8 of 10 at 4000 ms or less | 10/10 | 10/10 | 10/10 | MET |
| 4. An empty query gets a message that asks for input | 5 of 5 | 0/5 | 0/5 | 0/5 | MISSED |
| 5. 2 model calls and 1000 tokens or fewer | at least 8 of 10 pass | 10/10 | 10/10 | 10/10 | MET |

Real output from trial 1 of each criterion:

**Criteria 3 and 5**: `results/capstone_trial1.jsonl`, written by
`agent.py::run_agent` through `runlog.py::log_run`.

```
{"ts": "2026-11-16T06:05:26+00:00", "input": "vintage graphic tee under $30", "status": "ok", "output": "scored this absolute dream of a butterfly baby tee on depop for just $18 and I am never takingit off. It gives major early 2000s mall rat energy, especially paired with baggy dark wash jeans and chunky sneakers. If it gets chilly, I am just throwing on a black cropped zip hoodie and calling it a day.", "item_id": "lst_002", "wardrobe_items": 10, "model_calls": 2, "prompt_tokens": 755, "output_tokens": 194, "ms": 2872}
{"ts": "2026-11-16T06:05:38+00:00", "input": "90s track jacket in size M", "status": "ok", "output": "Scored this vintage Champion track jacket on poshmark and I am completely obsessed with the navy and white contrast. For $45, it is honestly the ultimate layering piece to throw over baggy denim and chunky sneakers for an effortless 90s streetwear vibe. I can also totally dress it up with khaki trousers for that retro-athletic look.", "item_id": "lst_004", "wardrobe_items": 10, "model_calls": 2, "prompt_tokens": 719, "output_tokens": 171, "ms": 3052}
```

**Criterion 2**: `results/capstone_c2_trial1.jsonl`, same writer. Line 3 is a
run with no results (`status: "no_results"`), and line 4 is a run with an
invalid API key (`status: "error"`).

```
{"ts": "2026-11-16T06:13:19+00:00", "input": "vintage graphic tee under $30", "status": "ok", "output": "scored this little butterfly baby tee on depop for only $18 and I am obsessed with the early 2000s energy. honestly looks so good with dark wash baggy jeans and chunky white sneakers for the ultimate nostalgic streetwear vibe. can also totally picture wearing it with wide-leg khakis and a black denim jacket when it gets chilly out.", "item_id": "lst_002", "wardrobe_items": 10, "model_calls": 2, "prompt_tokens": 735, "output_tokens": 175, "ms": 2720}
{"ts": "2026-11-16T06:13:27+00:00", "input": "90s track jacket in size M", "status": "ok", "output": "Found this vintage Champion track jacket on poshmark and it is officially the holy grail of my lazy outfit days. I threw it on over a white ribbed tank and some baggy dark wash denim, and suddenly I look like I actually tried to put together a streetwear fit. For only $45, the navy and white stripes give off the exact effortless 90s athletic energy I have been hunting for.", "item_id": "lst_004", "wardrobe_items": 10, "model_calls": 2, "prompt_tokens": 732, "output_tokens": 195, "ms": 2274}
{"ts": "2026-11-16T06:13:32+00:00", "input": "designer ballgown size XXS under $5", "status": "no_results", "output": "No listings matched 'designer ballgown' in size XXS under $5. Try raising the price limit, removing the size, searching for just the type of item, like 'dress'.", "item_id": null, "wardrobe_items": 10, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "ms": 392}
{"ts": "2026-11-16T06:13:38+00:00", "input": "denim jacket under $50", "status": "error", "output": "ModelUnavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.", "item_id": null, "wardrobe_items": 10, "model_calls": 1, "prompt_tokens": 0, "output_tokens": 0, "ms": 780}
```

**Criterion 4**: `results/capstone_c4_trial1.txt`. The message is produced by
the empty-result branch in `agent.py::_run_agent`. The five lines are the
messages for `' '`, `'   '`, `'under $30'`, `'under $50'` and `'size M'`.

```
  No listings matched ''. Try searching for just the type of item, like 'dress'.
  No listings matched ''. Try searching for just the type of item, like 'dress'.
  No listings matched '' under $30. Try raising the price limit, searching for just the type of item, like 'dress'.
  No listings matched '' under $50. Try raising the price limit, searching for just the type of item, like 'dress'.
  No listings matched '' in size M. Try removing the size, searching for just the type of item, like 'dress'.
```

**Criterion 1**: run in a fresh clone (`fitfinder-test`), following RUNNING.md.
`python test.py` printed `10 passed, 0 failed, 0 to look at, 0 skipped`, and
all 10 queries ran to completion in each of the 3 trials.

**Diagnosis**

Criteria 1, 2, 3 and 5 were met. Criterion 4 was missed in all 3 trials, 0 of 5
each time, and the five failures are one problem, not five.

The stage is the query parsing in `agent.py::_run_agent`, together with the
empty-result branch right after it. The mechanism: for `' '`, `'   '`,
`'under $30'`, `'under $50'` and `'size M'`, the regexes remove the price and
the size, and what is left is an empty `description`. Nothing checks for that.
The empty string goes to `search_listings`, which splits it into zero keywords,
so every listing scores 0 and the result is an empty list. The loop then takes
the no-results branch and builds its message from `parsed['description']`,
which gives `No listings matched ''`. The trace shows this directly:
`in: description=''` followed by `out: [] (empty)`. The model is not involved,
since `model_calls` was 0 in every run. The message is wrong because the input
was never validated, not because the search failed.

**The Improvement**



**What's Still Broken**

**How I Used AI**

