# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from pathlib import Path
from ._creator import run_with_git_dependency, RunResult

assert (Path(__file__).parent/"data").exists()
assert (Path(__file__).parent/"data"/"dependency_from_github").exists()