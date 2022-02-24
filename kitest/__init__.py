# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from pathlib import Path
from ._obsolete_app_with_git_dep import AppWithGitDependency
from ._gradle import RunResult
from ._temp_kotlin_app import TempProject
from ._errors import UnexpectedOutput, GradleRunFailed

assert (Path(__file__).parent/"data").exists()
assert (Path(__file__).parent/"data"/"dependency_from_github").exists()
assert (Path(__file__).parent/"data"/"dependency_from_github"
        /"src"/"main"/"kotlin"/"Main.kt").exists()