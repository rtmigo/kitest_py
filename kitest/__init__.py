from pathlib import Path
from ._creator import check_kotlin_lib

assert (Path(__file__).parent/"data").exists()
assert (Path(__file__).parent/"data"/"dependency_from_github").exists()