# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from kitest._creator import _create_temp_project, run_with_git_dependency


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
        result = run_with_git_dependency(
            module="io.github.rtmigo:kitestsample",
            url="https://github.com/rtmigo/kitest_sample_kotlin_lib_kt",
            main_kt="""
                import io.github.rtmigo.kitestsample.*
                fun main() = println(greet())
            """,

        )
        self.assertEqual(
            result.text, "hello :)\n"
        )
