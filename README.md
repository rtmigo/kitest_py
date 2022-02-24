![Generic badge](https://img.shields.io/badge/stability-experimental-red.svg)
![Generic badge](https://img.shields.io/badge/python-3.10+-blue.svg)
![Generic badge](https://img.shields.io/badge/os-Linux_|_MacOS_|_Windows-blue.svg)


# [kitest](https://github.com/rtmigo/kitest_py)

Cross-platform Python script for testing Java/Kotlin libraries.

By using Python (instead of Java-based scripting languages), we avoid 
modifying the Java framework on a testing system.

## Use

Suppose you have created a Kotlin library named `mylib`. You need to test that 
third-party projects can use `mylib` as a dependency.

The test can be run by creating a single file like this:

```python3
# lib_test.py

from kitest import *

with TempGradleApp(
    files={ 
        # minimalistic build script to use the library
        "build.gradle.kts": """
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

        # additional settings, if necessary 
        "settings.gradle.kts": """
            sourceControl {
                gitRepository(java.net.URI("https://github.com/username/mylib.git")) {
                    producesModule("io.github.username:mylib")
                }
            }            
        """,

        # kotlin code that imports and uses the library
        "src/main/kotlin/Main.kt": """
            import io.github.username:mylib.spanishGreeting
            fun main() = println(spanishGreeting())
        """}) as app:
    
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

--------------------------------------------------------------------------------

Work on this script started on 22.02.2022 :)
