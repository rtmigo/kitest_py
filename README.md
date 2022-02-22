Tool for testing Kotlin libraries. I use it to test my own code.

The library is intentionally written in Python (although it tests Java). This
way we avoid modifying the Java framework on a clean system.

## Basic usage (in CI)

To test a Kotlin library in CI, we create a testing script in Python for this
library (for example, `my_test.py`). And then we run the check like this:

```commandline
pip3 install pip3 install git+https://github.com/rtmigo/kitest_py#egg=kitest

python3 my_test.py
```

## check_kotlin_lib

Creates a mini-project of a console application **miniApp** that includes a
dependent library like this:

#### miniApp / settings.gradle.kts

```kotlin
sourceControl {
    gitRepository(java.net.URI("https://github.com/username/mylib.git")) {
        producesModule("io.github.username:mylib")
    }
}
```

#### miniApp / build.gradle.kts

```kotlin
implementation("io.github.username:mylib")
```

To call the function and check on our library, we run the following code:

#### ourLib / test_as_dependency.py (or any script name you like)

```python3
#!/usr/bin/env python3 

from kitest import check_kotlin_lib

check_kotlin_lib(
    dependency="io.github.username:mylib",
    dependency_url="https://github.com/username/mylib",
    main_kt="""
        import io.github.user:mylib.myLibFunc
        fun main() = println(myLibFunc())
    """,
    expected_output="myLibFunc output\n")
```

Run the check in CI:

```commandline
pip3 install pip3 install git+https://github.com/rtmigo/kitest_py#egg=kitest

python3 test_as_dependency.py
```

If the run returns code zero, then the library was successfully imported from 
GitHub, the `myLibFunc` function was run, and the program printed the expected result
`"myLibFunc output\n"`.

A non-zero error code means one of three things:

1. Gradle run was not successful (returned non-zero code)
2. The launch of the program on Kotlin was not successful (non-zero code
   returned due to an exception or intentionally)
3. The program completed successfully, but output to stdout is not what is
   specified by the expected_output argument



## Related repositories

* [kitest_sample_kotlin_lib_kt](https://github.com/rtmigo/kitest_sample_kotlin_lib_kt)

## License

Copyright © 2022 Artёm IG <github.com/rtmigo>

Licensed under
the [MIT License](https://github.com/rtmigo/kitest_py/blob/dev/LICENSE).

--------------------------------------------------------------------------------

Work on this library started on 22.02.2022