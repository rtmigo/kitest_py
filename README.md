Tool for testing Kotlin libraries. I use it to test my own code.

The library is intentionally written in Python (although it tests Java/Kotlin). 
This
way we avoid modifying the Java framework on a clean system.

## Basic usage (in CI)

To test a Kotlin library in CI, we create a testing script in Python for this
library (for example, `lib_test.py`). And then we run the check like this:

```commandline
pip3 install pip3 install git+https://github.com/rtmigo/kitest_py#egg=kitest

python3 lib_test.py
```

Examples of possible contents of `lib_test.py` are given below.

## run_with_git_dependency

Suppose we have created a library named `mylib`. The library is 
located in the `https://github.com/username/mylib` repository and describes the 
`io.github.username:mylib` module.

To check if the library is successfully connected to third-party projects, 
we create the following script: 

#### lib_test.py (or any name you like)

```python3
#!/usr/bin/env python3 

from kitest import run_with_git_dependency

result = run_with_git_dependency(
    module="io.github.username:mylib",
    url="https://github.com/username/mylib",
    main_kt="""
        // kotlin code that imports and uses the library        

        import io.github.username:mylib.spanishGreeting
        fun main() = println(spanishGreeting())
    """)

if result.text != "¡Hola!\n":
    exit(1)  # error code: we're not happy with the result

# no errors
```

To run the test on a clean system, install `kitest` and run the script:

```commandline
pip3 install pip3 install git+https://github.com/rtmigo/kitest_py#egg=kitest

python3 lib_test.py
```

### Under the hood

It will create a mini-project of a console application **miniApp** in Kotlin.
The miniApp will include your library like this:

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

The program will be executed with `gradle run -q`. Whatever the program prints
out will be returned in the result object.



## Related repositories

* [kitest_sample_kotlin_lib_kt](https://github.com/rtmigo/kitest_sample_kotlin_lib_kt)

## License

Copyright © 2022 Artёm IG <github.com/rtmigo>

Licensed under
the [MIT License](https://github.com/rtmigo/kitest_py/blob/dev/LICENSE).

--------------------------------------------------------------------------------

Work on this library started on 22.02.2022