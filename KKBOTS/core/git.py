import asyncio
import shlex
from typing import Tuple

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

import config

from ..logging import LOGGER


async def install_requirements(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


def get_upstream_repo_link():
    REPO_LINK = config.UPSTREAM_REPO
    if config.GIT_TOKEN:
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        TEMP_REPO = REPO_LINK.split("https://")[1]
        return f"https://{GIT_USERNAME}:{config.GIT_TOKEN}@{TEMP_REPO}"
    else:
        return REPO_LINK


def git():
    UPSTREAM_REPO = get_upstream_repo_link()
    try:
        repo = Repo()
        LOGGER(__name__).info(f"Git Client Found [VPS DEPLOYER]")
    except GitCommandError:
        LOGGER(__name__).info(f"Invalid Git Command")
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.remote("origin") if "origin" in repo.remotes else repo.create_remote("origin", UPSTREAM_REPO)
        origin.fetch()
        upstream_branch_ref = origin.refs[config.UPSTREAM_BRANCH]
        repo.create_head(config.UPSTREAM_BRANCH, upstream_branch_ref)
        repo.heads[config.UPSTREAM_BRANCH].set_tracking_branch(upstream_branch_ref)
        repo.heads[config.UPSTREAM_BRANCH].checkout(True)
        try:
            repo.create_remote("origin", config.UPSTREAM_REPO)
        except BaseException:
            pass
        nrs = repo.remote("origin")
        nrs.fetch(config.UPSTREAM_BRANCH)
        try:
            nrs.pull(config.UPSTREAM_BRANCH)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        install_req("pip3 install --no-cache-dir -r requirements.txt")
        LOGGER(__name__).info(f"Fetching updates from upstream repository...")
