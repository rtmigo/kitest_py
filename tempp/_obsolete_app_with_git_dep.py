# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import shutil
import tempfile
import warnings
from pathlib import Path
from typing import Optional

from tempp._dir_from_template import create_temp_project
from tempp._gradle import _run_gradle, RunResult


class AppWithGitDependency:

    def __init__(self,
                 main_kt: str,
                 url: str,
                 module: str,
                 branch: Optional[str] = None):
        # todo used only by repr. Rewrite CI and remove
        warnings.warn("Obsolete", DeprecationWarning)
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
                            basename_replacements={},
                            string_replacements={
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
