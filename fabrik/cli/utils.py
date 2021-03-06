import git


def has_git_repro(path=None):
    try:
        repo = git.Repo(path)  # NOQA
    except git.exc.NoSuchPathError:
        return False
    except git.exc.InvalidGitRepositoryError:
        return False

    return True


def get_git_remote(path=None):
    repo = git.Repo(path)
    return repo.remotes.origin.url


def get_git_branch(path=None):
    repo = git.Repo(path)
    branch = repo.active_branch
    return branch.name
