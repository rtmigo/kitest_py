from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from kitest import RunResult
from kitest._obsolete_app_with_git_dep import _run_gradle
from kitest._dir_from_template import create_temp_project


class TempKotlinApp:
    def __init__(self,
                 build_gradle_kts: str,
                 main_kt: str,
                 settings_gradle_kts: str = ""):
        self.main_kt = main_kt
        self.build_gradle_kts = build_gradle_kts
        self.settings_gradle_kts = settings_gradle_kts

    def _create(self, dst_dir: Path):
        create_temp_project(src_template_name="kotlin_app",
                            dst_dir=dst_dir,
                            basename_replacements={
                                "build.gradle.kts": self.build_gradle_kts,
                                "settings.gradle.kts": self.settings_gradle_kts,
                                "Main.kt": self.main_kt,
                            },
                            string_replacements={})

    @property
    def project_dir(self) -> Path:
        if self._temp_dir is None:
            raise Exception("Unavailable")
        return self._temp_dir / "project"

    def __enter__(self) -> TempKotlinApp:
        self._temp_dir = Path(tempfile.mkdtemp())
        self._create(self.project_dir)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self._temp_dir)

    def run(self) -> RunResult:
        output = _run_gradle(self.project_dir)
        return RunResult(output)