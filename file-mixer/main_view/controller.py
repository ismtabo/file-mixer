class MainViewController(object):
    """docstring for MainViewController."""
    def __init__(self, view):
        super(MainViewController, self).__init__()
        self.view = view

    def problem_number_changed(self, new_problem_number):
        print(new_problem_number)
