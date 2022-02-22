# SPDX-FileCopyrightText: (c) 2022 Artem Galk <rtmigo.github.io>
# SPDX-License-Identifier: MIT

class GradleRunFailed (Exception):
    def __init__(self, msg):
        super().__init__(msg)


class UnexpectedOutput (Exception):
    def __init__(self, msg):
        super().__init__(msg)