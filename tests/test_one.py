import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from kitest._creator import create_kotlin_sample_project


class TestOne(unittest.TestCase):
    def test(self):
        with TemporaryDirectory() as tds:
            project_root = Path(tds) / "project"

            create_kotlin_sample_project(
                project_root,
                main_code="fun main()",
                package_name="org.sample.package",
                repo_url="https://github.com/user/repo")
            self.assertIn(
                "https://github.com/user/repo",
                (project_root / "settings.gradle.kts").read_text())
