# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from pathlib import Path
from ._obsolete_app_with_git_dep import AppWithGitDependency, RunResult, UnexpectedOutput
from ._temp_kotlin_app import TempKotlinApp

assert (Path(__file__).parent/"data").exists()
assert (Path(__file__).parent/"data"/"dependency_from_github").exists()
assert (Path(__file__).parent/"data"/"dependency_from_github"
        /"src"/"main"/"kotlin"/"Main.kt").exists()