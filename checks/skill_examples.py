# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6", "jsonschema>=4.18"]
# ///
"""Check that every model-file example in a skill fits its schema, so skills and schemas
cannot drift. Checks each file alone: links between examples are not resolved.

Run from this repository's root: uv run checks/skill_examples.py
Exits 1 when an example does not fit.
"""
import importlib.util
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("validate", REPO / "scripts" / "validate.py")
validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate)

BLOCK = re.compile(r"^```yaml\n(.*?)^```", re.M | re.S)


def main():
    validators = validate.load_schemas()
    bad, seen = 0, 0
    for skill in sorted(REPO.glob("skills/**/SKILL.md")):
        for block in BLOCK.findall(skill.read_text()):
            try:
                d = yaml.load(block, validate.Loader)
            except yaml.YAMLError as e:
                print(f"{skill.relative_to(REPO)}: example is not valid YAML: {str(e).splitlines()[0]}")
                bad += 1
                continue
            kind = validate.BY_PREFIX.get(str(d.get("id", ""))[:3]) if isinstance(d, dict) else None
            if kind is None:
                continue
            seen += 1
            for e in validators[kind].iter_errors(d):
                where = "/".join(str(p) for p in e.absolute_path)
                print(f"{skill.relative_to(REPO)}: {d['id']}: {where + ': ' if where else ''}{e.message}")
                bad += 1
    print(f"{seen} examples checked, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
