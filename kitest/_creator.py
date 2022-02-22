import shutil
import subprocess
from pathlib import Path


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
                print(_header(p.name))
                print(new_text)
                print(_header("/"+p.name))
                print()


def _create_temp_project(src_template_name: str,
                         dst_dir: Path,
                         replacements: dict[str, str]):
    src_dir = Path(__file__).parent / "templates" / src_template_name
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
        raise Exception(f"Error code: {result.returncode}\n"
                        f"<stdout>{(result.stdout or b'').decode()}</stdout>\n"
                        f"<stderr>{(result.stderr or b'').decode()}</stderr>")
    return result.stdout.decode()

class UnexpectedOutput(SystemExit):
    def __init__(self, msg):
        super().__init__(msg)


def verify_kotlin_sample_project(project_dir: Path,
                                 main_code: str,
                                 repo_url: str,
                                 package_name: str,
                                 expected_output: str):
    _create_temp_project(src_template_name="cli",
                         dst_dir=project_dir,
                         replacements={"__PACKAGE__": package_name,
                                       "__REPO_URL__": repo_url,
                                       "__MAIN_KT__": main_code})

    output = _get_gradle_run_output(project_dir)
    if output != expected_output:
        raise UnexpectedOutput(output)
        #print(f"Unexpected output: {output}")
        #exit(1)
