class UnsavedModifiedProblem(Exception):

    def __init__(self, message):
        
        super(UnsavedModifiedProblem, self).__init__(message)

class NoneAnswerForInputFile(Exception):

    def __init__(self, message):

        super(NotAnswerForInputFile, self).__init__(message)
