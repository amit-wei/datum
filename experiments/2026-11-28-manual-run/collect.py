"""Copy the manual run's record into results/ after the run (#66).

Copies from <run>/ (default ~/datum-run):
  config/projects/**.jsonl  -> results/transcripts/  (the main session and its subagents)
  product/ tracked and untracked files, without .git -> results/product/
  product/ git log, without author names or emails -> results/product-log.txt
  notes.md, commit.txt      -> results/

The home folder and user name are replaced by "~" and "user" in every text file, since
the repository is public. Read results/ before committing it: anything personal said in
the run is still there. Refuses to overwrite an existing results/.
Usage: python3 collect.py [run-dir]
"""
import getpass
import glob
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results")


def scrub(path, home, user):
    try:
        text = open(path, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError):
        return
    text = text.replace(home, "~").replace(user, "user")
    open(path, "w", encoding="utf-8").write(text)


def main():
    run = os.path.abspath(os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/datum-run"))
    if os.path.exists(OUT):
        sys.exit(f"{OUT} already exists; look at it before replacing it.")
    os.makedirs(os.path.join(OUT, "transcripts"))

    for f in glob.glob(os.path.join(run, "config", "projects", "**", "*.jsonl"), recursive=True):
        rel = os.path.relpath(f, os.path.join(run, "config", "projects"))
        dest = os.path.join(OUT, "transcripts", rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(f, dest)

    product = os.path.join(run, "product")
    shutil.copytree(product, os.path.join(OUT, "product"), ignore=shutil.ignore_patterns(".git"))
    log = subprocess.run(["git", "log", "--date=iso", "--format=%h %ad %s", "--stat"],
                         cwd=product, capture_output=True, text=True).stdout
    open(os.path.join(OUT, "product-log.txt"), "w").write(log)
    for name in ("notes.md", "commit.txt"):
        if os.path.exists(os.path.join(run, name)):
            shutil.copy2(os.path.join(run, name), OUT)

    home, user = os.path.expanduser("~"), getpass.getuser()
    for root, _, files in os.walk(OUT):
        for name in files:
            scrub(os.path.join(root, name), home, user)
    print(f"copied to {OUT}; read it for anything personal before committing.")


if __name__ == "__main__":
    main()
