"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
        {
        "name": "item passed through, item 1 (denim jacket)",
        "query": "denim jacket",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        "name": "item passed through, item 2 (cargo pants)",
        "query": "cargo pants",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        "name": "item passed through, item 3 (sneakers)",
        "query": "sneakers",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        "name": "item passed through, item 4 (leather jacket)",
        "query": "leather jacket",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        "name": "item passed through, item 5 (band tee)",
        "query": "band tee",
        "wardrobe": "example",
        "criterion": 3,
    },
        {
        "name": "fit card price+platfor, item 1 (denim jacket)",
        "query": "denim jacket",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "fit card price+platfor, item 2 (cargo pants)",
        "query": "cargo pants",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "fit card price+platfor, item 3 (sneakers)",
        "query": "sneakers",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "fit card price+platfor, item 4 (leather jacket)",
        "query": "leather jacket",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "fit card price+platfor, item 5 (band tee)",
        "query": "band tee",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "price ceiling 1 (denim jacket under $30)",
        "query": "denim jacket under $30",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        "name": "price ceiling 2 (sneakers under $40)",
        "query": "sneakers under $40",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        "name": "price ceiling 3 (leather jacket under $40)",
        "query": "leather jacket under $40",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        "name": "price ceiling 4 (band tee under $20)",
        "query": "band tee under $20",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        "name": "price ceiling 5 (cargo pants under $30)",
        "query": "cargo pants under $30",
        "wardrobe": "example",
        "criterion": 5,
    },
    # TODO: add what your criteria 3, 4 and 5 need.
    #
    # Set "criterion" to the number in criteria.md that the scenario tests.
    # "criterion": None means a diagnostic run — useful to have, but it isn't
    # one of your five, and run_eval.py marks it as such in the table.
    #
    # For a state criterion, any normal query works — what you're checking is
    # what ends up in the session, not what the user typed.
    #
    # For a fit-card criterion, you probably want the SAME query listed more
    # than once, or several different items, depending on what your criterion
    # actually says.
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
