[![stability-experimental](https://img.shields.io/badge/stability-experimental-orange.svg)](https://github.com/rtmigo)


# [kitest](https://github.com/rtmigo/kitest_py)



Tool for testing Kotlin libraries.

The library is intentionally written in Python (although it tests Java/Kotlin). 
This way we avoid modifying the Java framework on a clean system.

## AppWithGitDependency

Suppose you have created a Kotlin library named `mylib`. Full module name is
`io.github.username:mylib`. It is located in the `https://github.com/username/mylib` 
repository.

The library contains function `spanishGreeting`, that returns `"¡Hola!"`

You need to test that third-party projects can use `mylib` as a 
dependency, downloading it directly from GitHub.


Create the following script: 

#### lib_test.py (or any name you like)

```python3
#!/usr/bin/env python3 

from kitest import *

with AppWithGitDependency(
        module="io.github.username:mylib",
        url="https://github.com/username/mylib",
        main_kt="""
            // kotlin code that imports and uses the library        
            import io.github.username:mylib.spanishGreeting
            fun main() = println(spanishGreeting())
        """) as app:
    
    app.run().assert_stdout_is("¡Hola!\n")

print("Everything is OK!")
```

To run the test on a clean system, install `kitest` and run the script:

```bash
# assuming pip and python are Python 3.10+
# and lib_test.py is a local file

pip install git+https://github.com/rtmigo/kitest_py
python lib_test.py
```

### Under the hood

It will create a small TestApp, that is a console application in Kotlin. TestApp
will use your library like this:

#### TestApp / settings.gradle.kts

```kotlin
sourceControl {
    gitRepository(java.net.URI("https://github.com/username/mylib.git")) {
        producesModule("io.github.username:mylib")
    }
}
```

#### TestApp / build.gradle.kts

```kotlin
implementation("io.github.username:mylib")
```

The program will be executed with `gradle run -q`. Whatever the program prints
out will be returned in the result object.

## License

Copyright © 2022 
Artёm IG <github.com/rtmigo>

Licensed under
the [MIT License](https://github.com/rtmigo/kitest_py/blob/dev/LICENSE).

Work on this library started on 22.02.2022 :)

--------------------------------------------------------------------------------

## Related repositories

* [kitest_sample_kotlin_lib_kt](https://github.com/rtmigo/kitest_sample_kotlin_lib_kt)
