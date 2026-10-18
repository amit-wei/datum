"""Build the three packaging variants from source/ into variants/<S|R|H>/.

S: every technique is a listed skill.
R: techniques are reference files inside each step skill that uses them.
H: every technique is a skill with disable-model-invocation: true.

Each variant is a Claude Code plugin named `datum`, loaded with --plugin-dir.
The text a step shows about a technique (its condition and description) is the same
in every variant; only how it is loaded differs.
"""
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(HERE, "variants")
USE = re.compile(r"^\{\{use ([a-z0-9-]+): (.+)\}\}$", re.M)
INCLUDE = re.compile(r"^\{\{include ([a-z0-9-]+)\}\}$", re.M)


def parse(path):
    text = open(path).read()
    _, front, body = text.split("---\n", 2)
    meta = {}
    for line in front.strip().splitlines():
        key, value = line.split(": ", 1)
        meta[key] = value
    return meta, body.lstrip("\n")


def load(kind):
    folder = os.path.join(SRC, kind)
    return {f[:-3]: parse(os.path.join(folder, f)) for f in sorted(os.listdir(folder))}


def frontmatter(meta, extra=()):
    lines = [f"name: {meta['name']}", f"description: {json.dumps(meta['description'])}"]
    lines += list(extra)
    return "---\n" + "\n".join(lines) + "\n---\n\n"


def pointer(variant, name, condition, techniques):
    description = techniques[name][0]["description"]
    if variant == "R":
        how = f"read `references/{name}.md` in this skill's folder"
    else:
        how = f"load it with the Skill tool: `datum:{name}`"
    return f"- **`{name}`**: {condition}\n  {description} To use it, {how}."


def build(variant, steps, techniques, agents):
    root = os.path.join(OUT, variant)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(os.path.join(root, ".claude-plugin"))
    json.dump({"name": "datum", "version": "0.0.0-packaging-" + variant,
               "description": "Packaging test variant " + variant},
              open(os.path.join(root, ".claude-plugin", "plugin.json"), "w"), indent=2)
    shared = {f[:-3]: open(os.path.join(SRC, "shared", f)).read().strip()
              for f in os.listdir(os.path.join(SRC, "shared"))}
    for name, (meta, body) in steps.items():
        used = USE.findall(body)
        body = INCLUDE.sub(lambda m: shared[m.group(1)], body)
        body = USE.sub(lambda m: pointer(variant, m.group(1), m.group(2), techniques), body)
        folder = os.path.join(root, "skills", name)
        os.makedirs(folder)
        open(os.path.join(folder, "SKILL.md"), "w").write(frontmatter(meta) + body)
        if variant == "R":
            os.makedirs(os.path.join(folder, "references"))
            for tech, _ in used:
                tmeta, tbody = techniques[tech]
                open(os.path.join(folder, "references", tech + ".md"), "w").write(
                    f"# {tech}\n\n{tmeta['description']}\n\n{tbody}")
    if variant != "R":
        extra = ["disable-model-invocation: true"] if variant == "H" else []
        for name, (meta, body) in techniques.items():
            folder = os.path.join(root, "skills", name)
            os.makedirs(folder)
            open(os.path.join(folder, "SKILL.md"), "w").write(
                frontmatter(meta, extra) + f"# {name}\n\n" + body)
    os.makedirs(os.path.join(root, "agents"))
    for name, (meta, body) in agents.items():
        lines = [f"{k}: {json.dumps(v) if k == 'description' else v}" for k, v in meta.items()]
        open(os.path.join(root, "agents", name + ".md"), "w").write(
            "---\n" + "\n".join(lines) + "\n---\n\n" + body)


def check(steps, techniques):
    """Every technique is used by some step, and every use names a technique."""
    used = {t for _, body in steps.values() for t, _ in USE.findall(body)}
    missing = used - set(techniques)
    unused = set(techniques) - used
    if missing or unused:
        sys.exit(f"unknown techniques: {sorted(missing)}; unused: {sorted(unused)}")


if __name__ == "__main__":
    steps, techniques, agents = load("steps"), load("techniques"), load("agents")
    check(steps, techniques)
    for variant in "SRH":
        build(variant, steps, techniques, agents)
    print(f"built S, R, H: {len(steps)} steps, {len(techniques)} techniques, {len(agents)} agents")
