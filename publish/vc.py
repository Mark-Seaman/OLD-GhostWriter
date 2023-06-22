from os import chdir, system
from os.path import exists
from pathlib import Path, PurePath

from publish.shell import shell


def vc_command(options):
    if options:
        cmd = options[0]
        args = options[1:]
        if cmd == "commit":
            vc_commit(args)
        elif cmd == "diff":
            vc_diff()
        elif cmd == "dirs":
            for d in vc_dirs():
                print(PurePath(d))
        # elif cmd == 'log':
        #     vc_log(args)
        elif cmd == "pull":
            vc_pull(args)
        elif cmd == "push":
            vc_push()
        elif cmd == "status":
            vc_status()
        else:
            vc_help()
    else:
        vc_help()


def vc_help():
    print(
        """
        vc Command

        usage: x vc COMMAND [ARGS]

        COMMAND:

            commit  - update all local changes in git
            diff    - show uncommitted changes
            dirs    - show the version directories
            log     - show the log on the production server
            pull    - pull all changes from repo
            push    - push all changes to repo
            status  - show git status

        """
    )


# ------------------------------
# Functions


def git_cmd(label, cmd):
    print(label)
    for d in vc_dirs():
        print(d)
        chdir(d)
        text = git_filter(shell(cmd))
        if text and text != "\n":
            print(f"cd {d}")
            print(text)


def git_filter(text):
    def ok(line):
        filters = [
            "up to date",
            "up-to-date",
            "nothing",
            "no changes",
            "branch main",
            "origin/main",
            "git add",
            "git checkout",
            "publish your local",
            "insertions(+)",
            "ing objects:",
        ]
        for f in filters:
            if f in line:
                return False
        return True

    text = text.split("\n")
    text = [line for line in text if ok(line)]
    return "\n".join(text)


def vc_commit(args):
    comment = " ".join(args)
    git_cmd("git add:", "git add -A .")
    git_cmd("git commit:", 'git commit -m "%s"' % comment)


def vc_diff():
    git_cmd("git diff:", "git diff --color")


def vc_dirs():

    # Macs
    hammer = Path.home() / "Hammer"
    if exists(hammer):
        pubs = hammer / "Documents/Shrinking-World-Pubs"
        github = Path.home() / "Github"
        ghost = github / "GhostWriter"
        prometa = github / "ProMETA"
        dirs = []
        dirs.append(hammer)
        dirs.append(prometa)
        dirs.append(pubs)
        dirs.append(ghost)
        return [PurePath(d) for d in dirs if d.exists()]


# def vc_log(args):
#     d = Path(environ['p'])
#     system('figlet Hammer')
#     cmd = f'cd {d} && git log --since="2 day ago" --name-only'
#     print(shell(cmd))
#     d = d / 'Documents'
#     system('figlet Documents')
#     cmd = f'cd {d} && git log --since="2 day ago" --name-only'
#     print(shell(cmd))


def vc_pull(args):
    vc_commit(args)
    cmd = """
        cd ~/Hammer &&
        git checkout production &&
        git pull &&
        git push
        git checkout main &&
        git pull &&
        git push
    """
    system(cmd)


def vc_push():
    cmd = """
        cd ~/Hammer &&
        git checkout production &&
        git pull &&
        git merge main -m "Main Merge" &&
        git push &&
        git checkout main &&
        cd ~/Hammer/Documents/Shrinking-World-Pubs &&
        git push &&
        # Show deployment status
        open https://cloud.digitalocean.com/apps/260d8b80-b11f-4e57-a38d-dea84b9c2396/overview
    """
    system(cmd)


def vc_status():
    git_cmd("git status:", "git status")
