from .cprint import cprint

class Reporter:
    def __init__(self, results):
        self.results = results

    def report(self):
        total_number_of_tests = self.results["passes"] + self.results["fails"] + self.results["errors"]

        print('\n')

        print(f"Test files\t{self.results["files"]}")
        print(f"Tests\t{total_number_of_tests}")

        if self.results["passes"]:
            cprint(f"Tests passed\t{self.results["passes"]}", "success")

        if self.results["fails"]:
            cprint(f"Tests failed\t{self.results["fails"]}", "failure")
      
