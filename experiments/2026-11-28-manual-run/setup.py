"""Set up the manual run (#66) outside the repository.

Makes <run>/ (default ~/datum-run) with:
  plugin/   the datum plugin, built from this repository's current skills, agents,
            scripts and schemas
  product/  an empty git repository: the builder's project, where Claude is started
  config/   a fresh Claude config (CLAUDE_CONFIG_DIR), so no personal skills, plugins,
            settings or memories leak into the run
  notes.md  the builder's running notes, outside product/
  commit.txt the datum commit the plugin was built from

Refuses to touch a <run>/ that already exists. Usage: python3 setup.py [run-dir]
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

NOTES = """# Notes (builder)

One line per moment worth keeping: the turn, what happened, and, apart, your impression.

| Turn | What happened | Impression |
|---|---|---|
"""


def git(*args, cwd):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def build_plugin(out, commit):
    os.makedirs(os.path.join(out, ".claude-plugin"))
    json.dump({"name": "datum", "version": f"0.0.0-manual-run+{commit}",
               "description": "datum, built for the manual run (#66)"},
              open(os.path.join(out, ".claude-plugin", "plugin.json"), "w"), indent=2)
    shutil.copytree(os.path.join(REPO, "skills", "in-progress"), os.path.join(out, "skills"))
    for folder in ("agents", "scripts", "schemas"):
        shutil.copytree(os.path.join(REPO, folder), os.path.join(out, folder))
    return sorted(os.listdir(os.path.join(out, "skills"))), sorted(os.listdir(os.path.join(out, "agents")))


def main():
    run = os.path.abspath(os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/datum-run"))
    if os.path.exists(run):
        sys.exit(f"{run} already exists; look at it, then remove it or pass another folder.")
    if git("status", "--porcelain", cwd=REPO):
        print("warning: the datum repository has uncommitted changes; the plugin includes them.")
    commit = git("rev-parse", "--short", "HEAD", cwd=REPO)

    os.makedirs(run)
    skills, agents = build_plugin(os.path.join(run, "plugin"), commit)
    product = os.path.join(run, "product")
    os.makedirs(product)
    git("init", "-q", "-b", "main", cwd=product)
    os.makedirs(os.path.join(run, "config"))
    open(os.path.join(run, "notes.md"), "w").write(NOTES)
    open(os.path.join(run, "commit.txt"), "w").write(commit + "\n")

    print(f"run folder: {run} (datum {commit})")
    print("skills:", ", ".join(skills))
    print("agents:", ", ".join(agents))
    print("\nStart it with:\n")
    print(f"  cd {product}")
    print(f"  CLAUDE_CONFIG_DIR={run}/config claude --plugin-dir {run}/plugin --model sonnet")
    print("\nThen /login once, and begin with /datum:datum and your description of the product.")


if __name__ == "__main__":
    main()
