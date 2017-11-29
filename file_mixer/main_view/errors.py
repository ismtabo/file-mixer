class UnsavedModifiedProblem(Exception):
    def __init__(self, message):
        super(UnsavedModifiedProblem, self).__init__(message)


class NoneAnswerForInputFile(Exception):
    def __init__(self, message):
        super(NoneAnswerForInputFile, self).__init__(message)


class NoneCurrentProblem(Exception):
    def __init__(self, message):
        super(NoneCurrentProblem, self).__init__(message)


class NoneCurrentProblemSavePath(Exception):
    def __init__(self, message):
        super(NoneCurrentProblemSavePath, self).__init__(message)


class EmptyProblemNumber(Exception):
    def __init__(self, message):
        super(EmptyProblemNumber, self).__init__(message)


class ChoosenFileHasNotInputExtension(Exception):
    def __init__(self, message):
        super(ChoosenFileHasNotInputExtension, self).__init__(message)
