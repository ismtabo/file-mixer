import os
import random
from mmap import mmap

from collections import namedtuple

import time

from .errors import NoneCurrentProblemSavePath
from .patterns import Serializable

FolderTreeElement = namedtuple('FolderTreeElement',
                               ['f', 'size', 'is_folder', 'fullname', 'children'])
ProblemFile = namedtuple('ProblemFile', ['input', 'answer'])


class Problem(Serializable):
    def __init__(self, problemid, used_files=None):
        self._problemid = problemid
        self._path = None
        self._used_files = []
        self._used_files_mm = []
        self.used_files = used_files or []
        self._input = ""
        self._answer = ""

    @property
    def number(self):
        return self._problemid

    @number.setter
    def number(self, new_number):
        self._problemid = new_number

    @property
    def path(self):

        if not self._path:
            raise NoneCurrentProblemSavePath("Please select save path to current problem")
        return self._path

    @path.setter
    def path(self, new_path):

        self._path = new_path

    @property
    def used_files(self):
        return self._used_files

    @used_files.setter
    def used_files(self, new_used_files):
        if self.used_files:
            del self.used_files
        for input_file_name, answer_file_name in new_used_files:
            self.add_used_files(input_file_name, answer_file_name)

    @used_files.deleter
    def used_files(self):
        self._used_files.clear()
        for input_mm, answer_mm in self._used_files_mm:
            input_mm.close()
            answer_mm.close()
        self._used_files_mm.clear()

    def add_used_files(self, input_file_name, answer_file_name):
        self._used_files += [ProblemFile(input_file_name, answer_file_name)]
        with open(input_file_name, 'r+') as file:
            input_file_mm = mmap(file.fileno(), 0)
            self._input += file.read()
        with open(answer_file_name, 'r+') as file:
            answer_file_mm = mmap(file.fileno(), 0)
            self._answer += file.read()
        self._used_files_mm += [ProblemFile(input_file_mm, answer_file_mm)]

    def remove_used_files(self, file_iter):
        del self._used_files[file_iter]
        input_file_mm, answer_file_mm = self._used_files_mm[file_iter]
        input_file_mm.close()
        answer_file_mm.close()
        del self._used_files_mm[file_iter]

    def sort(self):
        _used_files = list(zip(self._used_files, self._used_files_mm))
        _used_files.sort()

        self._used_files.clear()
        self._used_files_mm.clear()

        for files, mm_files in _used_files:
            self._used_files.append(files)
            self._used_files_mm.append(mm_files)

    def shuffle(self):
        random.seed(time.time())
        _used_files = list(zip(self._used_files, self._used_files_mm))
        random.shuffle(_used_files)

        self._used_files.clear()
        self._used_files_mm.clear()

        for files, mm_files in _used_files:
            self._used_files.append(files)
            self._used_files_mm.append(mm_files)

    def generate(self):
        self._input = ""
        self._answer = ""

        for input_file_mm, answer_file_mm in self._used_files_mm:
            input_file_mm.seek(0)
            self._input += input_file_mm.read().decode('ascii')
            answer_file_mm.seek(0)
            self._answer += answer_file_mm.read().decode('ascii')

    def clear(self):
        self._input = ""
        self._answer = ""
        del self.used_files

    @property
    def files_content(self):
        return self._input, self._answer

    def serialize(self):
        return {
            'number': self.number,
            'used_files': [
                {
                    'input': inputfilename,
                    'output': outputfilename
                }
                for inputfilename, outputfilename
                in self.used_files
            ]
        }

    @staticmethod
    def unserialize(marshall):

        problem_used_files = [
            ProblemFile(problemfile['input'], problemfile['output'])
            for problemfile in marshall.get('used_files', [])
            if all(map(os.path.exists, problemfile.values()))
        ]

        return Problem(marshall['number'], problem_used_files)
