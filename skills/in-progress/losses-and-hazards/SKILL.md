---
name: losses-and-hazards
description: Use once a part's functions are written, to find what must never happen and the states of the part that could lead there - at the product the losses and hazards, at any other part only the hazards its own functions introduce. Produces LOS- and HAZ- files. Not for what must hold to prevent a hazard (use writing-requirements) or for how parts and interfaces could cause one (synthesis's risk pass).
---

# Losses and hazards

This is step 1 of STPA (System-Theoretic Process Analysis), a safety method from
systems engineering (Leveson). It asks first what must never happen, then which states
of the part could lead there. Later steps answer each hazard with requirements; this
technique only finds and writes them.

- A **loss** is something the builder, a user or a third party must never suffer: an
  injury, lost or leaked data, lost money, a broken promise to someone. It names what
  is lost and by whom, not how.
- A **hazard** is a state of the part that, under bad conditions, leads to a loss. It
  is a state the part can be in, not a cause ("the server crashes") and not the loss
  itself ("the history is lost").

## Losses (the product only)

Losses are the builder's to state; they exist only at the product.

1. Read the elicitation records for entries marked `loss: true`, and for answers that
   name a harm without the mark.
2. If there are none, or a kind of harm the product plainly touches is missing (people
   hurt, data lost or exposed, money, trust), load `grilling` and ask the builder
   what must never happen, and to whom.
3. If the domain carries harms the builder cannot be expected to know (health,
   payments, children, personal data under law), run `research` in a subagent first,
   then put what it finds to the builder.

Write one `LOS-` file per loss the builder agrees to, linked to the entries it came
from. Keep a loss free of causes and designs: "the climber's training history is
lost", not "the history is lost when the phone breaks". Harm through what people do
with the product's output counts too: a suggested load the climber follows can injure
them. A harm the product cannot lead to is not a loss: mark its entry `out_of_scope`
with the reason, and write no file.

## Hazards (every part)

For each function of the part, ask: in what state of this part would a loss follow,
given bad conditions outside it? Write each such state as a hazard, linked to the
losses it leads to and the functions that introduce it.

- **One state, at this part's level.** A hazard names the part, not a lower part or a
  component: "the product holds the only copy of the training history".
- **A handful, not a list of causes.** Many causes lead to the same state; the causes
  come later, in synthesis's risk pass.
- **Every loss is reached** by at least one hazard of the product. A loss with none
  means a hazard is missing: look again before anything else. If the product truly
  cannot lead to it, it was never a loss: remove the file and mark its entry
  `out_of_scope` with the reason.

Below the product, a part lists only the hazards its own functions introduce. Most
introduce none: then write nothing. Do not restate a parent's hazards: they arrive
answered, as requirements in the part's `requirements/` folder. A new hazard that looks
like an inherited one is new only if no parent requirement already answers it; check
those requirements before writing it.

Not here: answering a hazard (requirements, with `answers: HAZ`), and unsafe control
actions or loss scenarios (synthesis's risk pass).

## The files

Losses in `.datum/model/product/analysis/`, hazards in the part's `analysis/` folder,
one file each, named by its ID. Make the ID with a fresh suffix and check that no file
already uses it:

```
echo "LOS-$(LC_ALL=C tr -dc '0-9A-HJKMNP-TV-Z' </dev/urandom | head -c 4)"
echo "HAZ-$(LC_ALL=C tr -dc '0-9A-HJKMNP-TV-Z' </dev/urandom | head -c 4)"
```

A loss: `id`, `status` (`draft` until the builder agrees), `statement`, `to` (any of
`user`, `builder`, `third party`), and `from` (the entries, as
`ELI-XXXX#n`). A hazard: `id`, `status`, `statement`,
`losses` and `arises_from` (functions of this part).

Two examples, for illustration only:

```yaml
id: LOS-8D2F
status: draft
statement: The climber's training history is lost.
to: [user]
from: [ELI-3RWN#2]
```

```yaml
id: HAZ-5QKA
status: draft
statement: The product holds the only copy of the climber's training history.
losses: [LOS-8D2F]
arises_from: [FUN-3G1N]
```
