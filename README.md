![Generic badge](https://img.shields.io/badge/stability-experimental-red.svg)
![Generic badge](https://img.shields.io/badge/python-3.10+-blue.svg)
![Generic badge](https://img.shields.io/badge/os-Linux_|_MacOS_|_Windows-blue.svg)


# [kitest](https://github.com/rtmigo/kitest_py)

Tool for testing Kotlin libraries.

`kitest` is written in Python (although it tests Java/Kotlin). This way we 
avoid modifying the Java framework on a testing system.

## TempKotlinApp

Suppose you have created a Kotlin library named `mylib`. The library contains 
function `spanishGreeting`, that returns `"¡Hola!"`.

You need to test that third-party projects can use `mylib` as a 
dependency.

The test can be run by creating a file like this:

#### lib_test.py (or any name you like)

```python3
from kitest import *

with TempKotlinApp(
        build_gradle_kts="""
            plugins {
                id("application")
                kotlin("jvm") version "1.6.10"
            }
            
            repositories { mavenCentral() }
            application { mainClass.set("MainKt") }
            
            dependencies {
                implementation("io.github.username:mylib")
            }            
        """,
        
        settings_gradle_kts="""
            sourceControl {
                gitRepository(java.net.URI("https://github.com/username/mylib.git")) {
                    producesModule("io.github.username:mylib")
                }
            }            
        """,
        
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

It will create a small app in a temporary directory. The program will be 
executed with `gradle run -q`. Whatever the program prints
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
