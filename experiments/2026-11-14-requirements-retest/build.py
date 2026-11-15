"""Build plugin/, the `datum` plugin, from the repo's skills, agents, scripts and schemas."""
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(HERE, "plugin")

def build():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(os.path.join(OUT, ".claude-plugin"))
    json.dump({"name": "datum", "version": "0.0.0-req-retest", "description": "Requirements retest"},
              open(os.path.join(OUT, ".claude-plugin", "plugin.json"), "w"), indent=2)
    shutil.copytree(os.path.join(REPO, "skills", "in-progress"), os.path.join(OUT, "skills"))
    for folder in ("agents", "scripts", "schemas"):
        shutil.copytree(os.path.join(REPO, folder), os.path.join(OUT, folder))
    return sorted(os.listdir(os.path.join(OUT, "skills")))


if __name__ == "__main__":
    print("built:", ", ".join(build()))
