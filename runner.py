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

    def find_tests_name(self, module):
        try:
          return [m for m in getmembers(module) if m[0] == "tests_name"][0][1]
        except Exception:
            raise Exception("Tests should have a name")

    def find_test_members(self, module, test_member_name):
        return [m for m in getmembers(module) if isfunction(m[1]) and m[0].startswith(test_member_name)]

    def load_tests(self, file_path):
        module = self.load_module(file_path)

        self.tests_name = self.find_tests_name(module)

        self.tests = self.find_test_members(module, "test_")

        self.before_all = self.find_test_members(module, "before_all")
        self.after_all = self.find_test_members(module, "after_all")

        self.before_each = self.find_test_members(module, "before_each")
        self.after_each = self.find_test_members(module, "after_each")

    def run_tests_for_file(self, file_path):
        self.load_tests(file_path)

        number_of_tests_in_file = len(self.tests)

        print(file_path)

        print(f"{self.tests_name} ({number_of_tests_in_file})")

        for before_all in self.before_all:
            before_all[1]()

        for test in self.tests:
            (test_name, test_fn) = test

            try:
              [test_description, error] = test_fn()
            except Exception:
                raise Exception('Test should have a description') 

            result_description = test_description or test_name

            if not error:
                cprint(f"✓ {result_description}", "success", 2)
                self.results["passes"] += 1

            elif error["type"] == 'PytrunAssertionError':
                cprint(f"× {result_description}: {error["message"]}", "failure", 2)
                self.results["fails"] += 1

            elif error["type"] == 'AssertionError':
                cprint(f"× {result_description}", "failure", 2)
                self.results["fails"] += 1

            else:
                self.results["errors"] += 1

        for after_all in self.after_all:
            after_all[1]()


    def run_all_tests(self):
        for file_path in self.file_paths:
            self.results["files"] += 1
            self.run_tests_for_file(file_path)
            print("\n")

        reporter = Reporter(self.results)

        reporter.report()
        
def main(path):    
  Runner(path).run_all_tests()
