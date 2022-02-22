# SPDX-FileCopyrightText: (c) 2022 Artem Galk <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from pathlib import Path
from ._creator import AppWithGitDependency, RunResult, UnexpectedOutput

assert (Path(__file__).parent/"data").exists()
assert (Path(__file__).parent/"data"/"dependency_from_github").exists()
assert (Path(__file__).parent/"data"/"dependency_from_github"/"src"/"main"/"kotlin"/"Main.kt").exists()