# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6", "jsonschema>=4.18"]
# ///
"""Check a datum model: each file against its schema, then the rules across files.

Run from the builder's repo: uv run validate.py [repo root]
Prints errors and warnings; exits 1 when there is an error. Clean means no errors.
"""
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry
from referencing.jsonschema import DRAFT202012

ROOT = Path("datum/model")
SCHEMAS = Path(__file__).resolve().parent.parent / "schemas"
ID = r"[A-Z]{3}-[0-9A-HJKMNP-TV-Z]{4}"
LINK = re.compile(rf"^({ID})(?:#([1-9][0-9]*))?$")
BY_PREFIX = {"FUN": "function", "SCN": "scenario", "ELI": "elicitation"}
UNCHECKED = {"SPK", "RES"}  # no schema yet: their step brings one


class Loader(yaml.SafeLoader):
    """Safe YAML that keeps dates as text, so a schema checks them as strings."""


Loader.yaml_implicit_resolvers = {
    k: [r for r in v if r[0] != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def load_schemas():
    docs = {p.name: yaml.load(p.read_text(), Loader) for p in SCHEMAS.glob("*.yaml")}
    registry = Registry().with_resources(
        (name, DRAFT202012.create_resource(doc)) for name, doc in docs.items()
    )
    return {name[:-5]: Draft202012Validator(doc, registry=registry) for name, doc in docs.items()}


def bool_keys(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if isinstance(k, bool):
                yield k
            yield from bool_keys(v)
    elif isinstance(x, list):
        for i in x:
            yield from bool_keys(i)


def links(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if k != "id":
                yield from links(v)
    elif isinstance(x, list):
        for i in x:
            yield from links(i)
    elif isinstance(x, str) and LINK.match(x):
        yield x


def part_of(f):
    """The part folder a file belongs to: the folder above its type folder."""
    return f.parent.parent


def main():
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    model = repo / ROOT
    if not model.is_dir():
        print(f"no model: {model} does not exist")
        return 1
    validators = load_schemas()
    errs, warns, arts = [], [], {}

    def rel(f):
        return f.relative_to(repo).as_posix()

    for f in sorted(model.rglob("*")):
        if not f.is_file():
            continue
        if f.suffix != ".yaml":
            warns.append(f"{rel(f)}: not a model file (only .yaml belongs in the model)")
            continue
        try:
            d = yaml.load(f.read_text(), Loader)
        except yaml.YAMLError as e:
            errs.append(f"{rel(f)}: not valid YAML: {str(e).splitlines()[0]}")
            continue
        for k in bool_keys(d):
            errs.append(f"{rel(f)}: key read as boolean {k} (quote it, or avoid on/off/yes/no)")
        if f.name == "steps.yaml":
            kind = "steps"
        elif f.name == "parts.yaml":
            continue  # synthesis brings its schema
        else:
            prefix = f.stem[:3]
            if prefix in UNCHECKED:
                continue
            kind = BY_PREFIX.get(prefix)
            if kind is None:
                warns.append(f"{rel(f)}: no schema for this file yet, not checked")
                continue
        for e in validators[kind].iter_errors(d):
            where = "/".join(str(p) for p in e.absolute_path)
            errs.append(f"{rel(f)}: {where + ': ' if where else ''}{e.message}")
        if kind == "steps" or not isinstance(d, dict):
            continue
        if d.get("id") != f.stem:
            errs.append(f"{rel(f)}: file name is not the id ({d.get('id')})")
            continue
        if d["id"] in arts:
            errs.append(f"{rel(f)}: id also used by {rel(arts[d['id']][1])}")
            continue
        arts[d["id"]] = (d, f)

    # Numbered entries and steps: unique, because links name them by number.
    numbers = {}
    for i, (d, f) in arts.items():
        items = d.get("entries") if i.startswith("ELI") else d.get("steps") if i.startswith("SCN") else None
        if not isinstance(items, list):
            continue
        ns = [x.get("n") for x in items if isinstance(x, dict)]
        for n in {n for n in ns if ns.count(n) > 1}:
            errs.append(f"{rel(f)}: number {n} used twice")
        numbers[i] = {x.get("n"): x for x in items if isinstance(x, dict)}

    # Every link resolves, and a #n names an entry or step that exists.
    for i, (d, f) in arts.items():
        for link in links(d):
            target, n = LINK.match(link).groups()
            if target not in arts:
                errs.append(f"{rel(f)}: {link} does not exist")
            elif n and int(n) not in numbers.get(target, {}):
                errs.append(f"{rel(f)}: {link}: {target} has no number {n}")

    # Rules by type.
    product = model / "product"
    needed = {}  # ELI entry -> covered by a scenario
    served = {}  # product scenario step -> served by a function
    for i, (d, f) in arts.items():
        if i.startswith("ELI"):
            for n, e in numbers.get(i, {}).items():
                if e.get("need") is True:
                    needed[f"{i}#{n}"] = False
        if i.startswith("SCN"):
            for n, s in numbers.get(i, {}).items():
                if s.get("by") == "product":
                    served[f"{i}#{n}"] = False
    for i, (d, f) in arts.items():
        if i.startswith("SCN"):
            for link in d.get("needs") or []:
                if link in needed:
                    needed[link] = True
                elif (m := LINK.match(link)) and m.group(2) and int(m.group(2)) in numbers.get(m.group(1), {}):
                    errs.append(f"{rel(f)}: needs {link}, an entry not marked need: true")
        if i.startswith("FUN"):
            at_product = part_of(f) == product
            if at_product and "parent" in d:
                errs.append(f"{rel(f)}: a product function has no parent function")
            if at_product and not d.get("serves"):
                errs.append(f"{rel(f)}: a product function serves no scenario step")
            if not at_product and "serves" in d:
                errs.append(f"{rel(f)}: only product functions serve scenario steps; use parent")
            if not at_product and "parent" not in d:
                errs.append(f"{rel(f)}: no parent function (the parent part's function it takes on)")
            p = d.get("parent")
            if p in arts and part_of(arts[p][1]) != part_of(f).parent:
                errs.append(f"{rel(f)}: parent {p} is not a function of the parent part")
            for link in d.get("serves") or []:
                if link in served:
                    served[link] = True
    for link, ok in sorted(needed.items()):
        if not ok:
            warns.append(f"{link}: a need no scenario covers")
    for link, ok in sorted(served.items()):
        if not ok:
            warns.append(f"{link}: a product step no function serves")

    print(f"ERRORS {len(errs)}")
    for e in errs:
        print(f"  {e}")
    print(f"WARNINGS {len(warns)}")
    for w in warns:
        print(f"  {w}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
