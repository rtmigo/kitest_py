Tool for testing Kotlin libraries. I use it to test my own code.

The library is intentionally written in Python (although it tests Java/Kotlin). 
This
way we avoid modifying the Java framework on a clean system.

Examples of possible contents of `lib_test.py` are given below.

## AppWithGitDependency

Suppose we have created a Kotlin library named `mylib`. The library is 
located in the `https://github.com/username/mylib` repository and implements 
the `io.github.username:mylib` module.

There is a Kotlin function `spanishGreeting` in out library, that 
returns `"¡Hola!"`

To check if the library is successfully connected to third-party projects, 
we create the following script: 

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
    
    app.run().assert_output_is("¡Hola!\n")

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