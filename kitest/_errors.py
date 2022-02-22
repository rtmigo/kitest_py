# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

class GradleRunFailed(SystemExit):
    def __init__(self, msg):
        super().__init__(msg)


class UnexpectedOutput(SystemExit):
    def __init__(self, msg):
        super().__init__(msg)