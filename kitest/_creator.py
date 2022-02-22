# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from kitest._errors import GradleRunFailed


def _replace_in_string(text: str, replacements: dict[str, str]) -> str:
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def _header(txt: str) -> str:
    return f"<{txt}> ".ljust(80, '-')


def _replace_in_dir(parent: Path, replacements: dict[str, str]):
    for p in parent.rglob('*'):
        if p.is_file():
            old_text = p.read_text()
            new_text = _replace_in_string(old_text, replacements)
            if new_text != old_text:
                p.write_text(new_text)
            print(_header(p))
            print(p.read_text())
            print(_header("/" + str(p)))
            print()


def _create_temp_project(src_template_name: str,
                         dst_dir: Path,
                         replacements: dict[str, str]):
    src_dir = Path(__file__).parent / "data" / src_template_name
    if not src_dir.exists():
        raise FileNotFoundError(src_dir)
    if dst_dir.exists():
        raise FileExistsError(dst_dir)
    shutil.copytree(src_dir, dst_dir)
    _replace_in_dir(dst_dir, replacements)


def _get_gradle_run_output(project_dir: Path) -> str:
    result = subprocess.run(["gradle", "run", "-q"],
                            cwd=project_dir,
                            capture_output=True)
    if result.returncode != 0:
        raise GradleRunFailed(
            f"Error code: {result.returncode}\n"
            f"<stdout>{(result.stdout or b'').decode()}</stdout>\n"
            f"<stderr>{(result.stderr or b'').decode()}</stderr>")
    return result.stdout.decode()


class TempProjectDir:
    """When `path` is `None`, creates a temporary directory and removes it
    afterwards.

    When `path` is not `None`, does nothing with the path.
    """

    def __init__(self, path: Optional[Path]):
        self.autoremove = False
        self.path: Optional[Path] = path

    def __enter__(self) -> Path:
        if self.path is not None and self.path.exists():
            raise FileExistsError(self.path)
        if self.path is None:
            self.path = Path(tempfile.mkdtemp())
            self.autoremove = True
        return self.path / "temp_project"

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.autoremove:
            if self.path.exists():
                shutil.rmtree(self.path)


class RunResult:
    def __init__(self, text: str):
        self.text = text


def run_with_git_dependency(main_kt: str,
                            url: str,
                            module: str,
                            temp_project_dir: Path = None) -> RunResult:
    with TempProjectDir(temp_project_dir) as dst_dir:
        _create_temp_project(src_template_name="dependency_from_github",
                             dst_dir=dst_dir,
                             replacements={"__PACKAGE__": module,
                                           "__REPO_URL__": url,
                                           "__MAIN_KT__": main_kt})

        output = _get_gradle_run_output(dst_dir)
        return RunResult(text=output)
