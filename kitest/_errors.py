class GradleRunFailed(SystemExit):
    def __init__(self, msg):
        super().__init__(msg)


class UnexpectedOutput(SystemExit):
    def __init__(self, msg):
        super().__init__(msg)