from inspect import getmembers, isfunction
from importlib import machinery
import types
import sys
import os
from .cprint import cprint
from .reporter import Reporter


class Runner:
    def __init__(self, path):
        self.file_paths = [] 
        self.load_file_paths(path)
        self.results = { "passes": 0, "fails": 0, "errors": 0, "files": 0 }

    def load_file_paths(self, path):
        if path.endswith("__pycache__"):
          return

        if os.path.isfile(path):
            self.file_paths.append(path)

        elif os.path.isdir(path):
            for nested_path in os.listdir(path):
                self.load_file_paths(os.path.join(path, nested_path))
  
    def load_module(self, file_path):
        loader = machinery.SourceFileLoader("testmod", file_path)
        module = types.ModuleType("testmod")
        loader.exec_module(module)

        return module

    def load_tests(self, file_path):
        module = self.load_module(file_path)

        self.tests = [m for m in getmembers(module) if isfunction(m[1]) and m[0].startswith("test_")]

        self.before_all = [m for m in getmembers(module) if isfunction(m[1]) and m[0].startswith("before_all")]
        self.after_all = [m for m in getmembers(module) if isfunction(m[1]) and m[0].startswith("after_all")]

        self.before_each = [m for m in getmembers(module) if isfunction(m[1]) and m[0].startswith("before_each")]
        self.after_each = [m for m in getmembers(module) if isfunction(m[1]) and m[0].startswith("after_each")]

    def run_tests_for_file(self, file_path):
        self.load_tests(file_path)

        for before_all in self.before_all:
            before_all[1]()

        for test in self.tests:
            (test_name, test_fn) = test

            [message, error] = test_fn()

            if not error:
                cprint(f"{message}", "success")
                self.results["passes"] += 1

            elif error["type"] == 'PytrunAssertionError':
                cprint(f"{message}: {error["message"]}", "failure")
                self.results["fails"] += 1

            elif error["type"] == 'AssertionError':
                cprint(f"{message}", "failure")
                self.results["fails"] += 1

            else:
                self.results["errors"] += 1

        for after_all in self.after_all:
            after_all[1]()


    def run_all_tests(self):
        for file_path in self.file_paths:
            self.results["files"] += 1
            self.run_tests_for_file(file_path)

        reporter = Reporter(self.results)

        reporter.report()
        
def main(path):    
  Runner(path).run_all_tests()
