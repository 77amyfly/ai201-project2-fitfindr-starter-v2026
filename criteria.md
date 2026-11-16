# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**

4 of 5 because my search is a plain keyword match and some phrasings will miss.
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**

5 of 5 because this is the code's job, not the model's: the same query always gives the same result.
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

---


## 3. The same item is passed through all three tools

Across queries whose first search result is a different listing each time, the `id` of `session["search_results"][0]`, the `id` of `session["selected_item"]`, and the `id` of the `new_item` received by `suggest_outfit` and by `create_fit_card` are all the same, in 5 of 5 tries.

**Why this target:**
5 of 5 because passing the item along is the code's job, not the model's: one mismatch means the loop picked or passed the wrong item. Both tools return strings with no `id`, so I record the `new_item` each one receives.
<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

---

## 4. The fit card gives the price and the platform

At least 4 of 5 fit cards, each for a different item, mention the item's price and its platform.

**Why this target:**
4 of 5 because the card is written by a model, which sometimes drops a detail.
<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

---

## 5. The price ceiling is respected

When a query includes a price ceiling, every listing returned has a price at or below it, in 5 of 5 tries.

**Why this target:**
5 of 5 because the price filter is plain code with no model in it, so one listing over the ceiling is a bug in the filter.

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

## Capstone criteria

**1. A fresh clone runs from RUNNING.md and can be used**

Following RUNNING.md once from a clean clone, `python test.py` shows 10 passed, and 10 of 10 queries of the tester's choice run to completion: the command prints a reply (a result or a message) and returns to the prompt.

Why this target: Being able to install and run the system is the precondition for anyone using it, so it has to work. It is 10 of 10 because this only tests installation and startup, with no model randomness, so a single failure means a real problem with a dependency or the MCP server.


**2. Every run leaves a complete log record**
In any 10 consecutive runs, whatever their outcome, `runs.jsonl` gains exactly 10 new lines, and every line contains all 10 keys (`ts`, `input`, `output`, `status`, `item_id`, `wardrobe_items`, `model_calls`, `prompt_tokens`, `output_tokens`, `ms`).


Why this target:
10 of 10 because the log is the only way I can diagnose a run after the fact, and a missing record is invisible: nothing shows that it is missing. The 10 runs are picked at random, so they can end in a result, in no results, or in an error, and the log has to be complete in all three cases.


**3. A run that finds a listing finishes within 4 seconds**

In 10 consecutive runs of queries that match at least one listing, and at least 9 seconds between runs so the rate limiter never pauses, the `ms` value in `runs.jsonl` is 4000 or less in at least 8 of the 10. `ms` covers the whole run, including starting the search server and both model calls.

Why this target:
4 seconds because this is a command-line tool someone waits at, and past about 4 seconds a person starts to wonder whether it has hung. It is 8 of 10 and not 10 of 10 because part of the time is the model service answering. 


**4. An empty query gets a message that asks for input**

For 5 empty or blank queries (for example `' '`, `'   '`, or a query with only a price like `'under $30'`), all 5 runs end without calling the model (`model_calls` is 0) and the terminal message tells the user to describe an item.


Why this target:
5 of 5 because an empty query is deterministic: the same input always gives the same result, so there is no randomness to excuse a miss. I picked this path because a blank query is the most likely mistake from someone using the tool for the first time, and today the message says `No listings matched ''`, which blames the search for something the user did not type. 

**5. A run that finds a listing makes exactly 2 model calls and uses 1000 tokens or fewer**
In 10 consecutive runs of queries that match at least one listing, a run passes if its `model_calls` is 2 and its `prompt_tokens` plus `output_tokens` is 1000 or less. At least 7 of the 10 runs must pass.


Why this target:
Exactly 2 calls because the loop has two model stages, `suggest_outfit` and `create_fit_card`, so any other number means a retry or a loop I did not intend. 1000 tokens because my measured average is 922, which leaves about 8% of room. It is 7 of 10 and not 10 of 10 because the length of what the model writes varies from run to run, and one of my measured runs was 1009. I allow 3 such runs, but not more, because then the typical run would be over budget.