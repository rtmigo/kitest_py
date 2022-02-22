# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from kitest._creator import _create_temp_project, AppWithGitDependency


class TestOne(unittest.TestCase):
    def test_create_temp_project(self):
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

    def test_run(self):
        with AppWithGitDependency(
                module="io.github.rtmigo:kitestsample",
                url="https://github.com/rtmigo/kitest_sample_kotlin_lib_kt",
                main_kt="""
                import io.github.rtmigo.kitestsample.*
                fun main() = println(greet())
            """) as app:
            result = app.run()
        self.assertEqual(
            result.output, "hello :)\n"
        )
