# Glossary

The terms datum uses, one meaning each. Skills, agents and docs use these words and no
synonyms; a reviewer flags any other. Add a term when it first appears in a skill.

| Term | Meaning |
|---|---|
| builder | The person who builds the product with datum and decides what is theirs to decide |
| part | A node of the product's tree. Every part runs the same engine steps |
| top part, product | The root part, `datum/model/product/` |
| leaf part | A part that meets the stopping rule: built or bought as one thing |
| unit | Something that runs separately (a process, a service); it hosts one or more parts |
| model | Everything under `datum/model/`: the artifacts of every part |
| artifact | One file of the model, named by its ID |
| ID | A type prefix and 4 Crockford base32 characters (`REQ-7K3Q`) |
| need | What the builder wants, drawn out by grilling into an elicitation record |
| scenario | One end-to-end journey from a trigger to an outcome the builder cares about |
| function | Something a part does, as a verb and its object, independent of how |
| requirement | What must hold for a function, and how well; or a constraint, or a budget |
| proof | The planned verification of requirements: a method and a criterion |
| method | Inspection, Analysis, Demonstration or Test |
| case | An executable piece (a test, an eval run, a script) that implements a proof |
| evidence | The result of running a proof's cases at a commit |
| verified | The evidence passes at the version's commit |
| decision, ADR | A choice with the alternatives considered and the reason, recorded with the prefix `ADR-` (architecture decision record, the software name). One type for every recorded choice |
| interface | What crosses between two parts, or between a part and something outside |
| engine step | One of the five steps every part runs: functional analysis, requirements, synthesis, design evaluation, cases |
| technique | How to do one thing well inside a step; a skill of its own |
| end condition | What must hold before the builder can close a step |
| closed | A step the builder has closed, recorded in `steps.yaml` with its commit |
| stale | A closed step whose part's files changed after its closing commit, and everything that depends on it |
| increment | A usable, verified addition of capability: a set of functions plus deferrals |
| stub | A stand-in for an out-of-scope part, derived from its interface |
| finding | What a reviewer reports: blocking, should fix, or a note |
| loss, hazard | Open: their form is being explored |
