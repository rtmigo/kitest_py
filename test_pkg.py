from chkpkg import Package

if __name__ == "__main__":
    with Package() as pkg:
        pkg.run_shell_code('kitest --help')

    print("\nPackage is OK!")
