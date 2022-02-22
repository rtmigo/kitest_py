import shutil
from pathlib import Path
from typing import Iterable


def _replace_all(text: str, pairs: Iterable[tuple[str, str]]) -> str:
    for src, dst in pairs:
        text = text.replace(src, dst)
    return text


def create_kotlin_sample_project(project_dir: Path,
                                 main_code: str,
                                 repo_url: str,
                                 package_name: str):
    if project_dir.exists():
        raise FileExistsError(project_dir)
    shutil.copytree(Path(__file__).parent / "templates" / "cli",
                    project_dir)
    for p in project_dir.rglob('*'):
        if p.is_file():
            old_text = p.read_text()
            new_text = _replace_all(
                old_text,
                [("__PACKAGE__", package_name),
                 ("__REPO_URL__", repo_url),
                 ("__MAIN_KT__", main_code)])
            if new_text != old_text:
                p.write_text(new_text)
                print()
                print("-" * 80)
                print(p.name)
                print("-" * 80)
                print(new_text)
