from __future__ import annotations

import inspect
import shutil
import subprocess
import tempfile
from collections.abc import Iterable
from pathlib import Path
from typing import List


class Glob:
    def __init__(self,
                 src_ref: Path,
                 src_glob: str,
                 dst_ref: Path):
        self.src_glob = src_glob
        self.dst = dst_ref
        self.src_ref = src_ref

    def copy(self):
        # TODO unit test
        if self.src_ref is None:
            self.src_ref = Path(".").absolute()
        for p in self.src_ref.rglob(self.src_glob):
            abs_target = self.dst / p.relative_to(self.src_ref)
            print(f"Copying {p} to {abs_target}")
            if p.is_dir():
                shutil.copytree(p, abs_target)
            else:
                shutil.copy(p, abs_target)


class TempProject:
    def __init__(self,
                 files: dict[str, str],
                 copy: Iterable[Glob] | None = None):
        self.files = files
        self.copy = copy

    def _create(self, dst_dir: Path):
        for fn, contents in self.files.items():
            full_fn = dst_dir / fn
            full_fn.parent.mkdir(parents=True, exist_ok=True)
            full_fn.write_text(contents)
        if self.copy is not None:
            # TODO unit test
            for c in self.copy:
                match c:
                    case Glob():
                        c.copy()
                    case _:
                        raise TypeError(c)

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

    def print_files(self, unindent: bool = True):
        for file in sorted(self.project_dir.rglob("*")):
            if file.is_file():
                print(("## " + str(file.relative_to(self.project_dir)) + " ")
                      .ljust(80, "#"))
                print()
                text = file.read_text()
                if unindent:
                    text = inspect.cleandoc(text)
                print(text)
                print()

    def run(self, args: List[str]) -> subprocess.CompletedProcess:
        result = subprocess.run(args,
                                cwd=self.project_dir,
                                universal_newlines=True,
                                # triggering text mode
                                capture_output=True)
        return result
