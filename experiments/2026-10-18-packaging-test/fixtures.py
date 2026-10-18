"""Write the fixture projects F0-F7 into fixtures/<F>/.

A fictional product: a tool that logs climbing sessions and suggests what to train
next. Each fixture adds to an earlier one. `steps.yaml` holds `closed_at: HEAD`, which
run.py replaces with the commit that holds the fixture, so no closed step is stale.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "fixtures")
P = "model/product"
SE = P + "/suggest-engine"


def closed(*steps):
    return "".join(f"{s}: {{closed_at: HEAD}}\n" for s in steps) or "{}\n"


F1 = {
    f"{P}/steps.yaml": closed(),
    f"{P}/analysis/ELI-2Q7M.yaml": """id: ELI-2Q7M
type: elicitation
date: 2026-10-01
needs:
  - id: N1
    words: "I forget what I did last time, so I repeat the same routes."
  - id: N2
    words: "I want to know what to train next without paying a coach."
  - id: N3
    words: "I log on my phone at the gym and look at it on my laptop at home."
""",
    f"{P}/analysis/SCN-4H8R.yaml": """id: SCN-4H8R
type: scenario
title: Log a session at the gym
actor: climber
covers: [ELI-2Q7M]
steps:
  - The climber opens the app on their phone at the gym.
  - They add each route or problem tried, its grade and whether it was sent.
  - They end the session.
  - At home, the session is on their laptop.
""",
    f"{P}/analysis/SCN-9W2E.yaml": """id: SCN-9W2E
type: scenario
title: Get the next training suggestion
actor: climber
covers: [ELI-2Q7M]
steps:
  - Before a session, the climber asks what to train.
  - They see a suggestion with the reason for it, drawn from their recent sessions.
""",
}

F2 = dict(F1)
F2.update({
    f"{P}/steps.yaml": closed("functional-analysis"),
    f"{P}/functions/FUN-3G1N.yaml": "id: FUN-3G1N\nstatement: Log a session\nserves: [SCN-4H8R]\nstate: agreed\n",
    f"{P}/functions/FUN-7SGT.yaml": "id: FUN-7SGT\nstatement: Suggest what to train next\nserves: [SCN-9W2E]\nstate: agreed\n",
    f"{P}/functions/FUN-5YNC.yaml": "id: FUN-5YNC\nstatement: Keep sessions the same on every device\nserves: [SCN-4H8R]\nstate: agreed\n",
    f"{P}/risks/RSK-3F9D.yaml": "id: RSK-3F9D\nstatement: A suggestion pushes the climber to overtrain and get injured\nthreatens: FUN-7SGT\n",
    f"{P}/requirements/REQ-7K3Q.yaml": """id: REQ-7K3Q
of: FUN-5YNC
pattern: event
statement: When a sesion is ended, the product shall show it on the climber's other devices within {measure}.
measure:
  metric: time from ending a session to it being shown on another online device
  bounds:
    - {statistic: p95, op: "<=", value: 2 s}
rationale: The climber checks the session at home soon after; a short wait is fine, minutes are not.
state: draft
""",
})

F3 = dict(F2)
F3.update({
    f"{P}/steps.yaml": closed("functional-analysis", "requirements"),
    f"{P}/requirements/REQ-7K3Q.yaml": F2[f"{P}/requirements/REQ-7K3Q.yaml"].replace("sesion", "session").replace("draft", "agreed"),
    f"{P}/requirements/REQ-1MRX.yaml": "id: REQ-1MRX\nof: FUN-3G1N\npattern: event\nstatement: When the climber adds an attempt, the product shall record its route, grade and outcome.\nstate: agreed\n",
    f"{P}/requirements/REQ-8PVS.yaml": "id: REQ-8PVS\nanswers: RSK-3F9D\npattern: ubiquitous\nstatement: The product shall not suggest more training load in a week than the climber's recent average plus a margin.\nstate: agreed\n",
    f"{P}/requirements/REQ-B4DG.yaml": """id: REQ-B4DG
of: FUN-7SGT
pattern: event
statement: When the climber asks what to train, the product shall show a suggestion within {measure}.
measure:
  metric: time from the request to the suggestion being shown
  bounds:
    - {statistic: p95, op: "<=", value: 1 s}
rationale: A suggestion is checked standing at the wall; a wait breaks the flow.
state: agreed
""",
    f"{P}/proofs/PRF-6TZA.yaml": "id: PRF-6TZA\nmethod: Test\ncovers: [REQ-7K3Q]\ncriterion: Over 200 ended sessions on two online devices, the p95 of the measure meets its bound.\n",
    f"{P}/proofs/PRF-2CQE.yaml": "id: PRF-2CQE\nmethod: Test\ncovers: [REQ-1MRX]\ncriterion: Every field of an added attempt is read back unchanged.\n",
    f"{P}/proofs/PRF-5JKB.yaml": "id: PRF-5JKB\nmethod: Test\ncovers: [REQ-8PVS]\ncriterion: For 50 generated histories, no suggested week exceeds the bound.\n",
    f"{P}/proofs/PRF-9HMD.yaml": "id: PRF-9HMD\nmethod: Test\ncovers: [REQ-B4DG]\ncriterion: Over 200 requests on the reference phone, the p95 of the measure meets its bound.\n",
})

PARTS = """parts:
  - name: app
    folder: app
    purpose: What the climber sees and touches, on phone and laptop.
    contributes_to: [FUN-3G1N, FUN-7SGT]
  - name: sync-service
    folder: sync-service
    purpose: Holds sessions and brings every device up to date.
    contributes_to: [FUN-5YNC]
  - name: suggest-engine
    folder: suggest-engine
    purpose: Turns recent sessions into the next suggestion.
    contributes_to: [FUN-7SGT]
"""

F6 = dict(F3)
F6.update({
    f"{P}/parts.yaml": PARTS,
    f"{P}/decisions/DEC-4XQ2.yaml": "id: DEC-4XQ2\nstatement: One app for phone and laptop, a hosted sync service, the suggestion computed on the device\ndrivers: [REQ-7K3Q, REQ-B4DG]\noptions:\n  - Suggestion on the server\n  - Suggestion on the device (chosen: works offline at the wall)\nstate: agreed\n",
    f"{P}/app/requirements/REQ-W1TA.yaml": "id: REQ-W1TA\nparent: REQ-1MRX\npattern: event\nstatement: When the climber adds an attempt, the app shall store its route, grade and outcome on the device.\nstate: agreed\n",
    f"{P}/sync-service/requirements/REQ-K7EB.yaml": "id: REQ-K7EB\nparent: REQ-7K3Q\npattern: event\nstatement: When the sync service receives a session, it shall make it available to the climber's other devices within {measure}.\nmeasure:\n  metric: time from receipt to availability\n  bounds:\n    - {statistic: p95, op: \"<=\", value: 1 s}\nrationale: Half of the product's 2 s budget; the rest is the devices' upload and fetch.\nstate: agreed\n",
    f"{SE}/requirements/REQ-Z3NP.yaml": "id: REQ-Z3NP\nparent: REQ-8PVS\npattern: ubiquitous\nstatement: The suggest engine shall not propose more weekly load than the recent average plus a margin.\nstate: agreed\n",
})

F7 = dict(F6)
F7.update({
    f"{P}/steps.yaml": closed("functional-analysis", "requirements", "synthesis"),
    f"{P}/app/requirements/REQ-H5RC.yaml": "id: REQ-H5RC\nparent: REQ-B4DG\npattern: event\nstatement: When a suggestion is ready, the app shall show it within {measure}.\nmeasure:\n  metric: time from the suggestion being ready to shown\n  bounds:\n    - {statistic: p95, op: \"<=\", value: 300 ms}\nrationale: Share of REQ-B4DG's 1 s budget.\nstate: agreed\n",
    f"{SE}/requirements/REQ-M8YD.yaml": "id: REQ-M8YD\nparent: REQ-B4DG\npattern: event\nstatement: When asked, the suggest engine shall return a suggestion within {measure}.\nmeasure:\n  metric: time from the request to the returned suggestion\n  bounds:\n    - {statistic: p95, op: \"<=\", value: 700 ms}\nrationale: Share of REQ-B4DG's 1 s budget.\nstate: agreed\n",
    f"{P}/interfaces/IFC-2B6V.yaml": "id: IFC-2B6V\nbetween: [app, sync-service]\nitems:\n  - {item: session, sender: app}\n  - {item: session, sender: sync-service}\n",
    f"{P}/interfaces/IFC-8DQF.yaml": "id: IFC-8DQF\nbetween: [app, suggest-engine]\nitems:\n  - {item: recent sessions, sender: app}\n  - {item: suggestion with its reason, sender: suggest-engine}\n",
})

F4 = dict(F7)
F4.update({
    f"{P}/steps.yaml": closed("functional-analysis", "requirements", "synthesis", "design-evaluation"),
    f"{P}/app/steps.yaml": closed(),
    f"{P}/sync-service/steps.yaml": closed(),
    f"{SE}/steps.yaml": closed(),
})

F5 = dict(F4)
F5.update({
    f"{SE}/steps.yaml": closed("functional-analysis", "requirements"),
    f"{SE}/functions/FUN-6QWB.yaml": "id: FUN-6QWB\nparent: FUN-7SGT\nstatement: Estimate the climber's recent load\nstate: agreed\n",
    f"{SE}/functions/FUN-A9KE.yaml": "id: FUN-A9KE\nparent: FUN-7SGT\nstatement: Pick the next focus (strength, endurance, technique) and explain why\nstate: agreed\n",
    f"{SE}/requirements/REQ-T2FH.yaml": "id: REQ-T2FH\nof: FUN-A9KE\npattern: ubiquitous\nstatement: The suggest engine shall state the reason for every suggestion in one sentence.\nstate: agreed\n",
})

FIXTURES = {"F0": {}, "F1": F1, "F2": F2, "F3": F3, "F4": F4, "F5": F5, "F6": F6, "F7": F7}

if __name__ == "__main__":
    shutil.rmtree(OUT, ignore_errors=True)
    for name, files in FIXTURES.items():
        root = os.path.join(OUT, name)
        os.makedirs(root)
        for path, text in files.items():
            os.makedirs(os.path.dirname(os.path.join(root, path)), exist_ok=True)
            open(os.path.join(root, path), "w").write(text)
    print("fixtures:", ", ".join(f"{k} ({len(v)} files)" for k, v in FIXTURES.items()))
