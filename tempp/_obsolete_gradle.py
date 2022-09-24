# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import subprocess
import warnings
from pathlib import Path

from ._errors import GradleRunFailed, UnexpectedOutput


def _run_gradle(project_dir: Path) -> subprocess.CompletedProcess:
    result = subprocess.run(["gradle", "run", "-q"],
                            cwd=project_dir,
                            universal_newlines=True,  # triggering text mode
                            capture_output=True)
    if result.returncode != 0:
        raise GradleRunFailed(
            f"Error code: {result.returncode}\n"
            f"<stdout>{result.stdout}</stdout>\n"
            f"<stderr>{result.stderr}</stderr>")
    return result


class RunResult:
    def __init__(self, cp: subprocess.CompletedProcess):
        warnings.warn("Obsolete 2022-09", DeprecationWarning)
        assert isinstance(cp.stdout, str)
        assert isinstance(cp.stderr, str)
        self.process = cp

    @property
    def stdout(self) -> str:
        return self.process.stdout

    def assert_stdout_is(self, expected: str):
        if self.stdout != expected:
            raise UnexpectedOutput(self.stdout)

    def assert_output_is(self, expected: str):
        warnings.warn("Use assert_stdout_is", DeprecationWarning)
        return self.assert_stdout_is(expected)
