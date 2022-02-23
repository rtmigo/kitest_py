# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import shutil
import subprocess
import tempfile
import warnings
from pathlib import Path
from typing import Optional

from kitest._dir_from_template import create_temp_project
from kitest._errors import GradleRunFailed, UnexpectedOutput


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


class AppWithGitDependency:
    def __init__(self,
                 main_kt: str,
                 url: str,
                 module: str,
                 branch: Optional[str] = None):
        self.main_kt = main_kt
        self.url = url
        self.module = module
        self.branch = branch
        self._temp_dir: Optional[Path] = None

    def _create(self, dst_dir: Path):
        details = ""
        # implementation("io.github.rtmigo:repr") { version { branch = "dev" } }
        if self.branch is not None:
            details = """{ version { branch = "__BRANCH__" } }""" \
                .replace("__BRANCH__", self.branch)

        create_temp_project(src_template_name="dependency_from_github",
                            dst_dir=dst_dir,
                            replacements={
                                "__PACKAGE__": self.module,
                                "__REPO_URL__": self.url,
                                "__MAIN_KT__": self.main_kt,
                                "__IMPLEMENTATION_DETAILS__": details
                            })

    @property
    def project_dir(self) -> Path:
        if self._temp_dir is None:
            raise Exception("Unavailable")
        return self._temp_dir / "project"

    def __enter__(self) -> AppWithGitDependency:
        self._temp_dir = Path(tempfile.mkdtemp())
        self._create(self.project_dir)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self._temp_dir)

    def run(self) -> RunResult:
        output = _run_gradle(self.project_dir)
        return RunResult(output)

