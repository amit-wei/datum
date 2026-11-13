"""Write the fixture projects F1-F4 into fixtures/<name>/.

A fictional product: a shared-expense splitter. `fixture-src/` holds its functional
analysis, written by a Sonnet agent following datum's functional-analysis skill from
the builder's two elicitation records (ELI-5KXR, ELI-7MDP). Each fixture adds what its
behaviour needs. `steps.yaml` holds the placeholder commit 0000000, which the rig
replaces with the fixture's own commit. Every fixture has the one-line CLAUDE.md; the
baseline runs without it.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "fixture-src")
OUT = os.path.join(HERE, "fixtures")
P = ".datum/model/product"
CHILD = P + "/settlement"
CLAUDE = ("This project is built with datum. Load the `datum` skill before answering any "
          "question about this product or doing any work in it.\n")


def closed(*steps):
    return "".join(f"{s}: {{closed_at: \"0000000\"}}\n" for s in steps) or "{}\n"


# The grilling round of the requirements step: the builder's values and their choice
# for each hazard. F2 drops the rounding entry, F3 the hazard choices.
VALUES = """  - n: 1
    question: Does anything have to be fast?
    answer: "No. A trip has a few dozen expenses; no speed matters to me."
    need: true
  - n: 2
    question: How big can a trip get?
    answer: "At most 12 people and a few hundred expenses."
    need: true
  - n: 3
    question: What amounts do you enter?
    answer: "Up to 10,000 per expense, to the cent, in one currency."
    need: true
"""
ROUNDING = """  - n: 4
    question: What if an amount does not divide evenly?
    answer: "Round each share to the cent and give the leftover cents to the person who paid. Nobody else may pay more than one cent above their exact share."
    need: true
"""
CHOICES = """  - n: 5
    question: How do you want to deal with balances that differ from the expenses recorded (HAZ-4R75)?
    answer: "Prevent it. The balances must always match the expenses exactly."
  - n: 6
    question: How do you want to deal with payments that do not leave everyone settled (HAZ-8NA1)?
    answer: "Prevent it. After the proposed payments everyone must be at zero."
  - n: 7
    question: How do you want to deal with a message that differs from the proposed payments (HAZ-FJYD)?
    answer: "Prevent it. The message says exactly the proposed payments."
  - n: 8
    question: How do you want to deal with an expense removed by mistake (HAZ-DD0C)?
    answer: "Show me the expense and ask me to confirm before deleting it. No undo needed."
  - n: 9
    question: How do you want to deal with the part holding the only copy of the expenses (HAZ-WKAA)?
    answer: "I accept it. No backups, as I said."
"""


def eli(*parts):
    return 'id: ELI-3RQV\ndate: "2026-11-13"\nentries:\n' + "".join(parts)


def source():
    files = {}
    for root, _, names in os.walk(SRC):
        for name in names:
            path = os.path.join(root, name)
            files[os.path.relpath(path, SRC)] = open(path).read()
    return files


BASE = {**source(), "CLAUDE.md": CLAUDE, f"{P}/steps.yaml": closed("functional-analysis")}

# F1: functional analysis closed, every value and hazard choice given.
F1 = {**BASE, f"{P}/analysis/ELI-3RQV.yaml": eli(VALUES, ROUNDING, CHOICES)}
# F2: as F1 without the builder's rounding rule.
F2 = {**BASE, f"{P}/analysis/ELI-3RQV.yaml": eli(VALUES, CHOICES)}
# F3: as F1 without the builder's choice for each hazard.
F3 = {**BASE, f"{P}/analysis/ELI-3RQV.yaml": eli(VALUES, ROUNDING)}

# F4: the product closed through cases, its synthesis handing two requirements down to
# a child part, `settlement`, whose functional analysis is closed. The handed-down
# requirements carry `parent:`, which the v0.1.0 schema does not know: the validator
# reports them, as it would in a real project at this version.
F4 = {**F1, f"{P}/steps.yaml": closed("functional-analysis", "requirements", "synthesis",
                                     "design-evaluation", "cases"),
      f"{P}/requirements/REQ-P1AN.yaml": """id: REQ-P1AN
status: agreed
pattern: event
statement: |
  When the user asks to settle, the part shall propose transfers after which every
  person in the trip has a balance of zero.
of: FUN-Y0N0
answers: [HAZ-8NA1]
""",
      f"{P}/requirements/REQ-M5GE.yaml": """id: REQ-M5GE
status: agreed
pattern: ubiquitous
statement: The part shall put into the settlement message exactly the transfers it proposed.
of: FUN-Z9Q2
answers: [HAZ-FJYD]
""",
      f"{P}/proofs/PRF-T8WJ.yaml": """id: PRF-T8WJ
status: agreed
title: Every proposed settlement leaves everyone at zero
method: test
rationale: Settling is the point of the product, and any change to the balances or the transfer search can break it.
covers: [REQ-P1AN]
criterion:
  pass: For every trip in the sample, applying the proposed transfers leaves every balance at zero.
  sample_min: 500
  conditions: Generated trips of 2 to 12 people with up to 300 expenses, even and exact splits mixed.
""",
      f"{P}/proofs/PRF-C2VR.yaml": """id: PRF-C2VR
status: agreed
title: The message matches the proposed transfers
method: test
rationale: The message is built from the transfers by code that later changes can break.
covers: [REQ-M5GE]
criterion:
  pass: The transfers read back from the message equal the proposed transfers, for every trip in the sample.
  sample_min: 100
  conditions: The generated trips of PRF-T8WJ.
""",
      f"{P}/parts.yaml": """parts:
  - name: settlement
    folder: settlement
    purpose: Turns the balances into the fewest transfers and the message that lists them.
    contributes_to: [FUN-Y0N0, FUN-Z9Q2]
""",
      f"{CHILD}/steps.yaml": closed("functional-analysis"),
      f"{CHILD}/functions/FUN-6QSE.yaml": """id: FUN-6QSE
status: agreed
parent: FUN-Y0N0
name: Find the fewest transfers
definition: From the balances of everyone in the trip, finds the smallest set of transfers that brings every balance to zero.
""",
      f"{CHILD}/functions/FUN-XK4B.yaml": """id: FUN-XK4B
status: agreed
parent: FUN-Z9Q2
name: Format the transfers as text
definition: Writes the proposed transfers as plain text, one transfer per line, for the user to paste into a chat.
""",
      f"{CHILD}/requirements/REQ-HV7N.yaml": """id: REQ-HV7N
status: agreed
pattern: ubiquitous
parent: REQ-P1AN
statement: The part shall propose no more transfers than the number of people in the trip minus one.
""",
      f"{CHILD}/requirements/REQ-0R3S.yaml": """id: REQ-0R3S
status: agreed
pattern: ubiquitous
parent: REQ-M5GE
statement: The part shall write each transfer as the payer's name, the receiver's name and the amount to the cent.
""",
      }

FIXTURES = {"F1": F1, "F2": F2, "F3": F3, "F4": F4}

if __name__ == "__main__":
    shutil.rmtree(OUT, ignore_errors=True)
    for name, files in FIXTURES.items():
        root = os.path.join(OUT, name)
        for path, text in files.items():
            os.makedirs(os.path.dirname(os.path.join(root, path)), exist_ok=True)
            open(os.path.join(root, path), "w").write(text)
    print("fixtures:", ", ".join(f"{k} ({len(v)} files)" for k, v in FIXTURES.items()))
