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


async def fetch_updates(repo):
    try:
        origin = repo.remote("origin")
    except ValueError:
        origin = repo.create_remote("origin", config.UPSTREAM_REPO)
    await origin.fetch()
    upstream_branch = config.UPSTREAM_BRANCH
    if upstream_branch in repo.heads:
        repo.heads[upstream_branch].checkout(True)
    else:
        repo.create_head(upstream_branch, origin.refs[upstream_branch])
        repo.heads[upstream_branch].set_tracking_branch(origin.refs[upstream_branch])
        repo.heads[upstream_branch].checkout(True)
    try:
        await origin.pull(upstream_branch)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")


async def git():
    REPO_LINK = config.UPSTREAM_REPO
    if config.GIT_TOKEN:
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        TEMP_REPO = REPO_LINK.split("https://")[1]
        UPSTREAM_REPO = f"https://{GIT_USERNAME}:{config.GIT_TOKEN}@{TEMP_REPO}"
    else:
        UPSTREAM_REPO = config.UPSTREAM_REPO

    try:
        repo = Repo()
        LOGGER(__name__).info(f"Git Client Found [VPS DEPLOYER]")
    except (GitCommandError, InvalidGitRepositoryError) as e:
        LOGGER(__name__).info(f"Invalid Git Command or Repository: {e}")
        repo = Repo.init()
        await fetch_updates(repo)
        await install_requirements("pip3 install --no-cache-dir -r requirements.txt")
        LOGGER(__name__).info("Fetching updates from upstream repository...")
