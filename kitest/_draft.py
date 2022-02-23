from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from kitest import RunResult
from kitest._app import _run_gradle
from kitest._dir_from_template import create_temp_project


class TempKotlinApp:
    def __init__(self,
                 build_gradle_kts: str,
                 main_kt: str,
                 settings_gradle_kts: str = ""):
        self.main_kt = main_kt
        self.build_gradle_kts = build_gradle_kts
        self.settings_gradle_kts = settings_gradle_kts

    def _create(self, dst_dir: Path):
        details = ""
        # implementation("io.github.rtmigo:repr") { version { branch = "dev" } }
        # if self.branch is not None:
        #     details = """{ version { branch = "__BRANCH__" } }""" \
        #         .replace("__BRANCH__", self.branch)

        create_temp_project(src_template_name="kotlin_app",
                            dst_dir=dst_dir,
                            basename_replacements={
                                "build.gradle.kts": self.build_gradle_kts,
                                "settings.gradle.kts": self.settings_gradle_kts,
                                "Main.kt": self.main_kt,
                            },
                            string_replacements={})

        # {
        #     "__PACKAGE__": self.module,
        #     "__REPO_URL__": self.url,
        #     "__MAIN_KT__": self.main_kt,
        #     "__IMPLEMENTATION_DETAILS__": details
        # })

    @property
    def project_dir(self) -> Path:
        if self._temp_dir is None:
            raise Exception("Unavailable")
        return self._temp_dir / "project"

    def __enter__(self) -> TempKotlinApp:
        self._temp_dir = Path(tempfile.mkdtemp())
        self._create(self.project_dir)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self._temp_dir)

    def run(self) -> RunResult:
        output = _run_gradle(self.project_dir)
        return RunResult(output)

# class StringVal:
#     def __init__(self, text: str):
#         self.text = text
#
#     def __str__(self):
#         return self.text
#
#
# class Dependencies(StringVal):
#     pass
#
#
# class GitDependency(Dependencies):
#     def __init__(self,
#                  module: str,
#                  branch: str | None = None):
#         details = ""
#         if branch is not None:
#             details = """{ version { branch = "__BRANCH__" } }""" \
#                 .replace("__BRANCH__", branch)
#
#         text = """
#             dependencies {
#                 implementation("__PACKAGE__") __IMPLEMENTATION_DETAILS__
#             }
#         """
#
#         text = text.replace("__PACKAGE__", module) \
#             .replace("__IMPLEMENTATION_DETAILS__", details)
#         super().__init__(text)
#
#
# class BuildGradleKts(StringVal):
#     def __init__(self, dependencies: object = ""):
#         super(BuildGradleKts, self).__init__("""
#         plugins {
#             id("application")
#             kotlin("jvm") version "1.6.10"
#         }
#
#         repositories { mavenCentral() }
#         application { mainClass.set("MainKt") }
#
#         __DEPENDENCIES__
#
#     """.replace("__DEPENDENCIES__", str(dependencies)))
#
#
# class SettingsGradleKts(StringVal):
#     pass
#
#
# class GitProducesModuleSettingsGradleKts(SettingsGradleKts):
#     def __init__(self,
#                  url: str,
#                  module: str):
#
#
# h)
#
# super().__init__(
# """
#     sourceControl {
#         gitRepository(java.net.URI("__REPO_URL__.git")) {
#             producesModule("__PACKAGE__")
#         }
#     }
# """.replace("__REPO_URL__", url)
# .replace("__PACKAGE__", module))
#
# class KotlinCliApp:
#     def __init__(self,
#                  build_gradle_kts: BuildGradleKts | str | None = None,
#                  settings_gradle_kts: SettingsGradleKts | str = ""):
#         self.build_gradle_kts = (build_gradle_kts
#                                  if build_gradle_kts is not None
#                                  else BuildGradleKts())
