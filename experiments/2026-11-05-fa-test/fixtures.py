"""Write the fixture projects A, B, C, D1 and D2 into fixtures/<name>/.

A fictional product: a tool that logs climbing sessions and suggests what to train
next. Each fixture is frozen just before the behaviour it tests. `steps.yaml` holds
the placeholder commit 0000000, which the rig replaces with the fixture's own commit.
Every fixture but A has a one-line CLAUDE.md; the baseline runs without it.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "fixtures")
P = ".datum/model/product"
SE = P + "/suggest-engine"


def closed(*steps):
    return "".join(f"{s}: {{closed_at: \"0000000\"}}\n" for s in steps) or "{}\n"


ELI = """id: ELI-2Q7M
date: 2026-10-01
entries:
  - n: 1
    question: What problem does this solve for you?
    answer: "I forget what I did last time, so I repeat the same routes."
    need: true
  - n: 2
    question: What do you want it to do about that?
    answer: "Tell me what to train next, without paying a coach."
    need: true
  - n: 3
    question: Where do you use it?
    answer: "I log on my phone at the gym and look at it on my laptop at home. The gym has bad signal."
    need: true
  - n: 4
    question: What is the worst thing it could do to you?
    answer: "Lose my history. That's years of sessions I can't get back."
    loss: true
"""
SEASON = """  - n: 5
    question: Anything else you want from it?
    answer: "I'd like to see how my grades move over a season."
    need: true
"""
SEASON_OUT = SEASON + "    out_of_scope: The builder wants the log and the suggestion first.\n"
INJURY = """  - n: 6
    question: Could it hurt you?
    answer: "If it tells me to do too much, yes. I've had finger injuries from overdoing it."
    loss: true
"""

B = {
    f"{P}/steps.yaml": closed(),
    f"{P}/analysis/ELI-2Q7M.yaml": ELI,
    f"{P}/analysis/SCN-4H8R.yaml": """id: SCN-4H8R
status: agreed
name: Log a session at the gym
kind: main
trigger: The climber starts a session at the gym.
steps:
  - {n: 1, by: climber, what: "Adds each route tried, its grade and whether it was sent."}
  - {n: 2, by: product, what: Records the session.}
  - {n: 3, by: climber, what: Opens the log on their laptop at home.}
  - {n: 4, by: product, what: Shows the same session there.}
outcome: The session is in the log on every device.
needs: [ELI-2Q7M#3]
""",
    f"{P}/analysis/SCN-6MBD.yaml": """id: SCN-6MBD
status: agreed
name: Look back before a session
kind: main
trigger: The climber wants to know what they did last time.
preconditions: At least one session is logged.
steps:
  - {n: 1, by: climber, what: Asks to see their recent sessions.}
  - {n: 2, by: product, what: Shows the recent sessions and the routes in them.}
outcome: The climber knows what they did last time.
needs: [ELI-2Q7M#1]
""",
    f"{P}/analysis/SCN-9W2E.yaml": """id: SCN-9W2E
status: agreed
name: Get the next training suggestion
kind: main
trigger: The climber asks what to train.
preconditions: At least one session is logged.
steps:
  - {n: 1, by: climber, what: Asks what to train next.}
  - {n: 2, by: product, what: "Suggests what to train, with the reason, from their recent sessions."}
outcome: The climber has a suggestion and knows why.
needs: [ELI-2Q7M#2]
""",
    f"{P}/analysis/SCN-2KVT.yaml": """id: SCN-2KVT
status: agreed
name: Log with no signal
kind: failure
trigger: The climber logs a session while the phone has no signal.
steps:
  - {n: 1, by: climber, what: Adds the routes as usual.}
  - {n: 2, by: product, what: Records the session on the phone.}
  - {n: 3, by: product, what: Brings the session to the other devices once the phone has signal.}
outcome: No session is lost and the log catches up by itself.
needs: [ELI-2Q7M#3]
""",
}

FUNCTIONS = {
    f"{P}/functions/FUN-3G1N.yaml": """id: FUN-3G1N
status: agreed
name: Record a session
definition: Keeps the routes a climber tried, with their grades and outcomes, as one session.
serves: [SCN-4H8R#2, SCN-2KVT#2]
""",
    f"{P}/functions/FUN-9PRJ.yaml": """id: FUN-9PRJ
status: agreed
name: Show past sessions
definition: Shows the climber their recent sessions and the routes in them.
serves: [SCN-6MBD#2]
""",
    f"{P}/functions/FUN-7SGT.yaml": """id: FUN-7SGT
status: agreed
name: Suggest what to train next
definition: Proposes what the climber should train next, with the reason, from their recent sessions.
serves: [SCN-9W2E#2]
""",
    f"{P}/functions/FUN-5YNC.yaml": """id: FUN-5YNC
status: agreed
name: Bring sessions to every device
definition: Makes a session recorded on one of the climber's devices appear on the others.
serves: [SCN-4H8R#4, SCN-2KVT#3]
""",
}

# As B with functions, no losses or hazards written, and need 5 in no scenario.
C = dict(B)
C.update(FUNCTIONS)
C[f"{P}/analysis/ELI-2Q7M.yaml"] = ELI + SEASON

# The product closed through cases, the child not started.
D = dict(B)
D.update(FUNCTIONS)
D.update({
    f"{P}/steps.yaml": closed("functional-analysis", "requirements", "synthesis", "design-evaluation", "cases"),
    f"{P}/analysis/ELI-2Q7M.yaml": ELI + SEASON_OUT + INJURY,
    f"{P}/analysis/LOS-8D2F.yaml": """id: LOS-8D2F
status: agreed
statement: The climber's training history is lost.
to: [user]
from: [ELI-2Q7M#4]
""",
    f"{P}/analysis/LOS-6TWR.yaml": """id: LOS-6TWR
status: agreed
statement: The climber is injured by following a suggestion.
to: [user]
from: [ELI-2Q7M#6]
""",
    f"{P}/analysis/HAZ-5QKA.yaml": """id: HAZ-5QKA
status: agreed
statement: The product holds the only copy of the climber's training history.
losses: [LOS-8D2F]
arises_from: [FUN-3G1N]
""",
    f"{P}/analysis/HAZ-3F9D.yaml": """id: HAZ-3F9D
status: agreed
statement: The product is suggesting more training load than the climber can take.
losses: [LOS-6TWR]
arises_from: [FUN-7SGT]
""",
    f"{P}/requirements/REQ-8PVS.yaml": """id: REQ-8PVS
status: agreed
pattern: ubiquitous
answers: HAZ-3F9D
of: FUN-7SGT
statement: The product shall not suggest more weekly load than the climber's recent average plus a margin.
""",
    f"{P}/parts.yaml": """parts:
  - name: app
    folder: app
    purpose: What the climber sees and touches, on phone and laptop.
    contributes_to: [FUN-3G1N, FUN-9PRJ]
  - name: sync-service
    folder: sync-service
    purpose: Holds sessions and brings every device up to date.
    contributes_to: [FUN-5YNC]
  - name: suggest-engine
    folder: suggest-engine
    purpose: Turns recent sessions into the next suggestion.
    contributes_to: [FUN-7SGT]
""",
    f"{P}/interfaces/IFC-8DQF.yaml": """id: IFC-8DQF
between: [app, suggest-engine]
items:
  - {item: recent sessions, sender: app}
  - {item: suggestion with its reason, sender: suggest-engine}
""",
    f"{P}/app/steps.yaml": closed(),
    f"{P}/sync-service/steps.yaml": closed(),
    f"{SE}/steps.yaml": closed(),
    f"{SE}/requirements/REQ-Z3NP.yaml": """id: REQ-Z3NP
status: agreed
pattern: ubiquitous
parent: REQ-8PVS
statement: The suggest engine shall not propose more weekly load than the average of the last four weeks plus a margin.
""",
})

# D1: the child untouched, with two flowed requirements that cannot both hold.
D1 = dict(D)
D1[f"{SE}/requirements/REQ-M8YD.yaml"] = """id: REQ-M8YD
status: agreed
pattern: ubiquitous
source: builder
statement: The suggest engine shall compute each suggestion from the latest session only.
rationale: Keeps a suggestion quick on the phone.
"""

# D2: the child grilled and its functions written; they bring no hazard of their own.
D2 = dict(D)
D2.update({
    f"{SE}/analysis/ELI-7VCX.yaml": """id: ELI-7VCX
date: 2026-10-20
entries:
  - n: 1
    question: What should the engine look at?
    answer: "My last four weeks of sessions, nothing else."
    need: true
  - n: 2
    question: How should it choose what comes next?
    answer: "Strength, endurance or technique, whichever I've neglected."
    need: true
  - n: 3
    question: What should it hand you?
    answer: "The focus, how much to do that week, and why."
    need: true
""",
    f"{SE}/functions/FUN-6QWB.yaml": """id: FUN-6QWB
status: agreed
parent: FUN-7SGT
name: Estimate recent load
definition: Turns the last four weeks of sessions into the weekly load the climber has been doing.
""",
    f"{SE}/functions/FUN-A9KE.yaml": """id: FUN-A9KE
status: agreed
parent: FUN-7SGT
name: Pick the next focus
definition: Chooses strength, endurance or technique as the next focus, whichever was trained least.
""",
    f"{SE}/functions/FUN-K2MV.yaml": """id: FUN-K2MV
status: agreed
parent: FUN-7SGT
name: Propose the weekly load
definition: Proposes how much the climber should do in the coming week for the chosen focus.
""",
    f"{SE}/functions/FUN-R7TD.yaml": """id: FUN-R7TD
status: agreed
parent: FUN-7SGT
name: State the reason
definition: Says why this focus and load were chosen, from the climber's recent sessions.
""",
})

# D3: as D2 with one more function, which brings a hazard that looks inherited but is not:
# hard exercises on the same fingers can injure within the weekly limit of REQ-Z3NP.
D3 = dict(D2)
D3[f"{SE}/analysis/ELI-7VCX.yaml"] = D2[f"{SE}/analysis/ELI-7VCX.yaml"].replace(
    "The focus, how much", "The focus, an exercise for it, how much")
D3[f"{SE}/functions/FUN-E4HX.yaml"] = """id: FUN-E4HX
status: agreed
parent: FUN-7SGT
name: Choose the next exercise
definition: Chooses the exercise for the next session, such as fingerboard hangs, to fit the next focus.
"""

CLAUDE_MD = "This project is built with datum. Load the `datum` skill before any work in this project.\n"
FIXTURES = {"A": {}, "B": B, "C": C, "D1": D1, "D2": D2, "D3": D3}
for name, fixture in FIXTURES.items():
    if fixture:
        fixture["CLAUDE.md"] = CLAUDE_MD

if __name__ == "__main__":
    shutil.rmtree(OUT, ignore_errors=True)
    for name, files in FIXTURES.items():
        root = os.path.join(OUT, name)
        os.makedirs(root)
        for path, text in files.items():
            os.makedirs(os.path.dirname(os.path.join(root, path)), exist_ok=True)
            open(os.path.join(root, path), "w").write(text)
    print("fixtures:", ", ".join(f"{k} ({len(v)} files)" for k, v in FIXTURES.items()))
