def expect(value):
    return Assertion(value)

class PytrunAssertionError(RuntimeError):
    def __init__(self, message):
        self.message = message


def equal(value, result):
    return value == result

def not_equal(value, result):
    return value != result


class Assertion:
    def __init__(self, value):
        self.value = value

    def to_equal(self, compare_to):
        self._assert(equal, compare_to)

    def not_equal(self, compare_to):
        self._assert(not_equal, compare_to)
    
    def _assert(self, check, compare_to):
        if not check(self.value, compare_to):
            raise PytrunAssertionError(f"expected {self.value} {check.__name__} {compare_to}")


