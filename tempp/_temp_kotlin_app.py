from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List

from tempp import RunResult


class TempProject:
    def __init__(self,
                 files: dict[str, str],
                 # build_gradle_kts: str,
                 # main_kt: str,
                 # settings_gradle_kts: str = ""

                 ):
        self.files = files

        # self.main_kt = main_kt
        # self.build_gradle_kts = build_gradle_kts
        # self.settings_gradle_kts = settings_gradle_kts

    def _create(self, dst_dir: Path):
        for fn, contents in self.files.items():
            full_fn = dst_dir / fn
            full_fn.parent.mkdir(parents=True, exist_ok=True)
            full_fn.write_text(contents)

    #        pass
    # create_temp_project(src_template_name="kotlin_app",
    #                     dst_dir=dst_dir,
    #                     basename_replacements={
    #                         "build.gradle.kts": self.build_gradle_kts,
    #                         "settings.gradle.kts": self.settings_gradle_kts,
    #                         "Main.kt": self.main_kt,
    #                     },
    #                     string_replacements={})

    @property
    def project_dir(self) -> Path:
        if self._temp_dir is None:
            raise Exception("Unavailable")
        return self._temp_dir / "project"

    def __enter__(self) -> TempProject:
        self._temp_dir = Path(tempfile.mkdtemp())
        self._create(self.project_dir)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self._temp_dir)

    def run(self, args: List[str]) -> subprocess.CompletedProcess:
        result = subprocess.run(args,
                                 cwd=self.project_dir,
                                 universal_newlines=True,
                                 # triggering text mode
                                 capture_output=True)
        return result

        # if result.returncode != 0:
        #     raise GradleRunFailed(
        #         f"Error code: {result.returncode}\n"
        #         f"<stdout>{result.stdout}</stdout>\n"
        #         f"<stderr>{result.stderr}</stderr>")
        # return result
        #
        # output = _run_gradle(self.project_dir)
        # return RunResult(output)
