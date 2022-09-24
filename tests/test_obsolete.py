import unittest

from tempp._obsolete_app_with_git_dep import AppWithGitDependency


@unittest.SkipTest
class TestAppGitObsolete(unittest.TestCase):

    # will fail if gradle is not installed

    @unittest.SkipTest
    def test_app_git_staging_branch(self):
        with AppWithGitDependency(
                module="io.github.user:repo",
                url="https://github.com/user/repo",
                branch="staging",
                main_kt="""
                    import io.github.user.repo.*
                    fun main() = println(something())
                """) as app:
            self.assertIn(
                """{ version { branch = "staging" } }""",
                (app.project_dir / "build.gradle.kts").read_text())

    @unittest.SkipTest
    def test_app_git_no_branch(self):
        with AppWithGitDependency(
                module="io.github.user:repo",
                url="https://github.com/user/repo",
                main_kt="""
                    import io.github.user.repo.*
                    fun main() = println(something())
                """) as app:
            self.assertNotIn(
                "branch",
                (app.project_dir / "build.gradle.kts").read_text())

    @unittest.SkipTest
    def test_run(self):
        with AppWithGitDependency(
                module="io.github.rtmigo:kitestsample",
                url="https://github.com/rtmigo/kitest_sample_kotlin_lib_kt",
                main_kt="""
                    import io.github.rtmigo.kitestsample.*
                    fun main() = println(greet())
                """) as app:
            result = app.run()
        self.assertEqual(result.stdout, "hello :)\n")
