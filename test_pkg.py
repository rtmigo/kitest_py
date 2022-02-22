from chkpkg import Package

if __name__ == "__main__":
    with Package() as pkg:
        pkg.run_python_code('from kitest import run_with_git_dependency, RunResult')

    print("\nPackage is OK!")
