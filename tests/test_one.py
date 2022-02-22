import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from kitest._creator import _create_temp_project, check_kotlin_lib
from kitest._errors import UnexpectedOutput


class TestOne(unittest.TestCase):
    def test(self):
        with TemporaryDirectory() as tds:
            project_root = Path(tds) / "project"

            _create_temp_project(
                src_template_name="dependency_from_github",
                dst_dir=project_root,
                replacements={
                    "__PACKAGE__": "org.sample.package",
                    "__REPO_URL__": "https://github.com/user/repo",
                    "__MAIN_KT__": "fun main()"})
            self.assertIn(
                "https://github.com/user/repo",
                (project_root / "settings.gradle.kts").read_text())

    def test_verify(self):
        check_kotlin_lib(
            dependency="io.github.rtmigo:kitestsample",
            dependency_url="https://github.com/rtmigo/kitest_sample_kotlin_lib_kt",
            main_kt="""
                import io.github.rtmigo.kitestsample.*
                fun main() = println(greet())
            """,
            expected_output="hello :)\n"
        )

    def test_unexpected(self):
        with self.assertRaises(UnexpectedOutput):
            check_kotlin_lib(
                dependency="io.github.rtmigo:kitestsample",
                dependency_url="https://github.com/rtmigo/kitest_sample_kotlin_lib_kt",
                main_kt="""
                    import io.github.rtmigo.kitestsample.*
                    fun main() = println(greet())
                """,
                expected_output="completely wrong")
